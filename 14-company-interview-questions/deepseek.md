# 🐋 DeepSeek - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, technical reports, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- Public information on DeepSeek's actual interview loop is **thin**. What is reported (by third-party guides and press, not an official process page) is a short, **hardcore technical loop of roughly 3-4 rounds** weighted heavily toward research depth plus the ability to write correct, efficient code fast.
- The bar is unusual: they hire **young researchers with strong publication records and near-zero required work experience**, but reject people who can talk about their niche and nothing else. Breadth across the efficient-LLM stack is the differentiator.
- Expect architecture deep-dives on the things they invented or popularised: **Mixture-of-Experts routing, Multi-head Latent Attention (MLA), auxiliary-loss-free load balancing, multi-token prediction, GRPO for RL reasoning**, and FP8 / kernel-level training-systems efficiency.
- The separator between hire and reject is reportedly the **software-engineering dimension**: can you turn equation 7 of a paper into a correct PyTorch implementation and reason about scaling it across a GPU cluster? Publications alone do not clear the coding bar.
- Roles and teams are based in **Hangzhou and Beijing**; the company hires in Mandarin and pursues AGI openly, publishing detailed technical reports and open-weight models. Fluency in **their own papers** is the single best-calibrated prep signal.

## Company context

DeepSeek is a Chinese frontier AI lab funded by the quant hedge fund High-Flyer and led by founder Liang Wenfeng, based in Hangzhou and Beijing. It became globally known for training frontier-class models at a small fraction of the usual cost and releasing them open-weight: the DeepSeek-V2/V3 line (large Mixture-of-Experts models with MLA for KV-cache compression, auxiliary-loss-free load balancing, multi-token prediction, and FP8 training) and DeepSeek-R1 (an open-weight reasoning model trained largely with reinforcement learning, which popularised GRPO). Their public identity is **efficiency**: architecture, kernels, and training-systems choices that squeeze more out of constrained hardware. "AI engineer" here is not a product-integration role - it usually means a research scientist or a systems/infra engineer sitting directly on training runs, inference kernels, and data pipelines, expected to both invent methods and ship the code that makes them run.

## Roles & titles they hire

DeepSeek recruits primarily through its own site and Chinese job boards (Boss Zhipin), with some LinkedIn postings aimed at international Chinese talent. Reported archetypes:

- **Deep Learning Researcher (AGI)** - core model research: architecture, pretraining, post-training/RL, reasoning. Reportedly open to strong new graduates with top-venue papers.
- **AI Core Systems / Infrastructure Engineer** - distributed training frameworks, GPU kernels, communication libraries, inference systems, storage.
- **Data engineers / data researchers** - large-scale data curation, filtering, and synthetic-data pipelines.
- **Full-stack and front-end engineers** - the app, API, and product surface around the models.
- **AI product and "AI tutor" / annotation-adjacent roles**, plus internships (LLM research interns are a common entry path).
- More recent postings emphasise **agentic AI** as the company pushes past chat into tool-using systems (reported in press, 2026).

Locations cluster in Beijing and Hangzhou. Treat any single title list as approximate: they scale hiring in bursts and postings rotate.

## The interview loop

**Be honest about the evidence here: DeepSeek does not publish an interview-process page, and there are very few first-person candidate write-ups in English.** The table below is the *typical shape for a research-heavy frontier lab*, cross-referenced with third-party guides that describe a short, intense, technically deep loop. Treat every row as inference or third-party report, not official fact.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter / screen | Call (reported, varies) | Background, papers, motivation, why DeepSeek, language fit |
| Technical / research screen | Live discussion + coding (reported, varies) | Depth in your area; can you implement a method, not just cite it |
| Architecture deep-dive | Whiteboard / discussion (inferred) | MoE routing, MLA / KV-cache, sparse attention, RL for reasoning; connecting your niche to efficient-LLM at large |
| Coding round | Live PyTorch / algorithms (reported, varies) | Translate a paper's equations into correct, efficient code under time pressure; clean Python |
| Systems / ML system design | Discussion (inferred) | Low-latency inference for 100B+ param models under GPU-memory limits; training-cluster efficiency |
| Data / research judgment | Discussion (reported) | Data curation and "data chemistry": filtering synthetic data, avoiding model collapse |
| Team / founder-level conversation | Discussion (inferred) | Research taste, breadth, ability to write clearly; DeepSeek publishes detailed reports and values technical writing |

Reported total is around 3-4 technical rounds, described as demanding and efficiency-obsessed ("does your code work" is not enough; "is this the most efficient way" is the real question). Because this is under-documented, ask your recruiter exactly what each round covers and in what language.

## What they emphasise

- **Efficiency as a first principle.** Their entire public reputation is doing more with less: MLA to shrink the KV cache, FP8 to halve training memory, DualPipe to hide communication behind computation. Answers that ignore cost, memory bandwidth, and hardware read as junior.
- **Implementation, not just ideas.** The reported hire/reject line is whether you can turn a method into correct, efficient PyTorch and reason about scaling it. Publications without coding fluency reportedly fail.
- **Breadth across the LLM stack.** They want researchers who connect their specialty to the bigger picture of efficient LLM development. Being able to talk only about your narrow niche is reportedly a red flag.
- **Data judgment.** Data curation, filtering, and synthetic-data quality ("how do you avoid model collapse?") come up as a distinct competence, not an afterthought.
- **RL for reasoning.** R1 made GRPO and verifiable-reward RL a house specialty; expect to reason about reward design, why they dropped the value model, and failure modes like reward hacking and length blowup.
- **Clear technical writing.** DeepSeek ships unusually detailed, readable technical reports. The ability to explain a complex result crisply is a real signal, not a soft skill.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Explain Multi-head Latent Attention (MLA). What problem does it solve and what does it cost?

<details><summary><b>Answer</b></summary>

MLA attacks the KV-cache bottleneck. In standard multi-head attention you cache a full K and V per head per token, and at long context and large batch that cache, not the weights, becomes the memory and bandwidth ceiling on decode. MLA instead projects the input down into a single low-rank **latent vector** per token (dimension far smaller than the concatenated head dimensions) and caches only that. At attention time it up-projects the latent back into per-head K and V. So you store one small vector per token instead of full K/V for every head, which is where the large reported KV-cache reductions come from (roughly a few percent of MHA for the big MoE models), directly buying you longer context and bigger batches per GPU.

The complication is RoPE. Rotary position embedding has to be applied to K in a way that does not commute cleanly with the low-rank up-projection, so you cannot just compress the RoPE-carrying part. DeepSeek's fix is **decoupled RoPE**: split into a position-agnostic component that gets compressed into the latent, and a small position-carrying component (extra query dimensions plus a shared key) that carries RoPE separately and is concatenated in. That preserves positional sensitivity while keeping the cache small.

Costs: extra up/down projection matrices and a more intricate kernel than vanilla attention, which is exactly why they wrote and open-sourced FlashMLA to make MLA decode fast on Hopper GPUs. Naive implementations can lose the win to projection overhead.

**Follow-ups:** Why does decode become memory-bandwidth-bound rather than FLOP-bound, and how does that change your kernel priorities? How does MLA interact with tensor parallelism across the head dimension?

</details>

### 2. Walk me through DeepSeekMoE. How is it different from a standard top-2 MoE like Mixtral?

<details><summary><b>Answer</b></summary>

Two ideas: **fine-grained experts** and **shared experts**. Standard MoE (Mixtral-style) splits each FFN into a handful of full-size experts and routes each token to top-2. DeepSeekMoE instead uses many smaller experts and routes to more of them, which increases the number of possible expert *combinations* per token and lets specialisation be finer-grained without raising active parameter count. On top of that, a few experts are designated **shared** and always active for every token, so common, cross-cutting knowledge lives there and the routed experts do not each have to re-learn it, reducing redundancy.

The economics are the usual MoE trade: total parameters are huge (V3 is 671B) but active parameters per token are small (about 37B), so you pay dense-13B-class compute for a much larger knowledge capacity. Memory still scales with total parameters, so you must hold all experts in VRAM across the cluster, and training needs expert parallelism with all-to-all communication to ship tokens to the device holding their expert. That communication is a first-order cost, which is why they built DeepEP and overlapped it with compute via DualPipe.

The interview signal is that you see MoE as a systems problem, not just a modelling trick: quality-per-FLOP goes up, but you now own load balancing, all-to-all bandwidth, and expert-placement decisions that dense models never face.

**Follow-ups:** Why do fine-grained experts make load balancing harder? Where would you place shared vs routed experts across devices to minimise communication?

</details>

### 3. DeepSeek-V3 uses auxiliary-loss-free load balancing. What was wrong with the auxiliary loss, and how does the bias trick work?

<details><summary><b>Answer</b></summary>

Left alone, MoE routers collapse onto a few favourite experts: those get all the tokens and all the gradient, the rest starve, and you waste both capacity and hardware because expert-parallel devices sit idle. The classic fix is an **auxiliary load-balancing loss** that penalises uneven expert utilisation. It works, but it fights the main objective: you are adding a gradient term whose only purpose is balance, and it bleeds into the model's quality. Tuning its weight is a lose-lose - too small and you get imbalance, too large and you hurt the language-modelling loss.

DeepSeek's auxiliary-loss-free approach removes that gradient term entirely and instead keeps a **per-expert bias** added to the routing scores only for the top-k selection decision. If an expert is over-subscribed, its bias is nudged down; if under-used, nudged up. The bias is updated by a simple rule based on observed load, not by backprop, so it steers routing toward balance without contaminating the training gradient. The expert's actual output weighting still uses the unbiased affinity, so you get balance in *who is selected* without distorting *how much they contribute*.

The payoff they report is better performance and cleaner expert specialisation than the auxiliary-loss baseline, because the model is no longer paying a quality tax for balance. Naming the separation - bias affects selection, not the gate value used in the weighted sum - is the detail that shows you actually understand it.

**Follow-ups:** How would you set the bias update step size, and what happens if it is too aggressive? Does this remove the need for any balancing signal during inference?

</details>

### 4. What is multi-token prediction (MTP) and why train with it?

<details><summary><b>Answer</b></summary>

Standard language-model training predicts only the next token. MTP adds auxiliary heads (or sequential modules) that also predict the next few tokens at each position, so the training signal per step is denser: the model is pushed to plan slightly further ahead rather than being purely greedy about position t+1. DeepSeek-V3 uses this as a training objective and reports it improves quality, the intuition being that forcing the representation to be predictive of t+2, t+3 encourages it to encode more about the future trajectory, which regularises and strengthens the main next-token head.

There is a second, practical payoff at inference. The extra prediction heads give you a natural **speculative decoding** mechanism: the MTP head proposes future tokens, the main model verifies them in one pass, and accepted tokens are emitted without a full forward step each. That turns a training-time objective into a decode-time speedup, which fits DeepSeek's efficiency-everywhere pattern.

Trade-offs to name: extra parameters and compute during training for the additional heads, and the depth-vs-benefit question - predicting too far ahead adds noise for diminishing return, so the horizon is small. At inference, the speculative win depends on acceptance rate; if the draft tokens are usually rejected you have added latency, not removed it. The honest framing is that MTP is a modest, cheap training improvement that also happens to hand you a compatible draft model for free.

**Follow-ups:** How does MTP-based speculation compare to using a separate small draft model? What acceptance rate do you need for speculative decoding to be a net win?

</details>

### 5. Explain GRPO. Why did DeepSeek drop the value network that PPO uses?

<details><summary><b>Answer</b></summary>

GRPO (Group Relative Policy Optimization) is the RL algorithm behind R1. In PPO you train a separate **value network** (a critic) to estimate the baseline expected reward at each state, and the advantage is reward minus that baseline. That critic is roughly the same size as the policy, so it doubles memory and adds its own training instability and hyperparameters. GRPO removes it. For each prompt you sample a **group** of outputs from the current policy, score them all with the reward function, and use the group's mean (and standard deviation) as the baseline: an output's advantage is how much better than its peers it did, normalised within the group. No learned critic, just the empirical group statistics.

That is a big efficiency win, which is on-brand for DeepSeek: you cut the critic's memory and compute, and for verifiable-reward tasks (math, code) where reward is a cheap, objective check, the group baseline is a perfectly good advantage estimate. You keep PPO's clipped surrogate objective and a KL penalty toward a reference policy to stop the model drifting off distribution.

The costs: you need multiple samples per prompt (the group), so more inference per update, and the baseline is only as good as your group size and reward signal. It shines when rewards are verifiable and cheap to compute at scale; it is shakier when reward is a noisy learned model, where a proper critic might reduce variance more.

**Follow-ups:** How does group size trade off against variance and cost? Where does the KL-to-reference term matter most, and what breaks if you drop it?

</details>

### 6. R1-Zero was trained with reinforcement learning and essentially no supervised fine-tuning first. What did that show, and why did the full R1 add SFT back?

<details><summary><b>Answer</b></summary>

R1-Zero's result is the striking one: starting from the base model and applying RL with simple, rule-based verifiable rewards (is the final answer correct, is the format right), reasoning ability emerged on its own. The model learned to produce long chains of thought, to self-verify, to backtrack, and reasoning benchmark scores climbed sharply (for example AIME pass@1 rising from the mid-teens to the seventies over training). The point it proved is that you do not necessarily need human-written reasoning traces to get reasoning; you can incentivise it with reward alone, and sophisticated behaviours like re-checking work appear without being explicitly demonstrated.

The catch is that pure-RL output is a mess to *use*. R1-Zero suffered from poor readability and language mixing - it would switch languages mid-trace or produce chains that were effective but hard to read. So the full R1 pipeline reintroduces a small amount of curated cold-start SFT data before RL to give the model a clean starting style and format, then does RL for reasoning, then a further round to fold in general helpfulness and safety. SFT here is not teaching it to reason - RL does that - it is fixing presentation and stability so the reasoning is legible and well-behaved.

The lesson for a candidate: separate the capability question (RL can induce reasoning) from the product question (you still need alignment and formatting passes to ship it).

**Follow-ups:** What reward-hacking failure modes would you watch for with rule-based rewards? Why does language mixing emerge, and how would you penalise it without hurting reasoning?

</details>

### 7. FP8 training at 671B scale is hard. What actually breaks in low precision, and how do you make it stable?

<details><summary><b>Answer</b></summary>

FP8 has very few mantissa bits and a narrow dynamic range, so the failure mode is that a handful of large-magnitude values (activation or gradient outliers) either overflow or force the scale so high that everything small underflows to zero. Do it naively across a whole tensor and training diverges or silently loses signal. The reason FP8 is worth the pain is that it roughly halves memory and doubles tensor-core throughput versus BF16, which at 671B parameters is the difference between feasible and not.

DeepSeek's approach is **fine-grained quantization** rather than per-tensor: they scale in small blocks - reported as tile-wise 1x128 for activations and block-wise 128x128 for weights - so an outlier only blows up the scale of its own small block instead of the entire tensor, keeping precision where the values are well-behaved. They also keep the numerically sensitive parts in higher precision: master weights, optimizer state, and certain accumulations stay in BF16/FP32, and they promote accumulation out of FP8 to avoid error building up over a long dot product. The GEMMs run in FP8 (they open-sourced DeepGEMM for exactly this), but the accumulation and the delicate reductions do not.

The general principle to state: quantize the bandwidth- and compute-heavy matmuls, protect the low-count, high-sensitivity state, and choose a quantization granularity fine enough that outliers are contained. Prove it with loss-curve parity against a BF16 baseline, not vibes.

**Follow-ups:** Why is per-tensor scaling insufficient and per-block enough? Which tensors would you never put in FP8, and why keep FP32 master weights?

</details>

### 8. Sketch how you would serve a 671B-parameter MoE model with low latency under GPU-memory constraints.

<details><summary><b>Answer</b></summary>

Start from the constraint: 671B parameters will not fit on one GPU even at FP8, so serving is inherently multi-GPU, and MoE means memory scales with *total* parameters (all experts resident) while compute scales with *active* ones (about 37B). So you shard. Use **expert parallelism** to spread experts across devices, plus tensor/pipeline parallelism for the dense parts, and accept that every token now triggers all-to-all communication to reach its expert. That communication is the latency enemy, so you overlap it with compute and co-locate frequently co-activated experts; DeepEP exists precisely to make this all-to-all fast.

Next, attack the KV cache, which at long context dominates memory: MLA already compresses it to a latent, and you can quantize the latent further. Use continuous (iteration-level) batching with paged KV so short requests do not wait on long ones and admission is cheap. Separate **prefill and decode**: prefill is compute-bound and batches well, decode is memory-bandwidth-bound, so many systems disaggregate them onto different pools sized differently. Add MTP/speculative decoding to cut per-token steps.

The MoE-specific serving headache is **load imbalance within a batch**: if many tokens in a step route to the same expert, that device becomes the bottleneck while others idle. So you need dynamic expert placement or replication of hot experts (an EPLB-style balancer) and you plan capacity around p95 routing skew, not the average. The whole design is a bandwidth-accounting exercise: weights, KV, and all-to-all traffic, budgeted against the interconnect.

**Follow-ups:** How do you decide the expert-parallel degree versus tensor-parallel degree? What metric tells you experts are imbalanced in production, and what is your mitigation?

</details>

### 9. Implement top-k MoE routing with a shared expert in PyTorch, and point out where the efficiency and correctness traps are.

<details><summary><b>Answer</b></summary>

A readable forward pass for one MoE layer:

```python
import torch, torch.nn.functional as F

def moe_forward(x, router_w, routed_experts, shared_expert, k, bias):
    # x: (T, d).  bias: (E,) per-expert load-balancing bias, no grad.
    scores = x @ router_w                     # (T, E) affinities
    topv, topi = torch.topk(scores + bias, k, dim=-1)   # bias steers selection only
    gate = F.softmax(topv, dim=-1)            # weights from UNBIASED-ranked scores' values

    out = shared_expert(x)                    # shared expert runs for every token
    for slot in range(k):
        idx = topi[:, slot]                   # (T,) expert id chosen in this slot
        w   = gate[:, slot].unsqueeze(-1)     # (T,1) its gate weight
        for e in routed_experts.unique_ids(): # in practice: group tokens per expert
            mask = idx == e
            if mask.any():
                out[mask] += w[mask] * routed_experts[e](x[mask])
    return out
```

Traps interviewers probe. **Correctness:** the load-balancing bias must affect *selection* (the topk) but the gate value used in the weighted sum should come from the true affinity, not the biased one - mix these up and you distort expert contributions. The shared expert is unconditional and must not be double-counted in the routed loop. **Efficiency:** the Python `for e in experts` loop is the naive version; real code sorts/groups tokens by expert once and does one batched matmul per expert (a grouped GEMM), because launching many tiny per-token kernels destroys throughput. In distributed training this grouping is an all-to-all that ships tokens to the device holding each expert, then ships results back. Also handle the capacity case: if an expert is overloaded beyond its buffer, you either drop or overflow tokens, and that policy affects both quality and balance.

**Follow-ups:** Rewrite the inner loop as a grouped matmul. How does token dropping at capacity interact with the auxiliary-loss-free bias?

</details>

### 10. How do you build a training dataset without triggering model collapse when a lot of your data is synthetic?

<details><summary><b>Answer</b></summary>

Model collapse is the failure where a model trained heavily on another model's (or its own) outputs progressively loses the tails of the distribution: rare facts, unusual phrasings, and diversity disappear, and quality degrades generation after generation. The core cause is that generated data is a lossy, mode-seeking sample of the real distribution, so recycling it amplifies the centre and forgets the edges. So the first rule is that synthetic data supplements real data, it does not replace it - keep a strong anchor of human/real corpus so the tails stay represented.

Concretely: (1) **verify, do not just generate.** For domains with checkable answers - math, code, formal reasoning - keep only synthetic samples that pass a verifier (unit tests, a solver, an execution check). Verified synthetic data is high-signal precisely because the filter, not the generator, decides what survives. (2) **Deduplicate and diversity-filter** aggressively; near-duplicate synthetic samples collapse variety and over-weight whatever the generator likes. (3) **Filter for quality and difficulty**, not volume - a smaller curated set beats a huge noisy one, and mixing in genuinely hard examples prevents the model from only seeing easy, self-confirming cases. (4) **Track distribution drift**: monitor n-gram/embedding diversity and per-domain coverage across data generations so you catch narrowing early.

The DeepSeek-flavoured version of this answer stresses the pipeline as a first-class research artefact: their reasoning data is built by generating candidate traces, verifying outcomes, and keeping the winners, which is exactly the "let a cheap objective filter do the curation" pattern.

**Follow-ups:** How would you measure diversity loss quantitatively before it shows up in benchmarks? When is self-generated data safe to train on and when is it poison?

</details>

### 11. DualPipe overlaps computation and communication in training. Why is that overlap the whole game at this scale, and what is the trade-off?

<details><summary><b>Answer</b></summary>

At 671B parameters across a large cluster, the GPUs spend a large fraction of every step *waiting*: pipeline parallelism leaves bubbles (stages idle while the pipeline fills and drains), and MoE adds heavy all-to-all traffic to route tokens to experts. If communication runs while compute is stalled, your expensive accelerators are underused and effective throughput craters. The single highest-leverage systems move is therefore to **hide communication behind computation** so the network transfers happen concurrently with matmuls rather than in series.

DualPipe is a bidirectional pipeline-parallelism schedule that runs micro-batches from both ends of the pipeline so that forward and backward phases interleave, shrinking the bubble, and it carefully arranges the schedule so that the all-to-all communication of one micro-batch overlaps the computation of another. Combined with a communication library tuned for the cross-node MoE traffic (DeepEP), most of the communication cost disappears into time the GPU was going to spend computing anyway. That overlap is a big part of how they hit their reported training-cost efficiency on constrained hardware.

The trade-off is memory and complexity. Keeping two directions of the pipeline in flight and overlapping stages means holding more activations and more in-flight state simultaneously, so DualPipe trades higher peak memory for lower idle time, and the schedule is far more intricate to implement and debug than naive 1F1B. It is worth it only when communication is genuinely a large share of step time, which at this scale it is.

**Follow-ups:** Where does the extra memory in DualPipe come from, and how would you bound it? When is pipeline parallelism the wrong tool versus more tensor or data parallelism?

</details>

### 12. DeepSeek claims frontier-class results at a fraction of the usual training cost. If an interviewer asks "how is that even possible," what is your structured answer?

<details><summary><b>Answer</b></summary>

Frame it as compounding efficiency at every layer, not one magic trick, and be careful about what the cost number does and does not include. **Architecture:** MoE means you train and serve with about 37B active parameters while holding 671B of capacity, so you pay far less compute per token than a dense model of equivalent quality; MLA shrinks the KV cache so long-context training and inference fit; MTP squeezes more signal from each step. **Numerics:** FP8 training roughly halves memory and doubles matmul throughput, and fine-grained quantization makes it stable at scale. **Systems:** DualPipe plus a tuned all-to-all library hide the MoE communication behind compute, so the cluster stays busy; custom kernels (FlashMLA, DeepGEMM) mean they are not leaving hardware performance on the table. **Method:** verifiable-reward RL with GRPO (no critic network) gets reasoning cheaply, and heavy data curation means fewer wasted tokens.

The honest caveats a good candidate adds: the widely cited figure is a *final training run* compute cost, not total cost of ownership - it excludes prior research, failed runs, data work, and salaries. It also reflects the discipline of a team that co-designs model, kernels, and cluster together, which is hard to replicate by copying any single component. The real lesson is organisational: efficiency came from owning the whole stack, from the attention variant down to the GEMM and the file system, so no layer silently wastes the others' work.

**Follow-ups:** Which of these levers generalises to a lab with different hardware, and which is specific to their GPU setup? What is missing from a single "training cost" number?

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - the highest-leverage dir for DeepSeek. Attention variants and MoE are the whole conversation: know MHA/GQA/MLA, KV-cache math, RoPE (and why it complicates MLA), sparse MoE routing, and multi-token prediction well enough to *implement*, not just describe.
2. **[08-inference-and-production](../08-inference-and-production/)** - inference economics is their obsession. KV-cache compression, continuous batching, paged attention, prefill/decode disaggregation, quantization (FP8/INT4), speculative decoding, and MoE serving imbalance.
3. **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - RL for reasoning is a house specialty. GRPO vs PPO, reward design for verifiable tasks, reward hacking, and the SFT-then-RL pipeline behind R1.
4. **[01-ml-and-dl-foundations](../01-ml-and-dl-foundations/)** and **[12-coding-challenges](../12-coding-challenges/)** - the reported hire/reject line is clean, efficient PyTorch under time pressure. Practise turning paper equations into correct implementations, and drill algorithmic coding too.
5. **[11-ai-system-design](../11-ai-system-design/)** - use a structured framework for "serve a 100B+ MoE model under GPU-memory limits" and "design an efficient training cluster." Closest existing case study: **[AI code assistant](../11-ai-system-design/case-studies/02-ai-code-assistant.md)** - a latency-sensitive product built on serving a large model, which forces exactly the KV-cache, batching, and throughput trade-offs DeepSeek probes.

Company-specific moves:

- **Read the DeepSeek-V3 and DeepSeek-R1 technical reports end to end** (both on arXiv; R1 is also in Nature). They are detailed and readable, and they are the single best-calibrated map of what this team cares about. Being fluent in MLA, DeepSeekMoE, auxiliary-loss-free balancing, MTP, FP8, and GRPO covers a large fraction of the plausible deep-dive.
- **Read their open-source infra releases** - FlashMLA, DeepEP, DeepGEMM, DualPipe, EPLB, 3FS. Even skimming the READMES teaches you why each component exists, which is the systems half of the interview.
- **Run an open-weight DeepSeek model locally and inspect the config** - MoE layer counts, expert counts, MLA dimensions. Speaking from the actual config beats book knowledge in a lab that ships the weights.
- **Prepare a data-curation story.** Have a real answer for filtering synthetic data, verifiable rewards, and avoiding model collapse; it is a distinct competence here.
- **Rehearse explaining one hard result crisply.** They value clear technical writing and breadth, so practise connecting your niche to the larger efficient-LLM picture out loud.

## Sources

- [DeepSeek-V3 Technical Report (arXiv 2412.19437)](https://arxiv.org/abs/2412.19437) - MLA, DeepSeekMoE, auxiliary-loss-free load balancing, multi-token prediction, FP8 training, DualPipe, 671B/37B-active
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (arXiv 2501.12948)](https://arxiv.org/abs/2501.12948) - GRPO, R1-Zero pure-RL reasoning, cold-start SFT, emergent self-verification
- [DeepSeek-R1 in Nature](https://www.nature.com/articles/s41586-025-09422-z) - peer-reviewed version of the R1 work
- [DualPipe (GitHub)](https://github.com/deepseek-ai/DualPipe) - bidirectional pipeline-parallelism algorithm for computation-communication overlap
- [DeepSeek AI Researcher interview guide, datainterview.com](https://www.datainterview.com/blog/deepseek-ai-researcher-interview) - third-party guide describing a 3-4 round hardcore technical loop, coding/efficiency emphasis, data-chemistry and system-design topics (unofficial)
- [SCMP: DeepSeek's LinkedIn AI job listings](https://www.scmp.com/tech/big-tech/article/3316982/deepseeks-linkedin-ai-job-listings-show-hunger-international-chinese-talent) - roles, Hangzhou/Beijing locations, hiring of young talent
- [Bloomberg: DeepSeek job postings highlight pivot to agentic AI](https://www.bloomberg.com/news/articles/2026-03-24/deepseek-s-latest-job-postings-highlight-pivot-to-agentic-ai) - recent agentic-AI role emphasis (2026)

Note: DeepSeek does not publish an official interview-process page, and first-person candidate reports in English are scarce, so the loop section above is explicitly labelled as inference plus third-party report rather than confirmed process.
