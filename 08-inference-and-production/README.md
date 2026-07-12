# ⚡ Inference, Serving & Production LLM Systems

This is the topic that separates "I call the API" from "I can own an LLM feature in production" - and it dominates system-design rounds for AI Engineer roles at labs, big tech, and startups alike. Infra-flavoured teams will drill into KV cache math and batching schedulers; product-flavoured teams will drill into SLOs, cost engineering, and reliability. Either way, you're expected to reason quantitatively: bytes, tokens/sec, dollars.

## Crash course

### The two phases of inference

Every LLM request has two radically different phases:

- **Prefill**: process the entire prompt in one pass. All prompt tokens are computed in parallel → big matrix-matrix multiplies → **compute-bound**. Cost grows with prompt length (attention is quadratic, GEMMs linear). Prefill determines **time-to-first-token (TTFT)**.
- **Decode**: generate output tokens one at a time. Each step is a matrix-*vector* multiply that must stream **all model weights (plus the KV cache) from GPU HBM** to produce a single token → **memory-bandwidth-bound**. Decode determines **time-per-output-token (TPOT)**.

**Arithmetic intensity** (FLOPs per byte moved) explains this. GPUs have a "ridge point" - roughly peak FLOPs ÷ memory bandwidth (~300 FLOPs/byte for an H100 at BF16). Prefill sits far above it (fully parallel GEMMs); batch-1 decode sits at ~1-2 FLOPs/byte, so the GPU idles waiting on memory. Consequences:

- Batch-1 decode speed has a hard ceiling: `weight bytes ÷ bandwidth`. A 70B model in FP16 (~140 GB) on ~3.35 TB/s HBM ⇒ ~24 tok/s max, no matter how fast the compute is.
- **Batching decode is nearly free**: the same weight-read serves every sequence in the batch, so throughput scales almost linearly with batch size until you hit compute or memory limits. Almost every serving optimisation is a scheme to keep decode batches large.

### KV cache: the thing that eats your GPU

During decode, each new token attends to all previous tokens' keys/values. Caching them avoids O(n²) recompute - but the cache is huge:

```
KV bytes/token = 2 (K,V) × n_layers × n_kv_heads × head_dim × bytes_per_elem
```

Worked example - Llama-3-70B-shaped model (80 layers, 8 KV heads via GQA, head_dim 128, FP16):

```
2 × 80 × 8 × 128 × 2 bytes ≈ 320 KB/token
  8K-token context  → ~2.6 GB per sequence
128K-token context  → ~41 GB per sequence (!)
```

On an 80 GB GPU already holding ~40 GB of INT4 weights, KV cache is what caps concurrent sequences - **batch size, and therefore throughput, is limited by KV memory**, not compute. Hence GQA (fewer KV heads), MLA (low-rank KV compression), KV-cache quantization (FP8/INT8 KV), and paged allocation.

### Making decode fast: the serving playbook

- **Continuous (in-flight) batching** (Orca, now universal): compose the batch *per decode step*, not per request. Finished sequences exit immediately; queued ones join mid-flight. Fixes static batching's convoy problem (whole batch waits for the longest output) and typically lifts throughput several-fold at similar latency.
- **PagedAttention** (vLLM): allocate KV cache in fixed-size blocks (e.g. 16 tokens) mapped through a block table - virtual memory for KV. Kills the internal/external fragmentation of contiguous per-sequence allocations (which wasted most of KV memory), enables near-zero-copy prefix sharing, and lets you safely run much larger batches.
- **Chunked prefill** (Sarathi-Serve): split long prefills into chunks and mix them into decode batches, so one 50K-token prompt doesn't stall every other user's token stream. Trades slightly worse TTFT for that prompt against stable inter-token latency for everyone.
- **Prefix / prompt caching**: reuse the KV cache of a shared prefix (system prompt, few-shot examples, long documents, conversation history) across requests. Self-hosted: prefix-aware routing + radix trees (SGLang) or hash-based block reuse (vLLM). API providers bill cached input tokens at a steep discount (~90% off reads on Anthropic, with a small write premium; ~50-75% off on OpenAI, applied automatically) - structuring prompts as *stable prefix first, variable content last* is one of the highest-ROI cost optimisations available.
- **Speculative decoding**: a cheap drafter proposes k tokens; the target model verifies them in one parallel pass; accepted tokens are emitted, the first rejection is replaced by a sample from the target. With the right accept/reject rule the output distribution is *exactly* the target model's - it's a latency optimisation with no quality tradeoff. Wins (~2-3× on ITL) when acceptance rate is high and there's spare compute; loses at high batch sizes or with poorly matched drafters.

### Quantization

- **Weights-only** (W4A16, W8A16): shrink weights to 4/8-bit, compute in FP16. Since decode is weight-bandwidth-bound, 4-bit weights ≈ up to ~4× faster batch-1 decode *and* 4× less memory. GPTQ (Hessian-based rounding) and AWQ (activation-aware scaling of salient channels) are the standard 4-bit PTQ methods; GGUF k-quants are the llama.cpp/Ollama ecosystem equivalent.
- **Weights + activations** (W8A8 INT8/FP8): also accelerates the *matmuls* themselves via INT8/FP8 tensor cores - this is what helps at high batch/prefill (compute-bound). FP8 is the workhorse on Hopper; FP4 variants (NVFP4/MXFP4) arrive with Blackwell-era hardware and some open-weight releases ship in MXFP4.
- **Typical quality cost**: 8-bit ≈ negligible; good 4-bit ≈ small but measurable (evaluate on *your* task, not just perplexity); below 4-bit gets rough. **KV-cache quantization** (FP8 KV) is a separate lever that directly buys batch size.

### Metrics, SLOs, and the throughput - latency curve

| Metric | Meaning | Driven by |
|---|---|---|
| **TTFT** | time to first token | queueing + prefill (prompt length) |
| **TPOT / ITL** | time per output token after the first | memory bandwidth, batch contention |
| **tokens/sec** | per-request or aggregate throughput | batch size, hardware |
| **Goodput** | throughput *that meets SLOs* | scheduler quality, load |
| **P50 vs P99** | median vs tail | tail = queue spikes, long prompts, preemptions |

Total latency ≈ `TTFT + TPOT × output_tokens`. Throughput and latency trade off along a curve: pushing batch size up raises tokens/sec but inflates TPOT and queue delay; past saturation, throughput plateaus while latency explodes. You pick an operating point from your SLO (e.g. "P99 TTFT < 800 ms, P99 ITL < 60 ms for interactive chat") and buy enough capacity to stay left of the knee. Report **goodput**, not raw throughput - 10K tok/s at 30 s TTFT is worthless for chat.

**Streaming** is the UX half of latency: SSE (`text/event-stream`) delivers deltas as they're generated, so perceived latency ≈ TTFT (hundreds of ms) instead of full completion (tens of seconds). Tool calls and JSON arrive as partial fragments - buffer per-block, or use incremental/partial JSON parsing for progressive UI.

### GPU memory math & parallelism one-liners

```
GPU memory ≈ weights (params × bytes/param)
           + KV cache (per-token bytes × total cached tokens)
           + activations & buffers (~few GB, batch/seq dependent)
```

- 8B model: FP16 ≈ 16 GB, INT4 ≈ ~4.5 GB (runs on a laptop).
- 70B model: FP16 ≈ 140 GB (needs 2× 80 GB GPUs), INT4 ≈ ~40 GB (fits one 80 GB GPU with room for KV).
- **Tensor parallelism (TP)**: shard every layer's matrices across GPUs, all-reduce each layer - cuts per-token latency, needs NVLink-class interconnect, standard within a node.
- **Pipeline parallelism (PP)**: shard by layer ranges across GPUs/nodes - tolerates slower interconnect, adds latency and pipeline bubbles; used when the model can't fit in one node.

### Choosing a serving stack

| Stack | Sweet spot |
|---|---|
| **vLLM** | default open-source choice; PagedAttention, continuous batching, huge model/hardware coverage |
| **SGLang** | shared-prefix-heavy and agentic workloads (RadixAttention prefix reuse), fast structured output |
| **TensorRT-LLM** | max performance on NVIDIA when you'll invest in engine builds/tuning |
| **TGI** | Hugging Face ecosystem integration, solid general-purpose server |
| **llama.cpp / Ollama / MLX** | CPU/edge/laptop and Apple Silicon; GGUF quants; dev-friendly local serving |

### Production patterns (the other half of the interview)

- **Self-host vs API**: decide on utilization (steady high volume favours self-host; spiky/low favours API), privacy/residency, model needs (frontier quality → API; fine-tuned/custom → self-host), team (inference infra is an oncall commitment), and unit economics (GPU-$/hr ÷ achievable tokens/hr vs per-token API price - batching efficiency dominates this math).
- **Reliability**: retries with **exponential backoff + full jitter** on 429/5xx (respect `Retry-After`), client-side concurrency caps, **circuit breakers** per provider, layered timeouts (connect, TTFT, inter-chunk inactivity, total), idempotency keys for side-effectful pipelines, fallback provider/model chains.
- **Cost engineering**: output tokens cost ~3-5× input tokens, and reasoning tokens bill as output - control `max_tokens` and reasoning effort. Levers, in rough ROI order: prompt/prefix caching, model tiering/cascades (cheap model + escalation), context truncation/summarization, batch APIs (~50% off for async work), semantic caching. Attribute cost per request/feature/user from day one.
- **Capacity & autoscaling**: GPU cold starts are minutes (node provision + image pull + weight load), so autoscale on queue depth/KV utilization with warm pools and predictive scaling - not CPU%.
- **Observability**: dashboard TTFT/ITL percentiles, queue depth, batch size, KV-cache utilization, preemptions, tokens in/out, error/429 rates, cost per request. GPU "utilization" alone is misleading - a memory-bound decode can show 100% while doing little compute.
- **Graceful degradation**: under overload, shed or queue low-priority traffic, fall back to smaller models, truncate history, cap output length, serve cached answers - degrade quality before availability.

## Interview questions

See [questions.md](questions.md) - 36 questions across basic, intermediate, and advanced.

## Red flags interviewers watch for

- Can't explain *why* prefill and decode are bottlenecked differently - treats "GPUs are fast" as the whole story, or can't connect memory bandwidth to tokens/sec.
- No KV cache number sense: can't ballpark bytes/token or explain why long contexts and big batches fight for the same memory.
- Hand-waves "we'll use vLLM" in system design without being able to say what PagedAttention or continuous batching actually do.
- Believes speculative decoding changes output quality, or that quantization is free - no instinct to evaluate on the actual task.
- Designs SLOs around average latency only; never mentions P99, TTFT vs ITL, or goodput; can't sketch the throughput - latency tradeoff.
- Cost blindness: doesn't know output tokens cost more than input, never mentions prompt caching, batch APIs, or model tiering when asked to cut a bill.
- Naive reliability: retries without jitter or budget (amplifying outages), one global timeout for a streaming call, no fallback plan for provider incidents.
- Chooses self-hosting "for cost" with zero utilization math, or an API "for simplicity" where privacy/latency constraints clearly forbid it.

## Further reading

- [Efficiently Scaling Transformer Inference (Pope et al., 2022)](https://arxiv.org/abs/2211.05102) - the canonical treatment of prefill/decode, batching, and parallelism tradeoffs.
- [Transformer Inference Arithmetic (kipply)](https://kipp.ly/transformer-inference-arithmetic/) - the classic back-of-envelope guide to KV cache, bandwidth, and latency math.
- [Efficient Memory Management for LLM Serving with PagedAttention (Kwon et al., 2023)](https://arxiv.org/abs/2309.06180) - the vLLM paper.
- [Orca: A Distributed Serving System for Transformer-Based Generative Models (Yu et al., OSDI 2022)](https://www.usenix.org/conference/osdi22/presentation/yu) - where continuous batching comes from.
- [Fast Inference from Transformers via Speculative Decoding (Leviathan et al., 2022)](https://arxiv.org/abs/2211.17192) - speculative decoding with the correctness proof.
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve (Agrawal et al., 2024)](https://arxiv.org/abs/2403.02310) - chunked prefill and stall-free scheduling.
- [vLLM documentation](https://docs.vllm.ai/) - the practical reference for a modern serving stack.
- [Exponential Backoff and Jitter (AWS Architecture Blog)](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) - the standard reference for retry design.
