# 🌑 Moonshot AI - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, technical reports, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- **Public detail on Moonshot's interview loop is thin**, and several third-party aggregators conflate this Beijing lab with unrelated companies also called "Moonshot". Treat the loop table below as the *typical frontier-lab-startup shape*, clearly labelled as inference, not a confirmed script.
- What is *not* thin is their published technical identity: long-context modelling, KV-cache-centric serving (Mooncake), reinforcement learning for reasoning (Kimi K1.5), and a trillion-parameter open-weight MoE (Kimi K2). Expect the technical bar to be set by that body of work.
- The signal they weight most heavily is **depth on long-context economics**: why the KV cache, not FLOPs, is the wall at 128K-2M tokens, and how you serve it without going bankrupt. This is their founding thesis, not a niche.
- Strong candidates can move between **architecture** (MLA, MoE routing, MuonClip stability), **systems** (prefill/decode disaggregation, prefix-cache reuse, expert parallelism), and **post-training** (long-context RL, agentic tool-use, evaluation). Single-lane specialists read as weaker for a lean lab.
- Come with a view on the **long-context-vs-RAG** question and on **why open-weight**. Their product and strategy both take a side; a substantive opinion beats a neutral one.

## Company context

Moonshot AI (月之暗面, "the dark side of the moon") is a Beijing frontier lab founded in March 2023 by Yang Zhilin, Zhou Xinyu, and Wu Yuxin, all Tsinghua graduates; Yang is a co-author of the Transformer-XL and XLNet papers, and long-context modelling is the company's founding bet. Its assistant, Kimi, launched in October 2023 marketed on handling very long inputs (initially around 200,000 Chinese characters, later extended substantially), and the company has since shipped the Kimi K1.5 reasoning model and the open-weight Kimi K2, a trillion-parameter Mixture-of-Experts model aimed at agentic and coding workloads. "AI engineer" here spans a narrow, high-density org: research engineers close to training runs, inference engineers who built and open-sourced the Mooncake serving stack, and post-training people working on RL and tool-use. Teams are small relative to US labs, so ownership runs wide.

## Roles & titles they hire

Moonshot recruits through its own careers site (careers.kimi.com) rather than the large Western job boards, and most listings are in Chinese for Beijing-based roles. The archetypes below are typical for a frontier LLM lab of this size and match the skill areas their public work implies; treat the exact titles as illustrative rather than quoted.

- **LLM Research / Research Scientist** - pre-training, post-training (RL, alignment), long-context and reasoning research; strong publication or open-source record expected
- **Research Engineer / Machine Learning Engineer** - large-scale training systems, data pipelines, distributed training for MoE at scale
- **Inference / Systems Engineer** - serving infrastructure, KV-cache management, the Mooncake stack, GPU efficiency
- **Agent / Post-training Engineer** - tool-use, agentic capability, RLHF/RLVR data and reward pipelines
- **Product / Applied Engineer** - Kimi assistant, API platform, developer-facing surfaces
- Plus conventional infrastructure, data, and full-stack software roles

Most engineering roles are Beijing-based; the company has periodically recruited overseas researchers as well.

## The interview loop

**Public, verifiable detail on Moonshot's specific loop is limited.** Their own careers portal does not publish a process description, and the aggregator reviews that surface under "Moonshot" searches appear to mix in unrelated companies (an eCommerce "Moonshot AI" and Google's X "moonshot factory"), so I will not present those as this company's process. The table below is the **typical loop for a competitive Chinese frontier lab hiring for a small, senior research/engineering pool**, presented as an inferred map. Verify every stage with your recruiter.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter / HR screen | ~30 min (inferred) | Background, motivation, why Moonshot/Kimi specifically, level fit |
| Technical phone screen | 1 round, coding + ML fundamentals (inferred) | Python coding, attention/transformer basics, ability to reason about tradeoffs |
| Deep technical round(s) | 2-4 rounds (inferred, varies by track) | Track-specific: architecture depth (attention/MoE), systems (inference/serving), or post-training (RL/agents); often a paper or project deep-dive |
| Coding / implementation | Live or take-home (inferred) | Clean Python, from-scratch implementation of a model component or a systems primitive |
| System design | 1 round (inferred) | LLM serving at scale, long-context KV-cache design, training-cluster or data-pipeline design |
| Team / hiring-manager & culture | 1-2 rounds (inferred) | Ownership, research taste, collaboration in a lean high-density team, AGI conviction |

For senior research hires, expect the balance to tilt toward research taste and a substantive discussion of your own work rather than algorithmic puzzles. For engineering hires, expect more emphasis on implementation and systems.

## What they emphasise

- **Long-context as a first-class problem, not a spec-sheet number.** Their thesis is that lossless long context underpins personalised, agentic products. Expect to be pushed past "we support 128K" into how you keep it accurate, fast, and affordable.
- **KV-cache and serving economics.** The Mooncake work (open-sourced, and the subject of an award-winning systems paper) makes disaggregated prefill/decode, cache reuse, and SLO-aware scheduling core company knowledge, not infra trivia.
- **MoE at trillion-parameter scale.** Kimi K2 is a 1T-parameter, 32B-active MoE. Routing, load balancing, expert parallelism, and training stability (the MuonClip/QK-Clip work) are live topics.
- **Post-training for reasoning and agents.** Kimi K1.5 scaled RL for long chain-of-thought; K2 targets agentic tool-use and coding. Understand RLHF/RLVR, long-context RL, and reward design, not just supervised fine-tuning.
- **Evaluation of hard-to-measure capabilities.** Long-context recall and multi-step agentic tasks are notoriously easy to fake with weak benchmarks; a credible view on rigorous evaluation stands out.
- **Open-weight conviction and efficiency.** They ship weights and technical reports; being fluent in their published methods (and having an opinion on the open-weight strategy) signals genuine interest.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Kimi's headline feature is very long context. When you push context from 8K to hundreds of thousands of tokens, what actually breaks first, and why?

<details><summary><b>Answer</b></summary>

Three walls, hit in roughly this order. **Attention compute** is O(n^2) in sequence length, so prefilling a long prompt gets quadratically expensive - this dominates time-to-first-token for long inputs. **KV-cache memory** is the harder wall: cache size grows linearly with context and with batch size, and for long contexts it dwarfs the model weights, capping how many concurrent sequences a GPU can hold. **Quality/recall** breaks more subtly: a model trained mostly on short sequences degrades at using information far back in the context (the "lost in the middle" effect), and positional encodings trained at one length extrapolate poorly to much longer ones.

The reason serving people obsess over the second wall: decode is memory-bandwidth-bound, and every generated token reads the entire KV cache. So long context taxes you twice, once in prefill compute and once in per-step decode bandwidth. Mitigations map to each wall: attention variants that shrink the cache (MLA, GQA), cache-aware scheduling and reuse (Mooncake-style disaggregation and prefix caching), and training/positional techniques (RoPE scaling, long-context continued pre-training, RL at long context) for the quality wall.

The answer interviewers want is that "long context" is not one problem but a compute problem, a memory problem, and a quality problem, each with different fixes, and that at Moonshot's scale the memory problem is usually the binding constraint.

**Follow-ups:** Which of these does a bigger batch make worse, and which does it make better? Why does context length turn into a memory question before it turns into a compute question during decode?

</details>

### 2. Kimi K2 uses Multi-head Latent Attention (MLA). Explain what it does and how it compares to GQA for KV-cache reduction.

<details><summary><b>Answer</b></summary>

MLA reduces the KV cache by storing a **low-rank latent** per token instead of full per-head keys and values. Rather than caching K and V for every head (MHA) or for a smaller set of shared KV heads (GQA), MLA projects the hidden state down into a compact latent vector, caches that, and reconstructs the per-head keys and values on the fly via up-projection matrices during attention. The cache stores the latent (plus a small decoupled component carrying the RoPE positional part), so per-token cache cost drops sharply while each query head still gets its own effective key/value.

Versus GQA: GQA reduces the cache by *sharing* KV heads across groups of query heads, a coarse knob (fewer KV heads = smaller cache, less expressive). MLA reduces it by *compression* into a shared latent, which can hit a similar or better memory footprint while preserving more head-specific expressiveness, because the per-head projections are learned rather than shared verbatim. The cost is extra matrix multiplies to compress and decompress, and a more intricate implementation, particularly the handling of RoPE, which does not commute cleanly with the low-rank decomposition and needs a decoupled positional pathway.

Why this matters at Moonshot specifically: a smaller KV cache is exactly what makes very long context and high-concurrency serving affordable, which is the whole product thesis. MLA trades a bit of compute and complexity for the memory that is the actual binding constraint.

**Follow-ups:** Why does RoPE complicate the low-rank factorisation, and how is that usually resolved? In what regime would plain GQA still be the pragmatic choice over MLA?

</details>

### 3. Walk me through why you would disaggregate prefill and decode onto separate machines, as Mooncake does. What does that buy you and what does it cost?

<details><summary><b>Answer</b></summary>

Prefill and decode have opposite hardware profiles. **Prefill** processes the whole prompt in parallel: it is compute-bound, benefits from large matmuls, and runs once per request. **Decode** generates one token at a time: it is memory-bandwidth-bound (each step reads the full KV cache), latency-sensitive, and runs hundreds of times per request. Run them on the same instance and they interfere: a big prefill stalls ongoing decodes, inflating inter-token latency, while decode's bursty small ops leave prefill's compute underused.

Disaggregation puts them on separate pools optimised independently. Prefill instances build the KV cache and hand it off; decode instances stream tokens. You can scale the two pools to the actual traffic mix, tune batching differently for each, and stop prefill spikes from wrecking decode tail latency. Mooncake goes further and makes the whole architecture **KV-cache-centric**: it pools underused CPU DRAM and SSD across the cluster into a distributed cache, so previously computed KV (for example shared prefixes) can be reused instead of recomputed, and a cache-aware scheduler places requests to maximise reuse while meeting latency SLOs. Publicly they report large throughput gains under SLO constraints and serving on the order of 100 billion tokens a day.

The cost is real: you must **transfer the KV cache** from prefill to decode nodes, which needs fast interconnect and careful overlap or it becomes the new bottleneck; the system is more complex to operate; and the cache tier adds consistency and eviction problems. It pays off at scale and with high prefix-sharing (chatbots, long shared system prompts, agents), and is overkill for a small single-node deployment.

**Follow-ups:** What determines whether the KV-cache transfer becomes the bottleneck? How does a shared multi-thousand-token system prompt change the economics in favour of a cache-centric design?

</details>

### 4. A chat assistant re-sends a long conversation history on every turn. How do you avoid recomputing all of it, and what are the pitfalls?

<details><summary><b>Answer</b></summary>

Use **prefix caching**: the KV cache for a token depends only on the tokens before it, so if a new request shares a prefix with something already computed (the conversation so far, or a shared system prompt), you can reuse those cached K/V entries and only prefill the new suffix. For a multi-turn chat this turns each turn's prefill from "reprocess the whole history" into "process just the new user message", which is a large saving on both latency and compute. Systems implement this with block-level cache indexing (paged attention style), often hashing token blocks so identical prefixes across different requests hit the same cache, and Mooncake extends reuse across a distributed cache tier rather than just within one GPU.

Pitfalls. **Exact-match only:** reuse is valid only where the token sequence (and positions) match exactly; a single differing token earlier invalidates everything after it, so injecting per-request data high up in the prompt destroys reuse. Put stable content (system prompt, retrieved docs, history) first and volatile content last. **Positional consistency:** the reused blocks must keep their original positions; RoPE means you cannot silently renumber them. **Eviction and memory pressure:** cache is finite, so you need an eviction policy (LRU-ish, or SLO-aware) and must accept cache misses gracefully. **Security/isolation:** cross-request prefix sharing must never leak one user's content into another's - sharing is safe for identical public prefixes (system prompts), risky for private data unless scoped per tenant.

The design lesson interviewers listen for: prompt *layout* is a performance decision, not just a prompting one.

**Follow-ups:** Where in the prompt do you place retrieved RAG documents if you want both good grounding and cache reuse? How would you measure cache hit rate and what would a low hit rate tell you?

</details>

### 5. Training a trillion-parameter model, attention logits can blow up and destabilise the run. What is going on, and how does something like MuonClip address it?

<details><summary><b>Answer</b></summary>

At very large scale, a recurring instability is **attention-logit growth**: the dot products between queries and keys drift to large magnitudes during training, the softmax saturates, gradients get spiky, and you see loss spikes or divergence. It is aggravated by aggressive optimisers that move weights fast. Moonshot's public work pairs the **Muon** optimiser (which orthogonalises the momentum update for 2D weight matrices, roughly equalising update magnitudes across directions and giving strong compute efficiency) with a stabiliser they call **MuonClip**, whose key piece is **QK-Clip**: after the update, it rescales/clips the query and key projection weights so the attention logits stay bounded, directly targeting the mechanism that blows up rather than just lowering the global learning rate.

Why not just cut the learning rate or add more warmup? Because that throws away the efficiency you adopted Muon for, and it treats a targeted failure with a blunt global tool. Clipping specifically the QK projections keeps the rest of training fast while capping the one quantity that diverges. Publicly they report training K2 on the order of 15.5 trillion tokens without the loss spikes that would otherwise force restarts, which at trillion-parameter scale is a large cost saving (every restart burns enormous compute).

The general principle worth stating: large-scale training stability is usually about identifying the specific quantity that diverges (attention logits, activation norms, gradient norms) and constraining *that*, rather than globally throttling learning. QK-Clip is a clean example of a targeted fix.

**Follow-ups:** Why do orthogonalised updates help efficiency but potentially worsen this particular instability? What would you monitor during a run to catch logit growth before it becomes a loss spike?

</details>

### 6. Kimi K2 is a 1T-parameter MoE with about 32B active per token and hundreds of experts. Explain the routing and the systems cost of training it.

<details><summary><b>Answer</b></summary>

Architecturally, most FFN blocks are replaced by many expert FFNs (K2 has hundreds, publicly reported as 384, with a small number, 8, activated per token plus a shared expert) and a router. For each token the router scores experts, selects the top-k, and the block output is the weighted sum of those experts. Total parameters are ~1T because you store every expert; active parameters are ~32B because each token runs only a few, so per-token FLOPs resemble a far smaller dense model while quality benefits from the large parameter pool. The asymmetry to name: **FLOPs scale with active params, memory scales with total params** - you must hold all experts in VRAM.

Training costs beyond a dense model of equal *active* size:

- **Load balancing.** Left alone, routers collapse onto a few popular experts; you add an auxiliary balancing loss (or a bias/aux-free scheme) so utilisation stays even, which matters both for model quality and for keeping every device busy.
- **Expert parallelism and all-to-all.** Experts are sharded across devices, so tokens must be shipped to whichever device holds their chosen expert and the results shipped back, an all-to-all communication pattern every layer. This is often the throughput bottleneck and is sensitive to network topology and to imbalance (a hot expert creates a straggler).
- **Routing instability.** Top-k selection is discrete; gradients flow only through chosen experts, and routing decisions can oscillate early in training.

Add the general trillion-scale stability work (see the MuonClip discussion) and you have why MoE at this scale is as much a systems problem as a modelling one.

**Follow-ups:** Why does expert imbalance hurt more during training than during single-request inference? How does a shared (always-on) expert change the routing dynamics?

</details>

### 7. Kimi K1.5 scaled reinforcement learning for reasoning without a process reward model or tree search. Why might you deliberately keep the RL recipe that simple?

<details><summary><b>Answer</b></summary>

Because the complex machinery is expensive, brittle, and often unnecessary if you get the fundamentals right. Moonshot's public K1.5 work argues that **long-context RL plus a solid policy-optimisation setup** is enough to reach strong long chain-of-thought reasoning, without Monte Carlo tree search, learned value functions, or a process reward model (PRM). Each of those adds cost and failure modes: PRMs need step-level labels and can be reward-hacked; tree search multiplies inference cost per training example; value functions add another network to train and stabilise.

The lever they lean on instead is **context length**. Scaling the RL context to long sequences (reported at 128K) lets the model actually do long, exploratory reasoning within a single rollout, so the "search" happens in-context rather than via an external tree. To make long rollouts affordable they use **partial rollouts**, reusing large chunks of previously generated trajectories instead of regenerating everything, which is where a lot of the compute savings come from. They also pursue **long2short**: transferring the capability learned by a long-CoT model into a model that answers more concisely, so you get the reasoning gains without paying full long-CoT token cost at serve time.

The engineering judgment being tested: prefer the simplest method that scales, and understand that with LLMs, additional context and clean reward signals frequently substitute for algorithmic complexity. Reach for PRMs or search only when you can show the simple recipe has plateaued, and know what each adds in cost and risk.

**Follow-ups:** What can go wrong with reward design when you skip a PRM and reward only final correctness? Why does long context reduce the need for explicit search at training time?

</details>

### 8. Kimi K2 targets agentic and coding tasks (for example SWE-bench-style problems). How would you evaluate whether an agentic model is actually good, beyond a single benchmark number?

<details><summary><b>Answer</b></summary>

A single pass@1 number hides almost everything that matters for agents, so evaluate at multiple levels. **End-to-end task success** on realistic tasks (does the patch make the repo's tests pass, in a sandbox, from a real issue) is the headline, but you must also measure **per-step correctness**: given the state, did the model choose the right tool and produce valid arguments? A model can pass a task by luck through a messy trajectory, or fail a good trajectory on one bad call, and only step-level eval distinguishes them. Add **cost and efficiency** (tokens and tool calls per solved task, wall-clock), because an agent that solves tasks at 10x the cost is often not shippable, and **robustness** (variance across seeds, sensitivity to prompt and tool-description changes).

Pitfalls specific to agentic and coding eval: **contamination** (the model may have seen the benchmark's repos or solutions in pre-training, inflating scores), **harness leakage** (giving the agent hints, retries, or oracle information the real setting would not have), and **reward gaming** (passing tests by hard-coding or by weakening the tests). For long-context agents, standard needle-in-a-haystack retrieval is too easy; you want tasks that require *reasoning over* dispersed information, not just locating a token. Build held-out, freshly-authored tasks to fight contamination, log full trajectories so failures are diagnosable, and report the distribution (variance, cost) not just the mean.

The signal: you treat evaluation as an adversarial engineering problem, aware that agentic benchmarks are unusually easy to fool.

**Follow-ups:** How would you detect that a high SWE-bench score is inflated by contamination? What would a good long-context agentic benchmark test that needle-in-a-haystack does not?

</details>

### 9. Implement single-step decode with a KV cache in PyTorch, for causal multi-head attention. Then say what changes for a long-context serving system.

<details><summary><b>Answer</b></summary>

The cache stores past K/V so each new token attends over history without recomputing it:

```python
import torch, torch.nn.functional as F

class KVCacheAttention:
    def __init__(self, n_heads, head_dim):
        self.n_heads, self.head_dim = n_heads, head_dim
        self.k_cache, self.v_cache = None, None  # each: B, H, T, hd

    def step(self, x, wq, wk, wv, wo):
        # x: B,1,D  -> one new token
        B, _, D = x.shape
        q = (x @ wq).view(B, 1, self.n_heads, self.head_dim).transpose(1, 2)
        k = (x @ wk).view(B, 1, self.n_heads, self.head_dim).transpose(1, 2)
        v = (x @ wv).view(B, 1, self.n_heads, self.head_dim).transpose(1, 2)
        self.k_cache = k if self.k_cache is None else torch.cat([self.k_cache, k], dim=2)
        self.v_cache = v if self.v_cache is None else torch.cat([self.v_cache, v], dim=2)
        att = (q @ self.k_cache.transpose(-2, -1)) / self.head_dim**0.5  # B,H,1,T
        out = F.softmax(att, dim=-1) @ self.v_cache                       # B,H,1,hd
        return out.transpose(1, 2).reshape(B, 1, D) @ wo
```

Points that get probed: no causal mask is needed at decode because the new query legitimately attends to all past positions; the cache grows by one position per step; RoPE would be applied to q and the new k *before* appending. What changes at serving scale: `torch.cat` reallocating every step is unacceptable, so real systems pre-allocate paged blocks (paged attention) and index into them; the cache is the dominant memory consumer, so you compress it (MLA/GQA) and reuse shared prefixes across requests; and you batch many sequences of different lengths together (continuous batching), which needs per-sequence length bookkeeping and a scheduler that admits and evicts under a memory budget.

**Follow-ups:** Why does paged allocation help fragmentation and admission control? Where would you slot in a rolling-window cache if the model used sliding-window attention?

</details>

### 10. Kimi extended usable context far beyond typical training lengths. How do you take a model trained at, say, 8K-32K and make it work at 128K or more?

<details><summary><b>Answer</b></summary>

You attack it from three sides: positional encoding, training, and evaluation. **Positional encoding** is the first blocker because RoPE frequencies trained at one length extrapolate poorly. The standard fixes rescale the rotary frequencies so trained positions cover the longer range: position interpolation (linearly compress positions into the trained range) and NTK-aware / YaRN-style scaling (adjust frequencies non-uniformly so high-frequency components, which carry local detail, are disturbed less than low-frequency ones). These let the model see long positions without the rotations flying off-distribution.

**Training** matters because rescaling alone gives mediocre quality: you do **continued pre-training on long sequences** (and long-context RL, as in K1.5) so the model actually learns to use distant context, not merely tolerate it. Data curation is real work here - you need genuinely long documents where distant tokens are relevant, not short texts concatenated, or the model never learns long-range dependencies. Efficiency tricks (document packing, careful attention masking so packed docs do not attend across boundaries) keep it affordable.

**Evaluation** is where teams fool themselves: passing needle-in-a-haystack (retrieve one planted fact) does not prove the model can *reason over* long context. You need tasks requiring aggregation across many dispersed positions and tests at the actual target length, plus a check that short-context quality did not regress.

The judgment being tested: context extension is a joint positional + data + eval problem, and the positional trick is the easy 20% of it.

**Follow-ups:** Why does high-frequency RoPE content need gentler scaling than low-frequency content? How would you construct an eval that a needle-in-a-haystack-only model would fail?

</details>

### 11. For a long-context assistant, when is a 1M-token context window the right tool, and when should you use retrieval (RAG) instead?

<details><summary><b>Answer</b></summary>

They solve overlapping but different problems, and the mature answer refuses the false binary. **Long context wins** when the relevant information is a bounded, cohesive body that benefits from the model seeing all of it at once: a single large codebase or document where cross-references matter, a long conversation, or tasks where chunking would sever dependencies retrieval cannot reassemble. It also wins on simplicity - no retrieval pipeline, no chunking or embedding-quality failure modes, no "the answer was in a chunk we did not retrieve".

**RAG wins** when the corpus is large or unbounded (millions of documents), changes frequently (you can update the store instantly instead of re-stuffing a prompt), needs citations and per-user access control, or when cost and latency matter: stuffing 1M tokens into every request is expensive on both prefill compute and KV-cache memory, and slow, whereas retrieval sends only what is relevant. At Moonshot's own scale this cost is not hypothetical - a million-token prompt is a large serving bill per call, which is precisely why the cache-centric serving work exists.

In practice they combine: retrieval to narrow a huge corpus down to a large-but-bounded relevant set, then a long context to reason over that set without aggressive chunking. The interviewer is checking that you weigh accuracy against cost and freshness rather than treating "just use long context" as a universal answer, and that you understand long context is not free - it moves cost from retrieval infrastructure to per-request compute and memory.

**Follow-ups:** How would prefix caching change the cost calculus for a long shared context reused across many queries? What retrieval failure would long context mask, and is masking it good or bad?

</details>

### 12. Why is decode latency dominated by memory bandwidth rather than compute, and what does that imply for how you optimise a serving system?

<details><summary><b>Answer</b></summary>

During autoregressive decode you generate one token at a time, so each forward pass processes a single position but must **read the entire model weights and the whole KV cache** from memory to do it. The arithmetic intensity (FLOPs per byte moved) is low: you do relatively little compute per parameter you load, so the GPU spends most of its time waiting on memory, not on the matmul units. Prefill is the opposite - it processes many tokens at once, reusing each loaded weight across the whole sequence, so it is compute-bound. This is why the same GPU can be near-idle on compute while decode is the bottleneck.

Implications for optimisation, which is really the point of the question:

- **Batch aggressively.** More concurrent sequences amortise the weight read across many tokens, raising arithmetic intensity - this is why continuous batching is the single biggest throughput lever.
- **Shrink the KV cache.** It is re-read every step, so MLA/GQA, quantised KV, and cache reuse directly cut the bytes moved per token.
- **Quantise weights.** Weight-only int4/int8 helps decode a lot (fewer bytes to read) even though it barely helps compute-bound prefill.
- **Speculative decoding.** Verify several draft tokens in one pass, so one expensive weight read produces multiple accepted tokens.
- **Disaggregate prefill and decode** (Mooncake) so the bandwidth-bound decode pool is tuned separately from the compute-bound prefill pool.

The tell of a strong candidate: they reason in bytes-moved-per-token and know which optimisations touch bandwidth versus FLOPs, rather than reaching for "use a bigger GPU".

**Follow-ups:** Why does weight-only quantization help decode far more than prefill? At what batch size does decode start to become compute-bound again?

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - the core bar. Attention variants (MHA/GQA and especially MLA), RoPE and long-context extension, MoE routing and load balancing, tokenization. Be able to implement, not just describe.
2. **[08-inference-and-production](../08-inference-and-production/)** - their differentiator. KV-cache math, paged attention, prefix caching, prefill/decode disaggregation (Mooncake), continuous batching, quantization, speculative decoding. Reason in bytes-per-token, not just FLOPs.
3. **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - post-training is central: RLHF/RLVR, long-context RL, reward design. The Kimi K1.5 report is the anchor.
4. **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - Kimi K2 targets agentic coding; understand tool-calling reliability, agent loops, and SWE-bench-style evaluation.
5. **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - long-context and agentic evaluation are easy to fake; a rigorous view stands out.
6. **[11-ai-system-design](../11-ai-system-design/)** - use the framework for "design serving for a long-context MoE" and "design a KV-cache-centric serving system". Closest existing case study: **[AI code assistant](../11-ai-system-design/case-studies/02-ai-code-assistant.md)** - Kimi K2 is explicitly an agentic coding model, so the long-context, tool-use, and low-latency serving tradeoffs in that case study map directly onto Moonshot's stack.

Company-specific moves:

- **Read the Kimi technical reports.** The Kimi K2 report (arXiv:2507.20534) for the trillion-scale MoE, MLA, and MuonClip/QK-Clip; the Kimi K1.5 report (arXiv:2501.12599) for long-context RL, partial rollouts, and long2short. Being fluent in these covers a large fraction of the likely technical depth.
- **Read the Mooncake paper** (arXiv:2407.00079) and skim the open-source repo. Prefill/decode disaggregation, the KV-cache-centric scheduler, and cache reuse are effectively company canon.
- **Use Kimi** and probe its long-context behaviour yourself; have concrete observations about where long context helps and where it strains.
- **Have a position** on long-context-vs-RAG and on the open-weight strategy. Their product and their releases both take a side, and a substantive opinion signals real interest.
- **Practise implementing** an attention/KV-cache primitive and a small MoE router in Python from scratch; from-scratch fluency reads well in a research-heavy lab.

## Sources

- [Moonshot AI - Wikipedia](https://en.wikipedia.org/wiki/Moonshot_AI) - company background, founders, timeline, model line, and business context
- [Kimi K2 GitHub repository](https://github.com/MoonshotAI/Kimi-K2) - Kimi K2 architecture specs (1T total / 32B active parameters, 384 experts, MLA, MuonClip) and agentic benchmarks
- [Kimi K2 technical report (arXiv:2507.20534)](https://arxiv.org/abs/2507.20534) - trillion-parameter MoE training, MuonClip/QK-Clip stability
- [Kimi K1.5 technical report (arXiv:2501.12599)](https://arxiv.org/abs/2501.12599) - reinforcement learning for reasoning, long-context RL, partial rollouts, long2short
- [Mooncake paper (arXiv:2407.00079)](https://arxiv.org/abs/2407.00079) - KV-cache-centric disaggregated serving architecture for Kimi
- [Mooncake open-source repository](https://github.com/kvcache-ai/Mooncake) - the serving platform for Kimi
- [Moonshot / Kimi careers portal](https://careers.kimi.com/) - official recruiting site (role listings; primarily Beijing-based, largely in Chinese)

*Note on the interview loop: Moonshot does not publish a process description, and third-party aggregators surface unrelated companies under the same name, so the loop section is presented as an inferred frontier-lab map rather than a verified sequence. Confidence in loop specifics is low; confidence in the technical focus areas is high.*
