# 🧠 Google DeepMind (and Google AI roles) - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- Two distinct loops share one brand: **DeepMind proper** (Research Engineer / Research Scientist / Software Engineer) runs a research-flavoured loop with math, ML breadth, and sometimes paper discussion; **Google AI-adjacent SWE-ML roles** run the classic Google loop (algorithmic coding × 2-3, system design, "Googleyness") plus 1-2 ML domain rounds.
- The DeepMind RE loop is famous for **breadth**: publicly reported rounds quiz across CS fundamentals, linear algebra, calculus, probability/statistics, and classical ML + RL - encyclopedic recall matters more here than at most labs.
- Expect at least one **ML coding round where you build a primitive from scratch** (attention, a loss, a sampling routine, a training loop) and where interviewers reportedly expect the code to actually run - no libraries doing the work, no AI assistance (candidate reports describe a strict no-AI-tools policy in technical rounds).
- The **algorithmic coding bar is standard Google**: LeetCode-medium/hard, clean communication, complexity analysis. Clearing coding is often gated before the ML rounds (reported, varies).
- Process is **slow and committee-driven**: recruiter → hiring manager → phone screens → 5-7 round loop → hiring committee. Public reports put end-to-end at roughly 6-10 weeks, longer for research tracks.
- **At least one round is now in person.** Google reinstated mandatory in-person interviewing for hires in 2025, a change publicly backed by Sundar Pichai and explicitly motivated by AI-assisted cheating in virtual technical rounds. Plan travel into your timeline.

## Company context

Google DeepMind is Google's consolidated frontier-AI unit - the Gemini model family, AlphaFold, AlphaGo/AlphaZero lineage, and the research behind much of Google's AI product surface. Engineers want in because it pairs frontier research with Google-scale compute (TPU fleets) and distribution through Search, Workspace, Android, and Cloud. "AI engineer" there usually means **Research Engineer** - someone who turns research ideas into fast, correct, large-scale code - while the broader Google org hires SWE-ML engineers who build ML-powered products and the serving/eval infrastructure around Gemini.

## Roles & titles they hire

Titles listed publicly on [deepmind.google/careers](https://deepmind.google/careers/) and Google's job board:

- **Research Engineer** (the core "AI engineer" role at DeepMind - bridges research and implementation; no PhD required, strong engineering + ML expected)
- **Research Scientist** (publication-driven; PhD-typical; paper-discussion rounds)
- **Software Engineer** (infrastructure, tooling, serving inside DeepMind - bar comparable to senior Google product teams)
- **Product Manager / Technical Program Manager / Program Manager** (non-IC-eng)
- On the Google side: **Software Engineer III/Senior/Staff, Machine Learning** (SWE-ML), **Machine Learning Engineer**, and AI-focused roles in Cloud AI, Search, and Labs
- **Student Researcher / internships** for early-career research tracks

Note the ladder distinction: DeepMind maintains RE and RS as separate ladders with different loops; SWE at DeepMind is closer to the standard Google SWE loop with domain depth added.

## The interview loop

Public info on the DeepMind RE loop is comparatively good (multiple detailed candidate write-ups and coaching-site guides agree on shape). Confidence: **medium-high** for structure, lower for round-by-round specifics, which vary by team and level. Since 2025, expect at least one stage to be conducted on site rather than virtually (company-wide policy, widely reported).

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter screen | 30 min call | Background, motivation, ladder/level fit ([official careers page](https://deepmind.google/careers/) describes initial interviews) |
| Hiring manager screen | 30-45 min | Project depth, team fit, research/eng orientation (reported, varies) |
| Technical phone screen(s) | 1-2 × 45-60 min, shared editor | Google-style algorithmic coding, LC medium/hard; clear communication (reported) |
| ML breadth round ("the quiz") | 1-2 back-to-back sessions, rapid-fire | CS fundamentals, linear algebra, calculus, probability/statistics, classical ML, RL basics - breadth over depth (well-documented in public candidate accounts; format may have evolved) |
| ML coding | 60 min | Implement an ML primitive from scratch (loss, attention, sampler, training loop); code expected to run (reported) |
| Systems / design round | 60 min | For RE: distributed training, eval infrastructure; for SWE: standard system design (reported, varies by track) |
| Paper discussion | 60 min | Research-scientist track mostly; sometimes RE - present a paper you know deeply, defend and extend it (reported, varies) |
| Leadership / team lead chats | 1-2 × 30-45 min | Mutual fit, project alignment, collaboration style |
| People & culture | 30-45 min | Values, "Googleyness"-equivalent, mission alignment (safety and responsibility framing is explicit on their careers page) |
| Hiring committee | Async | Packet review; reported to be slower and more research-weighted than standard Google HC |

For **Google SWE-ML** roles the loop is the standard, well-documented Google loop: 2-3 algorithmic coding rounds, 1 system design (ML design for ML-titled roles), 1 Googleyness/behavioural round, then hiring committee and team matching.

## What they emphasise

- **Breadth with real fundamentals.** The quiz-style rounds exist to filter for people who genuinely know the math and CS under the ML, not just framework APIs. Being unable to differentiate a simple expression by hand or state Bayes' rule is disqualifying in a way it isn't at product companies.
- **Code that runs, unaided.** Multiple public accounts stress from-scratch ML implementation with no autocomplete or AI tools, and reports describe DeepMind's AI-tool policy in interviews as stricter than peer labs.
- **Research taste even for engineers.** REs are expected to read papers, reason about experimental design, and push back on methodology - the hiring committee reportedly weighs research rigor for engineering roles too.
- **Scale engineering.** Distributed training (data/tensor/pipeline parallelism, TPU-mesh thinking), evaluation infrastructure, and performance work are core RE material - DeepMind's stack is publicly JAX-heavy.
- **Mission and responsibility.** The careers page leads with building AI "safely and responsibly"; culture rounds probe why you want frontier AI work and how you handle its stakes.
- **Classic Google collaboration signals** for the Google-side roles: humility, data-driven disagreement, working across teams ("Googleyness").

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. You're receiving an unbounded stream of event IDs. Return the k most frequent IDs seen so far, at any point, with bounded memory.

<details><summary><b>Answer</b></summary>

Start with the exact solution: a hashmap of counts plus a size-k min-heap keyed on count gives O(1) amortized updates and O(n log k) to maintain top-k - but the hashmap is O(distinct IDs), which violates bounded memory on an unbounded stream.

For truly bounded memory you must go approximate. Two standard options:

- **Misra-Gries (heavy hitters):** keep m counters; decrement all when a new ID arrives with no free slot. Guarantees finding all items with frequency > n/m using O(m) space; counts are underestimates by at most n/m.
- **Count-Min Sketch + heap:** a d×w array of counters with d hash functions; estimate = min over rows. Space O(d·w), overestimates only, error εn with probability 1−δ for w = ⌈e/ε⌉, d = ⌈ln(1/δ)⌉. Pair with a k-sized heap of candidates to answer top-k queries.

The interview signal is articulating the tradeoff: exact-but-unbounded vs bounded-but-approximate, and choosing based on stated constraints (skewed distributions favour sketches; adversarial streams need the formal guarantees). Mention practical details: sharding the sketch across workers is trivially mergeable (counters add), which matters in distributed settings; decay (sliding window or exponential) if "so far" becomes "recently."

**Follow-ups:** How would you merge sketches from 1,000 workers and what happens to the error bound? How do you handle a rotating window of the last hour?

</details>

### 2. Derive the gradient of cross-entropy loss with softmax inputs, and explain why we fuse them numerically.

<details><summary><b>Answer</b></summary>

With logits z, softmax p_i = e^{z_i} / Σ_j e^{z_j}, and one-hot target y, the loss is L = −Σ_i y_i log p_i. The key result: **∂L/∂z_i = p_i − y_i**.

Derivation sketch: ∂L/∂z_i = −Σ_k y_k (1/p_k) ∂p_k/∂z_i. The softmax Jacobian is ∂p_k/∂z_i = p_k(δ_{ki} − p_i). Substituting: −Σ_k y_k (δ_{ki} − p_i) = −y_i + p_i Σ_k y_k = p_i − y_i since Σ_k y_k = 1. The elegance - prediction minus target - is why softmax + CE is the canonical pairing: the gradient never saturates the way separate sigmoid+MSE gradients do, and it's linear in the error.

Numerical fusion matters for two reasons. First, computing log(softmax(z)) naively overflows: e^{z_i} for z_i ≈ 90 exceeds float32 range. The log-sum-exp trick subtracts m = max(z): log p_i = (z_i − m) − log Σ_j e^{z_j − m}, which is exact and stable. Second, computing p then log(p) loses precision when p is tiny (log of a denormal); the fused form keeps everything in log space. In bf16/fp16 training this is not optional - frameworks compute CE loss in fp32 from logits for exactly this reason, and large-vocab LMs (256k tokens) sometimes add a z-loss term to keep the log-partition function from drifting.

**Follow-ups:** What changes with label smoothing? Why can the loss for a large-vocabulary LM dominate memory, and what do fused kernels (e.g., chunked CE) do about it?

</details>

### 3. On average, how many fair coin flips until you see two heads in a row? Walk me through it.

<details><summary><b>Answer</b></summary>

Answer: **6**. Set up a Markov chain on progress states. Let E₀ = expected flips remaining with no progress, E₁ = expected flips with one trailing head.

- From S₀: flip once; heads (½) → S₁, tails (½) → S₀. So E₀ = 1 + ½E₁ + ½E₀ ⟹ E₀ = 2 + E₁.
- From S₁: flip once; heads (½) → done, tails (½) → back to S₀. So E₁ = 1 + ½·0 + ½E₀.

Substitute: E₀ = 2 + 1 + ½E₀ ⟹ ½E₀ = 3 ⟹ E₀ = 6.

The instructive contrast: expected flips to see **HT is 4**, not 6, even though both patterns have probability ¼ per two flips. Reason: after failing partway through HH (you had H, got T), you reset to zero progress; failing partway through HT (you had H, got another H) keeps you in the "have H" state. Overlapping self-structure makes HH "harder." This is the same phenomenon behind the general result that E[waiting time] = Σ over pattern self-overlaps of 2^k (Conway's leading-number trick): HH overlaps itself at lengths 1 and 2 → 2 + 4 = 6; HT only at length 2 → 4.

Interviewers use this class of question to check you reason with conditional expectation and state machines rather than pattern-matching to memorised answers - narrate the state setup explicitly.

**Follow-ups:** Expected flips for HHH? How would you estimate this by simulation and how many trials until your estimate's standard error is under 0.01?

</details>

### 4. Explain the SVD and give two places it shows up in modern deep learning.

<details><summary><b>Answer</b></summary>

Any real matrix W (m×n) factors as W = UΣVᵀ: U (m×m) and V (n×n) orthogonal, Σ diagonal with non-negative singular values σ₁ ≥ σ₂ ≥ ... The geometric read: every linear map is a rotation/reflection, an axis-aligned scaling, and another rotation. The Eckart-Young theorem says truncating to the top-r singular values gives the best rank-r approximation in Frobenius and spectral norm - this is the foundation of nearly every low-rank method.

Two concrete appearances:

1. **Low-rank adaptation (LoRA).** Fine-tuning updates ΔW empirically have low "intrinsic rank," so parameterizing ΔW = BA with B (m×r), A (r×n), r ≪ min(m,n) cuts trainable parameters by orders of magnitude (r=16 on a 4096×4096 projection: ~131k params vs 16.8M). SVD is the analysis tool that justifies this and initializes variants that decompose the pretrained weight itself.
2. **Conditioning and training stability.** The condition number σ₁/σ_min of weight matrices and of the input covariance governs gradient-descent convergence; spectral-norm monitoring detects exploding attention logits, and techniques like spectral normalization and μP-style init reason directly about singular-value scales.

Also worth naming: PCA is the SVD of the centred data matrix; pseudo-inverse solutions to least squares (V Σ⁺ Uᵀ) underlie linear-probe evaluations.

**Follow-ups:** Cost of full SVD on a 4096×4096 matrix, and what you'd use instead if you only need the top 10 singular vectors? Why is the spectral norm of a weight matrix relevant to Lipschitz bounds?

</details>

### 5. Implement multi-head self-attention from scratch - no `nn.MultiheadAttention`, and make it causal.

<details><summary><b>Answer</b></summary>

Core things to get right: the √d_k scaling, the head reshape, the causal mask applied *before* softmax, and mask value −inf (not a large negative number in fp16 - use the dtype min or −inf carefully).

```python
import torch, math

def mha(x, Wq, Wk, Wv, Wo, n_heads):
    B, T, D = x.shape
    d = D // n_heads
    def split(W):  # (B,T,D) -> (B,H,T,d)
        return (x @ W).view(B, T, n_heads, d).transpose(1, 2)
    q, k, v = split(Wq), split(Wk), split(Wv)
    att = (q @ k.transpose(-2, -1)) / math.sqrt(d)      # (B,H,T,T)
    mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
    att = att.masked_fill(mask, float("-inf"))
    att = torch.softmax(att, dim=-1)
    out = (att @ v).transpose(1, 2).reshape(B, T, D)     # concat heads
    return out @ Wo
```

Narrate the reasoning: scaling by √d_k keeps logit variance ≈1 at init so softmax isn't saturated; without it gradients vanish for large d. Multi-head is a reshape, not H separate matmuls - one fused projection then a view, O(T²·D) compute and O(H·T²) attention-matrix memory, which is the term FlashAttention eliminates by tiling and never materializing the T×T matrix. For inference, mention the KV cache: at decode step t you compute q for one token and attend over cached K,V - turning O(T²) per step into O(T).

Verify by construction: run it, check output shape, and check causality by asserting position 0's output is unchanged when you perturb position 5's input.

**Follow-ups:** Where does dropout conventionally go and why? Modify this for grouped-query attention - what changes and what does it buy at inference?

</details>

### 6. Implement nucleus (top-p) sampling. What failure mode of top-k does it fix?

<details><summary><b>Answer</b></summary>

Top-k fails because the "right" candidate-set size is context-dependent: after "The capital of France is", the distribution is peaked and k=50 admits 49 junk tokens; in open-ended prose the distribution is flat and k=50 may exclude perfectly good continuations. Nucleus sampling adapts the cutoff to the distribution's shape: keep the smallest set of tokens whose cumulative probability ≥ p.

```python
import torch

def nucleus_sample(logits, p=0.9, temperature=1.0):
    probs = torch.softmax(logits / temperature, dim=-1)
    sorted_probs, idx = torch.sort(probs, descending=True)
    cum = torch.cumsum(sorted_probs, dim=-1)
    # keep tokens until cumulative prob exceeds p; always keep the top token
    cutoff = cum - sorted_probs >= p          # True = drop
    sorted_probs[cutoff] = 0.0
    sorted_probs /= sorted_probs.sum()
    return idx[torch.multinomial(sorted_probs, 1)]
```

Details interviewers probe: the off-by-one (`cum - sorted_probs >= p` keeps the token that crosses the threshold; a naive `cum > p` can drop everything when the top token alone exceeds p), renormalization after masking, and temperature ordering (scale logits before softmax; temperature reshapes the distribution, p then truncates it). Complexity is O(V log V) for the sort; at 256k vocab this is measurable, so production samplers often do top-k pre-filter (k≈few hundred) then top-p inside it.

Also know the neighbours: min-p (threshold relative to max prob) behaves better at high temperature; greedy/beam for closed-form answers; and sampling params interact with eval reproducibility - evals should pin temperature=0 or report variance across seeds.

**Follow-ups:** Why can top-p=1.0, temperature=1.0 still produce degenerate repetition, and what mitigations exist? How do you make sampling reproducible across batch sizes on GPU?

</details>

### 7. Your pretraining loss suddenly diverges at step 300k of a long run. Diagnose and fix it.

<details><summary><b>Answer</b></summary>

Triage in order of likelihood and cost:

1. **Look at the telemetry around the spike.** Gradient-norm curve first: a spike preceding the loss jump points to an optimization event; flat grad norms with loss jump points to data or eval-side bugs. Check per-layer norms - attention-logit growth in late layers is a classic instability signature.
2. **Data.** A bad shard (corrupt encoding, adversarial document, near-duplicate flood) hitting at that step is common. Reproduce: replay the exact batch window from the data-loader checkpoint. Fix: skip the offending window, add validation on ingestion.
3. **Numerics.** fp16 without loss scaling overflows; even bf16 runs hit issues in softmax/logits at scale. Mitigations: bf16 with fp32 master weights and fp32 loss computation, z-loss on the logit partition function, QK-layernorm to bound attention logits.
4. **Optimization.** LR too high for this phase (cosine schedules can still be too hot post-warmup), Adam ε too small, β₂ too high causing stale second moments. Gradient clipping (global norm ~1.0) is the standard guardrail - check whether clipping frequency was rising before the spike.

Recovery playbook, publicly standard for large runs: roll back to the last good checkpoint, skip the suspect data window, optionally lower LR briefly, resume. The senior signal is having a *procedure* - checkpoint hygiene, deterministic data order so incidents are replayable, and dashboards that make the spike diagnosable in minutes rather than a re-run.

**Follow-ups:** Why does deterministic, resumable data ordering matter for this workflow? What would make you choose to restart the run entirely rather than roll back?

</details>

### 8. When would you choose Q-learning over policy gradients, and vice versa?

<details><summary><b>Answer</b></summary>

**Q-learning** (value-based, off-policy): learns Q(s,a) via the Bellman target r + γ max_a' Q(s',a'). Because it's off-policy, it can learn from replay buffers and stale data - high sample efficiency, which is decisive when environment interaction is expensive. Weaknesses: max over actions makes continuous action spaces awkward (you need discretization or an actor); the "deadly triad" (function approximation + bootstrapping + off-policy) can diverge; overestimation bias needs fixes like double Q-learning.

**Policy gradients** (e.g., REINFORCE → actor-critic → PPO): directly optimize E[R] via ∇J = E[∇log π(a|s)·A(s,a)]. Naturally handle continuous/stochastic actions, converge more stably (you're doing gradient ascent on the true objective, if on-policy), and the policy can be exactly the object you deploy. Weaknesses: on-policy data hunger (every update needs fresh rollouts), high gradient variance requiring baselines/advantage estimation (GAE), and sensitivity to step size - hence trust-region methods and PPO's clipping.

Rules of thumb: discrete actions + cheap simulator + need for replay → DQN-family. Continuous control or when you need a stochastic policy → actor-critic/PPO. Modern practice blends them (SAC is off-policy actor-critic with entropy regularization). Worth knowing for this company: RLHF-style LM post-training uses policy-gradient methods (PPO variants) because the "environment" step (generating text, scoring with a reward model) is expensive and the action space is the vocabulary - effectively a huge discrete space handled through the policy itself.

**Follow-ups:** What is the deadly triad, precisely, and which of the three do you give up in each family? Why does PPO clip the importance ratio instead of using a KL penalty alone?

</details>

### 9. Design the training setup for a model that doesn't fit on one accelerator - say 70B parameters on a pod of accelerators.

<details><summary><b>Answer</b></summary>

Start with the memory arithmetic. Adam mixed-precision training costs ≈16 bytes/param (2 weights + 2 grads + 4+4+4 optimizer states/master) → 70B params ≈ 1.1 TB of state before activations. No single device holds that, so you compose parallelism:

- **Data parallelism + state sharding (ZeRO/FSDP):** shard optimizer state, grads, and optionally params across the data-parallel group; all-gather params per layer on demand. Cheap to adopt, communication grows with sharding stage.
- **Tensor (model) parallelism:** split individual matmuls (column/row-parallel) across 4-8 devices with fast interconnect; requires all-reduces inside every layer, so keep it within a node/chip cluster.
- **Pipeline parallelism:** partition layers into stages across nodes; microbatching hides the bubble (bubble fraction ≈ (stages−1)/microbatches, so use ≫stages microbatches).
- **Activation checkpointing** trades ~30% recompute for activation memory.

On TPU-style hardware the framing is a device **mesh** with sharding annotations (JAX/XLA GSPMD): you declare how arrays shard over mesh axes and the compiler inserts collectives - same math, different ergonomics; DeepMind's stack is publicly JAX-based.

Then the reliability layer, which is where engineering interviews go: async checkpointing every N minutes (at this scale a preemption without checkpoints costs real money), deterministic resumable data pipelines, per-host failure detection and job restart, and throughput monitoring in MFU (model FLOPs utilization) - 40-55% MFU is a publicly typical target for dense transformer training. State your batch-size/LR scaling assumptions and how you'd validate the setup with a scaled-down proxy run before burning pod-weeks.

**Follow-ups:** Where does communication become the bottleneck as you scale data parallelism, and what does gradient accumulation change? How would you decide between wider tensor parallelism vs deeper pipeline?

</details>

### 10. Build the evaluation harness for a new frontier model release. What does it need to do?

<details><summary><b>Answer</b></summary>

Treat evals as production software, not scripts. Components:

1. **Versioned, immutable benchmark sets** - every dataset, prompt template, and scorer pinned by hash; a leaderboard number is meaningless if the prompt changed between runs.
2. **Contamination controls** - n-gram/substring overlap checks between eval sets and training data, plus held-out canary strings; report contamination status alongside scores.
3. **Deterministic decode policy** - temperature 0 for pass/fail tasks; for sampled generation, fixed seeds and multiple samples with variance reported. A 500-item eval has a 95% CI of roughly ±4 points at 50% accuracy - a 2-point "win" is noise, so paired tests (McNemar's on per-item outcomes) beat comparing headline numbers.
4. **Scorer validity** - exact-match and code-execution scorers where possible; where LLM-as-judge is unavoidable, calibrate the judge against a human-labelled slice and re-check per model family (judges drift and self-prefer).
5. **Regression gating in CI** - every candidate checkpoint runs a fast smoke suite (minutes) and nightly full suites; capability *and* safety evals (refusals, jailbreak batteries, bias probes) gate promotion.
6. **Traceability** - store raw transcripts, not just scores, so regressions are debuggable; tie every score to model hash + harness hash + data hash.

The scale problem is real: full suites across dozens of benchmarks × checkpoints is a scheduling and caching problem (dedupe identical prompt/model pairs, batch across evals, prioritise by information value). The senior signal: you talk about statistical honesty and reproducibility, not just which benchmarks to run.

**Follow-ups:** How do you detect that a benchmark has saturated or leaked, and what do you do next? How would you eval a model whose main improvement is long-context behaviour?

</details>

### 11. Design the serving system for a multimodal assistant (text + image input, streaming text out) at hundreds of millions of users.

<details><summary><b>Answer</b></summary>

Clarify SLOs first: p95 time-to-first-token (TTFT) under ~1s for interactive chat, streaming at ≥ human reading speed (~10-20 tok/s floor), regional availability, cost per query. Then the architecture:

- **Model tiering and routing.** Serve a small fast model for the bulk of traffic and route hard queries to a large model (Google publicly ships this pattern as Gemini Flash vs Pro tiers). Router can be a lightweight classifier; misroutes are a quality/cost dial.
- **Inference core.** Continuous (in-flight) batching to keep accelerators saturated; paged KV cache so long conversations don't fragment memory; prefix caching for shared system prompts (huge hit rates in assistant traffic); speculative decoding with a draft model for 2-3× decode speedup; quantized weights (int8/fp8) where quality allows.
- **Multimodal path.** Image encoder (ViT-style) runs as a separate stage - often on separate hardware - producing embeddings/tokens that join the text prompt; cache encodings for re-referenced images.
- **Disaggregated prefill/decode.** Prefill is compute-bound, decode is memory-bandwidth-bound; separating them onto different pools improves utilization and isolates TTFT from decode load.
- **Safety and product layer.** Inline safety classifiers on input and streamed output (with the ability to halt a stream), quota/abuse controls, conversation state store keyed to user, and global load balancing with regional model replicas.

Capacity math to volunteer: hundreds of millions of DAU × a few queries/day × ~1k tokens/query lands in the trillions of tokens/day - justify the tiering and caching decisions with that number.

**Follow-ups:** What breaks first as median context length grows 10×? How do you roll out a new model version safely under this traffic (shadow traffic, interleaved evals, rollback)?

</details>

### 12. Tell me about a time you disagreed with a researcher (or tech lead) about priorities, and what happened.

<details><summary><b>Answer</b></summary>

This is the culture round; at DeepMind and Google generally the evaluated axes are collaboration, intellectual humility, and data-driven disagreement ("Googleyness" on the Google side). Structure as STAR, but the content interviewers listen for:

- **You disagreed on substance, respectfully.** Example shape: a researcher wanted a bespoke experimental fork of the training stack for one paper; you believed the fork would rot and pushed for landing the feature behind a flag in mainline. Present the researcher's position as legitimate - deadline pressure before a conference is real - not as an obstacle.
- **You reduced the disagreement to evidence.** You quantified the cost (past forks took N weeks to reconcile; the flagged path added two days now) and timeboxed a spike to de-risk the mainline approach rather than debating in the abstract.
- **Clean resolution, including the case where you lost.** "Disagree and commit" is explicitly valued: if the decision went the other way, show you executed it wholeheartedly and set a checkpoint to revisit with data - not that you relitigated.
- **Relationship outcome.** The researcher-engineer partnership is the core working unit at a lab; end with how the collaboration got stronger (they brought you in earlier on the next project).

Anti-patterns: villainising the counterpart, "I was right all along" endings, escalating to management as the first move, and conflicts that are really just communication failures you didn't own. Pick a story with genuine technical stakes - evaluation validity, reproducibility, infra debt - because those map directly onto what REs at a lab negotiate weekly.

**Follow-ups:** What would have made you change your mind? Describe a time you were wrong in a technical disagreement - how did you find out?

</details>

## How to prepare

**Repo roadmap, weighted for this loop:**

- [`01-ml-and-dl-foundations`](../01-ml-and-dl-foundations/) - highest priority. The DeepMind breadth rounds live here: backprop math, optimization, regularization, probability. Go deeper on the math than for any other company in this repo.
- [`02-llm-fundamentals`](../02-llm-fundamentals/) - attention, tokenization, sampling, scaling: the raw material of the from-scratch ML coding round.
- [`08-inference-and-production`](../08-inference-and-production/) - KV cache, batching, quantization, speculative decoding for the RE systems round and any Gemini-adjacent SWE role.
- [`11-ai-system-design`](../11-ai-system-design/) - the design round; practise both training-side (distributed) and serving-side designs. Closest case study currently in this repo: [`11-ai-system-design/case-studies/05-content-moderation-pipeline.md`](../11-ai-system-design/case-studies/05-content-moderation-pipeline.md) - classifier-in-the-request-path design maps directly onto the safety-filter layer of an assistant serving stack.
- Secondary: [`07-evaluation-and-observability`](../07-evaluation-and-observability/) (eval-infra questions are increasingly common for REs) and [`05-fine-tuning-and-alignment`](../05-fine-tuning-and-alignment/) (RLHF/post-training literacy).

**Company-specific moves:**

1. **Rebuild ML primitives by hand, offline.** Attention, layernorm, Adam, CE loss, top-p sampling - in a plain editor, no autocomplete, no AI, and run them. This mirrors the reported round format exactly.
2. **Do a real math refresh.** Public candidate accounts (e.g., Aleksa Gordić's write-up) consistently cite linear algebra, calculus, and probability/statistics as make-or-break; *Mathematics for Machine Learning* (Deisenroth et al., free PDF) is the commonly cited text.
3. **Learn JAX basics.** DeepMind's research stack is publicly JAX-based; being fluent in `jit`/`vmap`/`pmap`-style thinking and the mesh/sharding mental model is a differentiator in RE systems conversations.
4. **Read DeepMind's own technical reports** - the Gemini technical reports and AlphaFold papers on [deepmind.google](https://deepmind.google/) - and have one paper (theirs or anyone's) you can present and defend for a potential paper-discussion round.
5. **Grind the classic Google bar too.** LeetCode medium/hard with spoken complexity analysis still gates the loop; don't let lab-flavoured prep crowd out plain algorithms. For the Google SWE-ML path, add one full ML system design mock. Compensation data is publicly tracked on [levels.fyi](https://www.levels.fyi/companies/google).

## Sources

- [Google DeepMind Careers (official)](https://deepmind.google/careers/) - roles and official four-stage hiring process description
- [techinterview.org - Google DeepMind Interview Process 2026](https://www.techinterview.org/post/3233474918/deepmind-interview-process-2026/) - track-by-track loop breakdown, timelines, AI-tool policy
- [Aleksa Gordić - How I Got a Job at DeepMind as a Research Engineer](https://gordicaleksa.medium.com/how-i-got-a-job-at-deepmind-as-a-research-engineer-without-a-machine-learning-degree-1a45f2a781de) - detailed first-person RE loop account (2021-era; process has evolved)
- [Omar Reid - How To Destroy the DeepMind Research Quiz (Medium/TDS)](https://medium.com/data-science/how-to-destroy-the-deepmind-research-quiz-90c9397c86db) - public description of the breadth-quiz format
- [IGotAnOffer - Google DeepMind Research Engineer Interview](https://igotanoffer.com/en/advice/google-deepmind-research-engineer-interview) - coding/ML round gating and difficulty reports
- [IGotAnOffer - Google Machine Learning Engineer Interview](https://igotanoffer.com/blogs/tech/google-machine-learning-engineer-interview) - Google-side SWE-ML loop structure
- [Glassdoor - Google DeepMind Interview Questions](https://www.glassdoor.com/Interview/Google-DeepMind-Interview-Questions-E1596815.htm) - aggregated candidate reports
- [Business Standard - Google shifts to in-person interviews amid AI cheating concerns](https://www.business-standard.com/companies/news/google-ai-cheating-job-interviews-in-person-hiring-shift-sundar-pichai-125082600492_1.html) - the 2025 in-person interviewing mandate
