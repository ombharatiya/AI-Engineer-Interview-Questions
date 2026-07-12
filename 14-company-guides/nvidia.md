# 🟩 NVIDIA - AI Engineer Interview Guide

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- **The hypothesis holds: AI roles skew systems/performance.** Public reports consistently describe loops centred on hardware-software co-design - GPU memory hierarchy, quantization, inference optimization, TensorRT/TensorRT-LLM, Triton/NIM - rather than model-architecture trivia. Expect performance math, not just ML flashcards.
- **CUDA literacy is expected even when you won't write kernels.** Multiple public guides report that AI/ML candidates are asked to read CUDA and reason about memory coalescing, warp divergence, and bank conflicts. C++ shows up in coding rounds far more than at typical "AI engineer" employers.
- **Standard big-tech loop shape, domain-heavy content.** Recruiter screen → technical phone screen (CoderPad/HackerRank) → optional hiring-manager call → 3-6 round final loop (coding, domain deep-dive, system design for senior, behavioural). End-to-end reports range 4-8 weeks.
- **Loops vary a lot by business unit.** A TensorRT-LLM performance role, an AI-frameworks role, and a Generative AI Solutions Architect role interview very differently - SA loops are reported as panel-style architecture conversations (up to ~7 technical discussions), not LeetCode marathons. Ask your recruiter what your specific loop covers; they generally tell you.
- **Culture screens are real but technical.** NVIDIA's publicly stated values - innovation, intellectual honesty, speed & agility, excellence, one team - show up as probing on how you handle being wrong, how fast you ship, and whether you can defend every claim you make. Even "leadership" conversations are reported to stay technical.

## Company context

NVIDIA builds the compute layer of the AI industry: GPUs (Hopper, Blackwell), the CUDA platform, networking (NVLink, InfiniBand/Spectrum-X), and an increasingly thick software stack on top - TensorRT-LLM, Triton Inference Server, NIM microservices, NeMo, Omniverse, and full AI "blueprints" for enterprises. Engineers want in because it's the rare place where the hardware, compiler, kernel, and serving layers are all first-party - you can chase a performance problem from PyTorch down to the SM. "AI engineer" at NVIDIA usually means *making models run fast and shipping the software that makes that repeatable* - inference optimization, framework internals, DL libraries, or customer-facing architecture - much more often than training frontier models.

## Roles & titles they hire

Actual posting titles from [jobs.nvidia.com](https://jobs.nvidia.com/) (the mix shifts constantly):

- **Deep Learning Software Engineer** - e.g. "Senior Deep Learning Software Engineer, PyTorch - TensorRT Performance"; inference stack, framework integration, kernel-adjacent work
- **AI/ML Infrastructure Engineer / System Software Engineer** - clusters, schedulers, serving infrastructure
- **Developer Technology Engineer (DevTech)** - NVIDIA's performance-engineering specialists; work with key customers/apps to optimize on NVIDIA hardware. The most CUDA-heavy loop of the AI-adjacent roles
- **Solutions Architect, Generative AI** - customer-facing technical role; NVIDIA's closest analog to a forward-deployed engineer. Architecture, LLM deployment, cost optimization
- **Deep Learning Algorithms Engineer** - numerics, model optimization, quantization, sparsity
- **Applied Deep Learning Research / Research Scientist** - publication-adjacent track (NeMo, model research); different loop, mostly out of scope here
- **Software Engineer, AI Frameworks** - PyTorch/JAX enablement, compilers (some overlap with the CUDA/compiler org)

## The interview loop

NVIDIA does not publish an official step-by-step interview guide, so confidence here is **medium**: the shape below is triangulated from third-party prep guides and aggregated candidate reports, which are broadly consistent with each other but vary by team and seniority.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter screen | 30-45 min call | Background, motivation ("why NVIDIA"), role/team fit, logistics |
| Online assessment | ~75 min HackerRank - DS&A problems plus multiple choice; mostly new-grad and some SWE pipelines (reported, varies) | Medium-difficulty coding, CS fundamentals |
| Technical phone screen | 45-60 min with a peer engineer; CoderPad/HackerRank; resume deep-dive + live coding (reported, varies) | Coding in C++ or Python, domain fluency, how you reason aloud |
| Hiring manager call | 30-60 min, mixed behavioural + high-level technical (reported, varies) | Project depth, ownership, team fit |
| Final loop | 3-6 back-to-back rounds of 45-60 min, virtual or onsite | 1-2 coding rounds; domain deep-dive (GPU architecture, DL, inference optimization); system design for senior roles; behavioural with the hiring manager |
| Solutions Architect variant | Panel with several senior SAs plus serial technical conversations - candidates report up to ~7 rounds, all technical including "leadership" chats (reported, varies) | Architecture discussion, cost-effective LLM deployment, customer scenarios, communication |
| Decision | Days to ~2 weeks after finals | - |

End-to-end timelines reported publicly range from ~4 to 8 weeks; referrals reportedly compress this.

## What they emphasise

- **Hardware-software co-design over model trivia.** The consistent public signal for 2025-2026 loops: can you make a model fast on a GPU? Quantization (FP8/INT4), kernel fusion, KV-cache management, batching strategy, and Triton/TensorRT deployment come up across AI roles - not just kernel teams.
- **Performance math on the spot.** Estimating tokens/sec from memory bandwidth, sizing KV caches, deciding compute-bound vs memory-bound - being able to do roofline-style arithmetic in your head is a strong differentiator, because it's the daily job.
- **C++ and systems depth.** Unusual among "AI engineer" employers: C++ is a first-class interview language, and OS/architecture fundamentals (caches, memory hierarchy, concurrency) are reported in loops even for ML-flavoured roles.
- **CUDA reading fluency.** You don't need to have shipped kernels for most AI roles, but you should read a kernel and spot uncoalesced access, warp divergence, or a bank conflict, and know what Nsight would tell you.
- **Intellectual honesty and speed.** NVIDIA's stated core values surface in behavioural rounds: they probe how you respond when you're wrong, whether you overclaim, and whether you ship at "speed of light." Bluffing on a technical answer is reported to end loops fast.
- **Communication for customer-facing roles.** SA/DevTech loops weight explaining tradeoffs to a skeptical technical audience - deploying an LLM cost-effectively is a reported interview theme almost verbatim from the job descriptions.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. You want to serve a 70B-parameter model on a single 80 GB GPU. Walk me through whether it fits and what single-stream tokens/sec you'd expect.

<details><summary><b>Answer</b></summary>

Start with memory: 70B params at FP16 is ~140 GB - it doesn't fit on one 80 GB GPU. Options: tensor-parallel across 2 GPUs, or quantize. Weight-only INT4 gets you to ~35 GB, leaving ~40+ GB for KV cache and activations - that's the usual single-GPU answer.

Then throughput: autoregressive decode at batch 1 is memory-bandwidth-bound, because every generated token streams essentially all weights through the SMs once (GEMV, arithmetic intensity ≈ 2 FLOPs/byte, far below the GPU's ridge point). So the ceiling is:

tokens/sec ≈ memory bandwidth / bytes read per token

On an H100-class part (~3.3 TB/s HBM), INT4 weights (~35 GB) give a ceiling of roughly 90-95 tokens/sec single-stream. Real systems land below that - KV-cache reads grow with context, kernels don't hit peak bandwidth, and dequantization adds overhead - so quoting "maybe 60-80% of the ceiling" shows calibration. At FP16 across 2 GPUs, the same math gives ~24 tok/s per stream (140 GB over ~3.3 TB/s per GPU with TP splitting the reads).

The senior follow-through: single-stream latency is the wrong target for most services. Batching amortises the weight reads across requests, raising arithmetic intensity until you approach compute-bound - which is why throughput-oriented serving runs large batches and the per-token weight-streaming argument stops dominating.

**Follow-ups:** At what batch size does this become compute-bound, roughly? How does the picture change on a Blackwell-class part with FP4 support?

</details>

### 2. Size the KV cache for a 70B-class model and explain how paged KV cache management works and why it exists.

<details><summary><b>Answer</b></summary>

KV cache per token = 2 (K and V) × n_layers × n_kv_heads × head_dim × bytes_per_element. For a Llama-70B-shaped model with GQA (80 layers, 8 KV heads, head dim 128) at FP16: 2 × 80 × 8 × 128 × 2 B ≈ 320 KB per token. A 4K-token sequence is ~1.3 GB; 32 concurrent 4K sequences is ~42 GB - the KV cache, not the weights, becomes the capacity limit on batch size. (Note GQA already saved 8× vs full MHA; without it this would be unservable.)

Naive allocators reserve max-context-length contiguous buffers per request, wasting memory on fragmentation and unused headroom - most of a reservation is dead if the sequence ends early. Paged KV cache (vLLM's PagedAttention; TensorRT-LLM has an equivalent) borrows virtual memory design: KV storage is split into fixed-size blocks (e.g., a few tokens each), sequences hold block tables mapping logical to physical blocks, and attention kernels gather through the indirection. Benefits: near-zero fragmentation, allocation on demand, and copy-on-write sharing of common prefixes (system prompts, beam search) via reference counts.

Levers to shrink it further: FP8 KV cache (halves it, usually negligible quality loss), sliding-window or hybrid attention layers, and prefix caching across requests.

**Follow-ups:** What does the block-table indirection cost in the attention kernel? When would you evict vs offload KV blocks to host memory?

</details>

### 3. What does TensorRT / TensorRT-LLM actually do to a model to make it faster - and when will it *not* help?

<details><summary><b>Answer</b></summary>

Three core mechanisms. First, **graph and kernel fusion**: fusing patterns like GEMM + bias + activation into single kernels, and in TRT-LLM, fused multi-head attention kernels - this cuts kernel-launch overhead and, more importantly, avoids round-trips of intermediate tensors through HBM. Second, **precision optimization**: running layers in FP8/INT8/INT4 with calibration or pre-quantized checkpoints, using tensor cores at lower precision for 2-4× GEMM throughput and proportionally less weight traffic. Third, **kernel auto-tuning**: for each op, shape, and target GPU, selecting the best implementation ("tactic") from a library, so the engine is specialised to your hardware and shapes.

TensorRT-LLM adds LLM-serving machinery on top: in-flight (continuous) batching, paged KV cache, speculative decoding support, and tensor/pipeline parallelism - arguably these scheduler-level features matter more for LLM throughput than kernel selection does.

When it won't help: (1) batch-1 decode that's already bandwidth-bound streaming weights - fusion trims overhead but the ceiling is HBM bandwidth, so quantization is the lever, not compilation; (2) highly dynamic shapes or control flow that defeat shape-specialised engines; (3) models dominated by unsupported ops that fall back to unfused implementations; (4) workloads where the bottleneck is elsewhere - tokenization, retrieval, network. Profile before compiling.

**Follow-ups:** How would you verify a fused engine is numerically equivalent enough to the source model? What's your process when a TRT engine is *slower* than the PyTorch baseline?

</details>

### 4. Compare FP8, INT8, and INT4 quantization for LLM inference. How do you decide, and how do you validate?

<details><summary><b>Answer</b></summary>

Decide by bottleneck and hardware. **FP8 (E4M3)** on Hopper/Blackwell tensor cores quantizes both weights and activations: ~2× GEMM throughput vs FP16, halved weight traffic, and accuracy loss that's usually negligible for inference - the default when the hardware supports it, especially for compute-bound prefill and large-batch serving. **INT8 weight+activation** is the older path; activation outliers in LLMs make naive INT8 activations lossy, hence techniques like SmoothQuant that migrate outlier scale from activations into weights before calibration. **INT4 weight-only** (AWQ/GPTQ-style) targets the memory-bound decode regime: weights are stored 4-bit and dequantized on the fly into higher-precision math. You keep activation fidelity, cut weight bytes 4× vs FP16 - directly multiplying the bandwidth-bound tokens/sec ceiling - at the cost of dequant overhead and growing accuracy risk, which worsens for smaller models and harder tasks.

Validation is the senior half of the answer: perplexity deltas are necessary but insufficient - quantization damage concentrates in specific capabilities (math, code, long-context recall, instruction following). Run your actual task evals against the FP16 baseline, check per-layer error to find sensitive layers (first/last layers and attention projections often stay in higher precision), and A/B on live-ish traffic before full rollout.

**Follow-ups:** Why is the KV cache often quantized separately from weights? When would you accept quantization-aware training cost over post-training quantization?

</details>

### 5. Explain continuous (in-flight) batching. Why does it beat static batching, and what new problems does it create?

<details><summary><b>Answer</b></summary>

Static batching forms a batch of requests, runs it to completion, then starts the next. Two failure modes: head-of-line blocking - the batch finishes when its *longest* sequence finishes, so short requests wait on long ones and finished slots sit idle - and poor utilisation between batches while requests queue.

Continuous batching schedules at iteration granularity: after every decode step, finished sequences exit the batch and queued requests are injected, so the GPU runs a full batch nearly every step. This is the single biggest serving-throughput win of the vLLM/TensorRT-LLM generation - typical public numbers are 2-3× throughput over static batching, with better p99 latency because no request waits for a stranger's completion.

New problems: **prefill/decode interference.** Injecting a new request means running its prefill (long, compute-bound) alongside other requests' decode steps (short, bandwidth-bound), causing latency spikes for in-flight decodes. Mitigations: chunked prefill (split prefill into pieces interleaved with decode steps, smoothing token-level latency at a small throughput cost) or disaggregated serving (separate prefill and decode GPU pools, shipping KV cache between them - better SLO isolation, at the cost of KV-transfer bandwidth and more moving parts). Also: scheduling policy now matters (fairness vs throughput vs SLO-aware admission), and KV-cache capacity, not compute, usually caps the effective batch - which loops back to paged KV and FP8 KV cache.

**Follow-ups:** How would you set the chunked-prefill chunk size? What metrics would tell you decode steps are being starved?

</details>

### 6. Here's a CUDA kernel that's 10× slower than expected. Without running it, what are the usual suspects, and how do you confirm each?

<details><summary><b>Answer</b></summary>

Read for the big four, in order of likelihood:

1. **Uncoalesced global memory access.** Threads in a warp should hit consecutive addresses so loads collapse into few memory transactions. Column-major traversal of a row-major array, or an access pattern like `data[threadIdx.x * stride]` with large stride, multiplies the number of sectors fetched per warp. Confirm in Nsight Compute: low global load efficiency / high sectors-per-request.
2. **Shared memory bank conflicts.** Shared memory has 32 banks; threads in a warp hitting different addresses in the same bank serialize. Classic case: transposing tiles with a `tile[32][32]` array - same-column accesses all land in one bank. Fix: pad to `[32][33]`. Confirm: bank-conflict counters in the profiler.
3. **Warp divergence.** A data-dependent branch within a warp executes both paths serially with masked lanes. Fine for rare branches; fatal in inner loops. Confirm: branch efficiency metrics; fix by restructuring so a warp takes a uniform path (sort/partition work, predication).
4. **Occupancy/launch issues.** Too many registers or too much shared memory per block limits resident warps, so the SM can't hide memory latency; or the grid is simply too small to fill the GPU. Confirm: occupancy analysis, and check achieved vs theoretical occupancy.

Then the meta-answer interviewers want: don't guess - Nsight Compute's speed-of-light section tells you immediately whether you're memory-bound or compute-bound, and everything above falls out of the metrics.

**Follow-ups:** The profiler says 85% memory throughput and 20% compute - what class of fixes remains? When does *lowering* occupancy improve performance?

</details>

### 7. When is a workload compute-bound vs memory-bound on a GPU? Do the roofline math for transformer prefill vs decode.

<details><summary><b>Answer</b></summary>

The roofline model: a kernel's attainable throughput is min(peak FLOPs, arithmetic intensity × memory bandwidth), where arithmetic intensity (AI) = FLOPs per byte moved from HBM. The crossover ("ridge point") is peak FLOPs / bandwidth. For an H100-class GPU - roughly 1 PFLOP/s dense FP16 and ~3.3 TB/s - the ridge is ~300 FLOPs/byte. Below that, more FLOPs are free; above it, more bandwidth is free.

**Decode (batch 1):** each layer does matrix-vector products - every weight byte is read once and used for ~one multiply-accumulate per token. AI ≈ 2 FLOPs/byte (at FP16). Two orders of magnitude below the ridge: hopelessly memory-bound. This single number explains most of LLM inference engineering - quantization (fewer bytes), batching (reuse bytes across requests), and speculative decoding (more tokens per weight-pass) are all attacks on decode's AI.

**Prefill:** processing a prompt of length S is matrix-matrix work - weights are reused across all S tokens, so AI scales with S (until caches/tiling limits). A few hundred tokens of prefill already pushes GEMMs past the ridge into compute-bound territory. That's why prefill saturates tensor cores while decode idles them, why time-to-first-token and time-per-output-token have different optimization playbooks, and why disaggregating prefill/decode onto different hardware pools can make sense.

Batched decode sits in between: batch B multiplies decode's AI by ~B, and the ridge math predicts the batch size where you flip regimes.

**Follow-ups:** Where does attention (as opposed to the MLP GEMMs) sit on the roofline as context grows? How does FP8 move the ridge point?

</details>

### 8. Design the parallelism strategy for serving a 405B-parameter dense model. TP, PP, EP - what goes where and why?

<details><summary><b>Answer</b></summary>

Start with memory: 405B at FP16 is ~810 GB; FP8 is ~405 GB. An 8-GPU HGX node (8 × 80 GB = 640 GB) fits the FP8 weights with ~200 GB left for KV cache - so the baseline answer is FP8 + tensor parallelism (TP=8) within one node.

Why TP inside the node: TP shards individual layers (attention heads, MLP columns/rows) and requires an all-reduce per transformer layer - hundreds of collectives per token. That's only viable on NVLink-class interconnect (~900 GB/s per GPU on Hopper NVSwitch); over inter-node InfiniBand, per-layer all-reduces at decode batch sizes crater latency. Rule of thumb the interviewer is listening for: TP within the NVLink domain, something coarser across nodes.

If you must span nodes (FP16, or huge KV capacity): pipeline parallelism - split layers into stages, one cross-node transfer per stage boundary instead of per layer. Costs: pipeline bubbles (mitigated by micro-batching, which serving traffic provides naturally) and higher time-to-first-token. Expert parallelism only applies to MoE models - experts shard across GPUs with all-to-all routing - not to a dense 405B, and saying so is worth points.

Close with the serving overlay: replicate the whole TP-8 unit for throughput and route requests across replicas; scale replicas, not parallelism degree, once the model fits. Bigger TP than necessary buys latency at a steep throughput-per-GPU cost.

**Follow-ups:** How does NVLink bandwidth vs InfiniBand bandwidth change if this becomes a Blackwell NVL72-class rack? What changes for a 400B MoE with ~30B active parameters?

</details>

### 9. A model runs fine in FP32 but produces garbage after conversion to FP16. Debug it.

<details><summary><b>Answer</b></summary>

First, characterise "garbage": NaNs, all-same-token loops, or subtle quality loss - they have different causes. Then bisect by layer: run FP32 and FP16 side by side on the same input and compare activations layer by layer (max abs error, cosine similarity) to find where they diverge. This turns a mystery into a specific op.

Usual suspects, because FP16's max value is 65504 and it loses precision near zero:

- **Overflow in attention logits**: QK^T products before softmax can exceed FP16 range for long contexts or unnormalized checkpoints → inf → NaN after softmax. Fix: compute softmax in FP32 (standard in fused attention kernels), check for missing 1/√d scaling.
- **Variance accumulation in LayerNorm/RMSNorm**: sums of squares over large hidden dims overflow or lose precision. Fix: accumulate in FP32.
- **Large-magnitude outlier activations** - well-documented in LLMs at scale - that FP16 clips where FP32 didn't.
- **Reductions and long dot products** accumulating error: GEMMs should accumulate in FP32 (tensor cores do this by default; hand-written kernels sometimes don't).
- **Final logits/loss in half precision**: keep the LM head output and sampling math in FP32.

The standard mixed-precision recipe encodes all this: compute-heavy GEMMs in FP16/BF16, numerically sensitive ops (softmax, norms, logits) in FP32. And mention BF16: same range as FP32 with less mantissa - if the problem is range, BF16 usually fixes it outright, which is why it became the default training dtype.

**Follow-ups:** Why did BF16 largely replace FP16 + loss scaling for training? Same symptom appears only for some prompts - what does that tell you?

</details>

### 10. Code: implement the block manager for a paged KV cache - allocate, append, free, and copy-on-write prefix sharing.

<details><summary><b>Answer</b></summary>

The core is a free list of fixed-size blocks, per-sequence block tables, and reference counts for sharing:

```python
class BlockManager:
    def __init__(self, num_blocks: int, block_size: int):
        self.block_size = block_size
        self.free = list(range(num_blocks))
        self.refs = [0] * num_blocks
        self.tables = {}        # seq_id -> list[block_id]
        self.lengths = {}       # seq_id -> tokens written

    def _alloc(self) -> int:
        if not self.free:
            raise MemoryError("KV cache exhausted")  # caller preempts/queues
        b = self.free.pop()
        self.refs[b] = 1
        return b

    def append_token(self, seq_id: int):
        table = self.tables.setdefault(seq_id, [])
        n = self.lengths.get(seq_id, 0)
        if n % self.block_size == 0:              # need a new block
            table.append(self._alloc())
        else:
            last = table[-1]
            if self.refs[last] > 1:               # shared: copy-on-write
                self.refs[last] -= 1
                new = self._alloc()
                # (kernel would copy last block's KV data here)
                table[-1] = new
        self.lengths[seq_id] = n + 1

    def fork(self, parent: int, child: int):      # share prefix
        self.tables[child] = list(self.tables[parent])
        self.lengths[child] = self.lengths[parent]
        for b in self.tables[child]:
            self.refs[b] += 1

    def free_seq(self, seq_id: int):
        for b in self.tables.pop(seq_id, []):
            self.refs[b] -= 1
            if self.refs[b] == 0:
                self.free.append(b)
        self.lengths.pop(seq_id, None)
```

Discussion points that separate levels: only the *last* block ever needs copy-on-write (earlier blocks are immutable once full); allocation failure is a scheduling event (preempt a sequence and recompute or swap its KV), not an exception to crash on; and the block table is exactly what the attention kernel consumes to gather K/V physically.

**Follow-ups:** How do you pick block size - what do 1-token vs 128-token blocks trade? How would you add prefix caching *across* requests (hash-based block reuse)?

</details>

### 11. Solutions-architect scenario: a customer's LLM chatbot on 8 GPUs is "too slow and too expensive." You have one week with them. What do you do?

<details><summary><b>Answer</b></summary>

Resist prescribing before measuring - the reported SA interview failure mode is jumping to "buy more GPUs" or "use our stack" without diagnosis.

Day 1-2, measure: define the SLO (time-to-first-token, tokens/sec per stream, p99), then break down request latency - client → gateway → retrieval → queue → prefill → decode. Grab GPU utilisation, achieved batch size, and cost per million tokens as the baseline. Very common findings in the field: GPUs at 15% utilisation because the serving layer is a naive framework loop with batch size 1; or latency dominated by retrieval/network, not the model.

Day 3-5, apply leverage in order of effort-to-impact: (1) proper serving engine with continuous batching and paged KV (TensorRT-LLM/vLLM-class) - often the single biggest win; (2) quantize to FP8/INT4 after task-eval validation; (3) right-size the model - if evals show a fine-tuned or distilled smaller model holds quality, that's a multiplicative cost win; (4) prefix/response caching for repeated system prompts and FAQs; (5) only then talk parallelism topology and autoscaling.

Day 5-7, prove it: re-run the same benchmark suite, present before/after on the SLO and cost per million tokens, and be honest about what didn't work and residual risks. Framing everything in the customer's metrics - dollars and SLOs, not FLOPs - is the point of the exercise.

**Follow-ups:** The customer insists quality dropped after quantization but their eval suite shows no change - what now? How do you handle it when the honest answer is "your workload doesn't need our biggest GPU"?

</details>

### 12. Explain speculative decoding. Why does it speed decode up, when does it not, and how is output quality preserved?

<details><summary><b>Answer</b></summary>

Decode is memory-bound: each target-model forward pass streams all weights to emit one token. Speculative decoding exploits the idle compute: a cheap draft model (or auxiliary heads) proposes k tokens autoregressively, then the target model verifies all k in a *single* forward pass - verification of k tokens costs roughly the same as generating one, because the weight streaming dominates and the extra tokens ride along like a small batch.

Quality is preserved exactly, not approximately: the rejection-sampling scheme accepts draft token t with probability min(1, p_target(t)/p_draft(t)); on rejection it resamples from the residual distribution. The output distribution is provably identical to sampling the target model alone - this is the key point candidates miss. Expected speedup ≈ (average accepted tokens + 1) per target pass, so it lives or dies on draft/target agreement.

When it doesn't help: (1) high-entropy generation (creative sampling at high temperature) - acceptance rates drop; (2) large-batch serving - the GPU is already compute-bound, so there's no idle compute to spend on verification, and speculation can *reduce* throughput; (3) a draft model that's slow relative to the target or poorly distribution-matched. It shines for latency-sensitive, small-batch, greedy-ish workloads - chat and code completion.

Variants worth naming: self-speculation via extra decoding heads (Medusa/EAGLE-style), and n-gram/prompt-lookup drafting for tasks that copy from context (RAG, editing), which needs no draft model at all.

**Follow-ups:** How do you choose k, and what happens to acceptance as k grows? How does speculation interact with continuous batching in a real serving engine?

</details>

## How to prepare

Repo topics, in priority order for NVIDIA specifically:

- **[08-inference-and-production](../08-inference-and-production/)** - this is the loop. Quantization, KV cache, batching, speculative decoding, serving engines: go deepest here, and be able to do the bandwidth/roofline arithmetic (questions 1, 2, 7 above) without notes.
- **[11-ai-system-design](../11-ai-system-design/)** - senior loops include design rounds, and NVIDIA's flavour is infrastructure-shaped: cost, throughput, SLOs, parallelism topology. Closest case study to their product surface: [Enterprise RAG Assistant](../11-ai-system-design/case-studies/01-enterprise-rag-assistant.md) - enterprise RAG on self-hosted inference is literally what NVIDIA's NIM/blueprint stack targets, and the SA loop's architecture conversations live here.
- **[02-llm-fundamentals](../02-llm-fundamentals/)** - attention, GQA/MQA, positional encodings, sampling: needed as the substrate for every inference-optimization question.
- **[01-ml-and-dl-foundations](../01-ml-and-dl-foundations/)** - numerics (FP16/BF16/FP8), normalization, backprop mechanics; the FP16-debugging class of question draws on this.
- **[12-coding-challenges](../12-coding-challenges/)** - coding rounds are real; practise medium DS&A plus systems-flavoured problems (allocators, caches, schedulers). If a role lists C++, expect to be tested in it - Python-only prep undershoots NVIDIA more than any other company in this guide set.
- **[04-rag-and-retrieval](../04-rag-and-retrieval/)** and **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - mainly for Solutions Architect / Generative AI roles, where customer architectures are RAG- and agent-shaped.

Company-specific moves:

1. **Read the NVIDIA Technical Blog** ([developer.nvidia.com/blog](https://developer.nvidia.com/blog/)) - the TensorRT-LLM, Triton, and NIM posts are effectively the interview syllabus for inference roles, written by the teams that interview you.
2. **Run the stack yourself.** Quantize and serve a Llama-class model with [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) (or vLLM for contrast) on any cloud GPU: build an engine, enable in-flight batching, measure tokens/sec at several batch sizes. "I benchmarked it" beats "I read about it" in every domain round.
3. **Learn one GPU generation's numbers cold.** Pick H100 (or Blackwell): memory capacity, HBM bandwidth, FP16/FP8 tensor-core throughput, NVLink bandwidth - from the public architecture whitepapers. Most performance-math questions are unanswerable without these anchors, and knowing them signals you live in this world.
4. **Refresh C++ and read some CUDA.** Even a weekend with a matrix-multiply kernel tutorial (tiling, shared memory, coalescing) covers the CUDA-literacy bar for most AI-application roles; DevTech/kernel roles need far more.
5. **Watch GTC talks for your target team** - sessions are public and show you exactly what the team ships and how they talk about tradeoffs; useful both for the domain round and for a credible "why NVIDIA."

Compensation: no numbers here - see [levels.fyi](https://www.levels.fyi/companies/nvidia) for current data.

## Sources

- [Exponent - Get a Job at NVIDIA: Interview Process and Top Questions](https://www.tryexponent.com/blog/nvidia-interview-process) - loop stages, HackerRank screen format, final-round structure, core values
- [Final Round AI - NVIDIA Interview Process 2026](https://www.finalroundai.com/blog/nvidia-interview-process) - timelines, AI/ML-specific focus areas (quantization, CUDA, distributed training), resume-screen priorities
- [IGotAnOffer - NVIDIA Interview Process & Timeline](https://igotanoffer.com/en/advice/nvidia-interview-process) - six-step process overview, C++ emphasis (surfaced via search; page fetch blocked, claims cross-checked against other sources)
- [Glassdoor - NVIDIA Senior Solutions Architect interview reports](https://www.glassdoor.com/Interview/NVIDIA-Senior-Solutions-Architect-Interview-Questions-EI_IE7633.0,6_KO7,33.htm) - SA loop shape (panel + multiple technical rounds, LLM deployment topics)
- [NVIDIA Careers](https://jobs.nvidia.com/) - role titles and job-description requirements (TensorRT, PyTorch, CUDA, Triton)
- [NVIDIA Technical Blog](https://developer.nvidia.com/blog/) - TensorRT-LLM, Triton, and NIM engineering posts underpinning the domain-focus claims
- [TensorRT-LLM on GitHub](https://github.com/NVIDIA/TensorRT-LLM) - in-flight batching, paged KV cache, quantization feature set
- [levels.fyi - NVIDIA](https://www.levels.fyi/companies/nvidia) - compensation data
