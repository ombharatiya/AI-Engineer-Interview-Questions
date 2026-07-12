# 📦 Amazon (AWS + AGI) - AI Engineer Interview Guide

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- **Leadership Principles are half the interview.** Every interviewer in the loop is assigned 2-3 of Amazon's 16 Leadership Principles and grades you against them with STAR-format behavioural questions. This is not a formality - candidates with strong technical rounds fail on weak LP stories. Prepare 8-10 quantified stories before you touch LeetCode.
- **The Bar Raiser is real and has veto power.** One interviewer from outside the hiring team, specially trained, whose job is to keep the bar high. They ask the hardest behavioural questions and probe your STAR stories several "why" levels deep.
- **The loop shape is well documented.** Recruiter screen → (sometimes) online assessment → 1-2 technical phone screens → 4-6 back-to-back ~60-minute interviews covering coding, (ML) system design, domain depth, and behavioural. Amazon publishes official prep pages for several tracks.
- **"AI engineer" spans very different orgs.** AWS AI platform teams (Bedrock, SageMaker, Q) interview like senior SDE loops with an ML flavour; the AGI org (Nova models, AGI SF Lab agents) runs science-style loops with ML breadth/depth rounds and - per candidate reports - fewer behavioural questions and heavy modern-LLM content.
- **Coding is still classic DS&A.** Unlike most frontier labs, Amazon keeps traditional algorithm rounds (graphs, heaps, design-a-cache) alongside ML content. System design is at genuine extreme scale: multi-tenancy, throttling, cell-based isolation, and operational excellence are native vocabulary.

## Company context

Amazon runs two distinct AI bets: AWS sells the picks and shovels - Bedrock (multi-model inference platform), SageMaker, Amazon Q (enterprise/developer assistants), and Trainium silicon - while the AGI org builds Amazon's own frontier models (the Nova family) and agents (Nova Act, the AGI SF Lab founded around Adept's team). Engineers want in for scale you cannot get elsewhere - Bedrock serves foundation-model inference to a large share of the world's enterprises - and, on the AGI side, for a funded frontier-model effort with its own silicon. "AI engineer" at Amazon therefore means anything from multi-tenant GPU serving infrastructure, to applied GenAI teams embedding LLMs in every product org (search, ads, Alexa+, Rufus), to research engineering on pretraining and agents.

## Roles & titles they hire

- **Software Development Engineer (SDE I/II/III)** - on Bedrock, SageMaker, Q, and GenAI feature teams; the most common door into AI work at Amazon
- **Applied Scientist / Senior Applied Scientist** - science track; official interview-prep page exists; heavy ML breadth/depth
- **Machine Learning Engineer / ML Ops Engineer** - productionising models, more common in product orgs
- **Research Scientist / Research Engineer (AGI, AGI SF Lab)** - frontier model training and agents; the SF Lab publicly recruits strong quantitative people from any discipline
- **Solutions Architect / Prototyping Architect (GenAI specialist)** - customer-facing AWS roles; Amazon's closest analogue to forward-deployed engineering
- **Data Scientist** - analytics-leaning, separate loop

## The interview loop

Public confidence here is high: Amazon documents its process (including official applied-scientist and SDE prep pages), and thousands of candidate reports are broadly consistent. Exact round count varies by level and org.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter screen | 15-30 min | Fit, level calibration, timeline |
| Online assessment | Coding tasks + work-style simulation; mainly SDE-track and junior roles (reported, varies) | DS&A correctness, LP-aligned judgement |
| Technical phone screen(s) | 1-2 × ~60 min, shared editor; for Applied Scientist, with a senior scientist/leader (official) | Coding, ML fundamentals (metrics, evaluation), 1-2 LP questions |
| Onsite "loop" | 4-6 × 55-60 min back-to-back, virtual or in person; 4 interviews is the official applied-scientist shape | See below - every round includes assigned Leadership Principles |
| - Coding round(s) | 1-2 rounds, classic DS&A; AGI loops add ML coding (implement a model component) (reported, varies) | Working code, complexity analysis, testing instincts |
| - ML breadth + ML depth | Science-track and AGI loops: fundamentals sweep, then deep dive in your specialty; heavy modern LLM-training content reported for AGI | Real understanding vs. buzzwords |
| - System design / ML system design | SDE II+ and all senior roles | Scale, multi-tenancy, tradeoffs, operational excellence |
| - Science application / tech talk | Applied-scientist loops: applied problem or presentation of your own work (official + reported) | Research-to-product judgement |
| - Bar Raiser round | One interviewer from outside the team, veto power (official) | LPs under deep probing; overall hiring bar |
| Debrief → offer | Interviewers vote; Bar Raiser must agree | - |

Typical end-to-end timeline reported publicly: 3-6 weeks. AGI-org loops are reported to weight behavioural questions lighter and ML depth heavier than standard Amazon loops (reported, varies).

## What they emphasise

- **Leadership Principles, operationalised.** Not culture-fit vibes - a scoring rubric. The most commonly probed LPs in engineering loops per public reports: Customer Obsession, Ownership, Dive Deep, Invent and Simplify, Have Backbone; Disagree and Commit, Deliver Results. Answers must be first-person ("I", not "we"), specific, and quantified.
- **Dive Deep as a technical signal.** Interviewers push past your first answer: why that data structure, why that consistency model, what exactly was the root cause. Vague seniority reads as a red flag.
- **Operational excellence.** AWS teams live on-call: expect debugging scenarios, p99 thinking, blast-radius reduction, rollback-first instincts. Knowing what a metric/alarm/runbook culture looks like is a differentiator.
- **Scale and multi-tenancy by default.** Design answers that ignore noisy neighbours, throttling, quotas, and per-tenant isolation miss the core of what AWS builds.
- **Frugality applied to GPUs.** Cost-per-token and right-sizing model choice is an Amazon-flavoured design axis; "use the biggest model everywhere" is the wrong answer.
- **For AGI: modern LLM literacy.** Candidate reports describe questions on training techniques, evaluation (including perplexity and preference-based evals), and data quality - closer to a frontier-lab loop than a classic Amazon one.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Tell me about a time you disagreed with your team's technical direction. What did you do?

<details><summary><b>Answer</b></summary>

This targets **Have Backbone; Disagree and Commit** - a heavily probed LP. Structure with STAR and keep the Action section longest.

Strong answer shape: (S/T) a concrete decision with real stakes - e.g., the team wanted to fine-tune a model where you believed retrieval would be cheaper and easier to update. (A) You disagreed *with data*: built a quick eval set, benchmarked both approaches, presented cost and latency numbers, and escalated respectfully when the first conversation didn't land. (R) Either you changed the decision - quantify the outcome - or you were overruled and **committed fully**, without relitigating or sandbagging, and you can say what you learned.

What the interviewer (often the Bar Raiser) is grading:

- Did you disagree with evidence rather than opinion or seniority?
- Did you push at the right level - direct, not passive-aggressive, not a flame war?
- After the decision, did you genuinely commit? "I kept saying I told you so" fails the second half of the principle.
- Is it a real story? They will probe: exact metrics, who was in the room, what you'd do differently. Rehearsed-but-hollow stories collapse under Bar Raiser follow-ups.

Avoid: stories where the disagreement was trivial, where "we" did everything, or where your only action was voicing concern once and going quiet.

**Follow-ups:** What would you have done if you'd been overruled and then proven right? Tell me about a time you were the one who was wrong.

</details>

### 2. Design a multi-tenant inference platform that serves many foundation models to thousands of customers (Bedrock-shaped).

<details><summary><b>Answer</b></summary>

Split control plane from data plane immediately - that's the AWS-native move.

**Control plane:** model catalogue and versioning, tenant onboarding, quotas, per-tenant config (guardrails, logging opt-outs), capacity reservations. **Data plane:** the request path - authn/authz, per-tenant throttling (token bucket keyed on account + model), admission control, then routing to a model fleet.

**Fleet design:** each model family gets a pool of GPU workers running continuous batching with paged KV-cache. Two capacity classes mirror the real product: *on-demand* (shared pools, fair-queued, may queue under load) and *provisioned throughput* (dedicated capacity for a tenant - strict isolation, predictable latency, higher cost). Scale pools on queue depth and tokens/sec, not CPU.

**Isolation is the crux of multi-tenancy:** no cross-tenant KV or prompt leakage (clear per-request state), per-tenant encryption of logs, cell-based architecture so one region/cell failure or one abusive tenant has bounded blast radius, and noisy-neighbour control via admission and per-tenant concurrency caps.

**Cross-cutting:** guardrails/content filtering as a composable layer before and after the model; metering every input/output token for billing; observability split into TTFT, per-token latency, and queue time so you can localise regressions; deployment via canary cells with automatic rollback.

Tradeoffs to name: batching raises throughput but hurts tail latency for streaming; provisioned capacity wastes GPUs at low utilisation but is the only honest latency SLA; model-agnostic APIs limit per-model optimisations.

**Follow-ups:** How do you handle a 10× traffic spike on one model? Where does prompt caching fit, and what does it leak-risk across tenants?

</details>

### 3. Design an enterprise assistant that answers questions over a company's internal documents, respecting per-user permissions (Amazon Q-shaped).

<details><summary><b>Answer</b></summary>

This is enterprise RAG where **ACL enforcement is the hard requirement**, not retrieval quality.

**Ingestion:** connectors (SharePoint, S3, Confluence, Jira...) pull documents *and their ACLs*. Chunk, embed, and index - but store principal lists (users/groups) as metadata on every chunk. Sync ACL changes on a short schedule; a revoked permission must propagate quickly, so treat ACL sync as a separate, faster pipeline than content re-indexing.

**Query path:** authenticate the user, expand their group memberships, then filter retrieval *at query time* by ACL metadata - never rely only on index-time filtering, because permissions change between crawls. Hybrid retrieval (BM25 + dense) with a reranker; pass only permitted chunks to the LLM with citation markers.

**The failure mode to call out explicitly:** the model must never see a document the user can't see. If it enters the context window, no prompt instruction reliably keeps it out of the answer. Filtering must happen before generation - this single sentence signals you understand the security model.

**Answer quality:** require citations, run a groundedness check (is each claim supported by a retrieved chunk?), and return "I don't know" when retrieval confidence is low - hallucinated answers about HR policy are worse than none.

**Evaluation:** per-connector golden question sets, retrieval recall@k, groundedness/citation precision via calibrated LLM-judge, and a red-team suite specifically for permission leakage (user A asking about user B's restricted docs).

**Follow-ups:** How do you handle a document whose ACL is broader than its content should be? What changes when the corpus is 100M documents across 50 connectors?

</details>

### 4. Find the top-K most frequent items in a high-volume event stream with bounded memory.

<details><summary><b>Answer</b></summary>

Start with the exact solution, then show you know when it breaks - that's the Dive Deep signal.

**Exact (fits in memory):** hash map of counts + min-heap of size K. O(n log K) time, O(n) space for the map. The map, not the heap, is the memory problem: cardinality of a real event stream (user IDs, queries) can be billions.

**Bounded memory:** Count-Min Sketch for approximate counts + a K-sized heap of candidates.

```python
import heapq

class TopK:
    def __init__(self, k, width, depth, hashes):
        self.k = k
        self.cms = [[0] * width for _ in range(depth)]
        self.hashes = hashes          # depth independent hash fns
        self.heap = []                # (est_count, item)
        self.in_heap = {}

    def add(self, item):
        est = min(
            self._bump(row, h(item) % len(row))
            for row, h in zip(self.cms, self.hashes)
        )
        if item in self.in_heap:
            self.in_heap[item] = est
        elif len(self.heap) < self.k or est > self.heap[0][0]:
            # insert / evict min (rebuild heap lazily in practice)
            ...

    def _bump(self, row, idx):
        row[idx] += 1
        return row[idx]
```

Properties worth stating: CMS never undercounts, only overcounts - with width w and depth d, error ≤ n/w with probability 1 − (1/2)^d roughly, so memory is a tunable accuracy knob. For distributed streams, CMS sketches merge by element-wise addition, so each shard sketches locally and a reducer merges - this is what makes it production-viable.

**Follow-ups:** How do you get top-K over a sliding 5-minute window? When would you just use exact counting sharded over hosts instead?

</details>

### 5. Why did transformers displace RNNs for language modelling, and what exactly does the KV cache buy you at inference time?

<details><summary><b>Answer</b></summary>

Two separate wins. **Training:** an RNN must process tokens sequentially - the hidden state at step t depends on t−1 - so you can't parallelize across the sequence, and gradients degrade over long ranges even with LSTM gating. A transformer computes attention over all positions at once: full sequence parallelism on accelerators, and any token can attend directly to any other in one step instead of information surviving hundreds of recurrent updates. That's what made scaling to trillions of training tokens practical. **Modelling:** direct pairwise attention handles long-range dependency better than a compressed fixed-size hidden state.

The cost is attention's O(n²) compute and memory in sequence length, versus O(n) for an RNN - which is why long-context work centres on attention variants (sliding-window, grouped-query, sparse) and better kernels.

**KV cache:** at generation step t you need attention between the new query and keys/values of all previous tokens. Without caching you'd recompute every layer's K and V for the whole prefix at every step - O(n²) redundant work per token. Caching stores each layer's K,V once, making each new token roughly O(n) attention against cached tensors. The price is memory: cache size scales with layers × KV-heads × head_dim × sequence length × batch, which is exactly why serving systems care about grouped-query attention (fewer KV heads), quantized caches, and paged allocation - KV memory, not weights, is often what caps concurrent batch size on a GPU.

**Follow-ups:** Why does grouped-query attention shrink the cache and what does it trade? How does prefix/prompt caching relate to the KV cache?

</details>

### 6. Your LLM endpoint's p99 latency doubled after a deploy. The model weights didn't change. Walk me through your debugging.

<details><summary><b>Answer</b></summary>

Lead with the operational instinct: **mitigate before root-causing**. If a rollback is safe and the regression is customer-impacting, roll back first - the investigation can proceed against the bad build in a test cell. Interviewers at AWS are explicitly listening for this ordering.

Then decompose. "Latency" for an LLM service is at least three numbers: queue/admission time, time-to-first-token (prefill), and per-token time (decode). Which moved?

- **Queue time up:** admission control or autoscaling changed - check batch scheduler config, max concurrent sequences, scaling thresholds shipped in the deploy.
- **TTFT up:** prefill path - longer prompts (traffic-mix shift, not deploy), a tokenizer or prompt-template version change silently inflating input tokens, or prompt-cache hit rate dropped because a cache key changed.
- **Per-token time up:** decode path - batch size limits changed, KV-cache memory pressure causing preemption/recompute, a runtime/driver/kernel version bump in the container image, or speculative decoding disabled by a config flag.

Also rule out the boring suspects: retries amplifying load (check retry rate - a new timeout can create a retry storm that looks like a latency problem), one bad host or heterogeneous GPU node in the fleet (check per-host p99), and upstream/downstream dependencies (guardrail or logging service slowed down in-line).

Close with prevention: config changes should canary like code, dashboards should split TTFT/TPOT/queue by default, and the finding feeds a blameless COE-style writeup with action items.

**Follow-ups:** p99 doubled but p50 is flat - what does that tell you? What alarm would have caught this pre-customer?

</details>

### 7. You're training a large model across hundreds of accelerators. Compare data, tensor, and pipeline parallelism - when do you combine them?

<details><summary><b>Answer</b></summary>

**Data parallelism (DP):** replicate the model, shard the batch, all-reduce gradients each step. Simplest and scales widest, but requires the model (plus optimizer state) to fit on one device - optimizer state is the killer: Adam in mixed precision costs several times the parameter memory. ZeRO/FSDP fix this by sharding parameters, gradients, and optimizer state across the DP group, gathering shards on demand; this is the default for models that almost fit.

**Tensor parallelism (TP):** split individual weight matrices across devices - each matmul becomes partial matmuls plus an all-reduce *inside every layer*. Communication is frequent and latency-sensitive, so TP lives within a node on the fastest interconnect (NVLink, or NeuronLink on Trainium). It's how a single layer too big for one device fits at all.

**Pipeline parallelism (PP):** assign contiguous layer blocks to different devices; microbatch the input so stages overlap. Communication is small (activations at stage boundaries), so PP tolerates slower cross-node links - but pipeline "bubbles" waste compute at the start and end of each step, so you need enough microbatches to amortise, and interleaved schedules to shrink the bubble.

**Combining:** frontier-scale training uses 3D parallelism - TP within a node, PP across nodes, DP across the remaining axis - plus sequence/context parallelism for long-context phases. Rule of thumb: use the minimum TP that fits a layer, minimum PP that fits the model, and spend everything else on DP, because DP scales throughput most cheaply.

At hundreds of hosts, checkpointing strategy and straggler/failure recovery matter as much as the parallelism math - mean time between hardware failures becomes shorter than the run.

**Follow-ups:** Where does gradient accumulation fit? Why does activation checkpointing trade compute for memory, and when is it not worth it?

</details>

### 8. How would you decide an LLM-powered assistant is ready to launch to millions of customers?

<details><summary><b>Answer</b></summary>

Frame it as a gate ladder, and anchor every gate to a customer-facing metric - that's the Customer Obsession framing Amazon rounds reward.

**Offline gates:** a versioned golden set covering the real task distribution plus hard cases (ambiguous queries, out-of-scope requests, adversarial inputs). Grade with rubric-based LLM-as-judge *calibrated against human labels* - report judge - human agreement, or the numbers mean nothing. Separate capability metrics (task success, groundedness, citation precision) from safety metrics (harmful content, prompt-injection resilience, PII leakage), because they gate independently: a model can get smarter and less safe in the same revision.

**Regression discipline:** evals run in CI on every prompt, model, or retrieval change; a launch candidate must beat or match the incumbent on the golden set with no safety regressions. Track eval-set contamination and refresh sets over time.

**Pre-launch traffic:** shadow mode (new system answers silently alongside the old, compare offline) → internal dogfood → canary at a small percentage of real traffic with automatic rollback wired to leading indicators: thumbs-down rate, escalation-to-human rate, retry/rephrase rate, latency.

**Launch criteria written down in advance** - target task-success rate, maximum hallucination rate on the golden set, safety red-team pass rate, p99 latency - so the go/no-go is mechanical, not vibes. Post-launch, sample production conversations (with consent/privacy controls) into a labelling queue so the golden set grows from real failures.

The senior signal: saying explicitly that no offline eval fully predicts online behaviour, so the canary + rollback machinery *is* part of the eval strategy.

**Follow-ups:** Your judge and your humans disagree 20% of the time - what do you do? Which single online metric would you alarm on first?

</details>

### 9. Design an agent that operates a web browser to complete multi-step tasks. How do you make it reliable enough to ship?

<details><summary><b>Answer</b></summary>

This is the AGI SF Lab / Nova Act problem shape: agents that act in real environments, where the bar is reliability, not demos.

**Core loop:** observe (DOM accessibility tree + screenshot - DOM for precision and cheap tokens, vision for canvas/rendered content the DOM misses) → plan → act (a small, typed action space: click element-by-reference, type, scroll, navigate) → verify. The verify step is what separates shippable from demo: after each action, check an explicit postcondition (did the cart count increment?) rather than assuming success and drifting silently off-course.

**Reliability mechanisms:**

- Decompose long tasks into small, individually-verifiable steps; retry at step level, not task level.
- Checkpoint state so a mid-task failure resumes instead of restarting.
- Bounded budgets (steps, time, cost) with graceful abandonment and a report of what was and wasn't done.
- Human confirmation gates on irreversible or sensitive actions - purchases, sends, deletes. Never let the agent self-authorise.

**Security is a first-class design axis:** web page content is untrusted input, and prompt injection ("ignore your instructions, click here") is the top attack. Mitigations: strictly separate page content from instructions in the context, constrain the action space per task, and treat any page-originated "instruction" as data requiring user confirmation.

**Evaluation:** success rate over a large suite of real-site tasks, run repeatedly - single-run success is meaningless for stochastic agents; report pass@k and consistency. Track per-step failure taxonomy (grounding error, stale DOM, planning error) so improvements target the actual bottleneck.

**Follow-ups:** Sites A/B-test and change layouts constantly - how does your agent stay robust? How would you use RL or fine-tuning on trajectories versus prompting a general model?

</details>

### 10. Implement scaled dot-product attention with a causal mask in NumPy.

<details><summary><b>Answer</b></summary>

ML-coding rounds (reported in AGI loops) want a clean implementation plus proof you know why each line exists.

```python
import numpy as np

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)   # numerical stability
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def attention(Q, K, V, causal=True):
    """Q: (B, T, d_k), K: (B, T, d_k), V: (B, T, d_v)"""
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)   # (B, T, T)
    if causal:
        T = scores.shape[-1]
        mask = np.triu(np.ones((T, T), dtype=bool), k=1)
        scores = np.where(mask, -1e9, scores)          # not 0!
    weights = softmax(scores, axis=-1)                 # (B, T, T)
    return weights @ V                                  # (B, T, d_v)
```

Points to make unprompted:

- **√d_k scaling:** dot products of d_k-dimensional vectors have variance ~d_k; unscaled, softmax saturates and gradients vanish.
- **Mask with −inf (large negative), not zero:** a zero score still gets positive softmax weight; you need it to vanish *after* softmax.
- **Stable softmax:** subtract the row max first, or large logits overflow.
- **Complexity:** O(T²·d) time, O(T²) score memory per head - say that this T² memory is what FlashAttention eliminates by tiling and never materialising the full matrix.

Extension the interviewer often asks for: multi-head - reshape to (B, h, T, d_k/h), attend per head, concatenate, project. Be able to write it without hesitation.

**Follow-ups:** Modify it for grouped-query attention. How does the causal mask interact with a KV cache at inference (hint: the new token attends to everything cached - no mask needed at decode)?

</details>

### 11. A customer's Bedrock-hosted workload costs too much. Cut inference cost dramatically without unacceptable quality loss - walk me through it.

<details><summary><b>Answer</b></summary>

Frugality-flavoured design question. The senior move: **measure before optimising** - get cost per request decomposed into input tokens, output tokens, and model choice; the biggest lever is usually not where intuition points.

Ordered by typical impact:

1. **Right-size the model per task.** Most traffic in a real workload is easy. Route with a cheap classifier or confidence signal: small model (a Haiku/Nova-Lite-class option) for the bulk, large model for the hard tail. This alone is often a multiple-x cost cut. Requires an eval set to prove quality holds - routing without evals is guessing.
2. **Attack input tokens.** Prompts accrete cruft: trim the system prompt, deduplicate few-shot examples, cap retrieved chunks by relevance instead of a fixed k. Prompt caching makes repeated prefixes (long system prompts, shared documents) dramatically cheaper - restructure prompts so the static part is a stable prefix.
3. **Cap and shorten outputs.** Output tokens cost more than input; set max-token limits, ask for terse formats (JSON, not prose), stop sequences.
4. **Batch the asynchronous work.** Anything not latency-sensitive (nightly summarisation, backfills) moves to batch processing at discounted, off-peak pricing.
5. **Distill or fine-tune small.** If one high-volume task dominates, fine-tune a small model on the large model's outputs for that task - highest effort, biggest durable win.
6. **Semantic caching** for genuinely repeated queries - measure the real hit rate first; it's often lower than hoped.

Wrap with governance: per-team token budgets, cost dashboards, and alarms - otherwise the savings erode in a quarter.

**Follow-ups:** Which of these would you do first with one week and no fine-tuning budget? How do you prove quality didn't regress?

</details>

### 12. Tell me about your most significant failure. What happened, and what did you change afterward?

<details><summary><b>Answer</b></summary>

A Bar Raiser staple, targeting **Ownership**, **Dive Deep**, and **Earn Trust**. The trap is picking a fake failure ("I worked too hard"). Pick a real one with real cost - a launch that missed, an outage you caused, a model that regressed in production.

Structure that works:

- **Situation/Task:** stakes stated plainly, with numbers. "I owned the ranking model powering X; a bad deploy degraded conversion for N hours."
- **Action (the longest part):** what *you* did in the moment - detection, mitigation, communication - told honestly, including what you got wrong. First person throughout.
- **Root cause, Amazon-style:** show five-whys depth. Not "the config was wrong" but "the config was wrong *because* nothing validated it, *because* our deploy pipeline treated config as data, *because* we'd never treated config changes as code changes."
- **Result + mechanism:** what changed structurally, not just "I learned to be careful." Amazon's culture explicitly prefers mechanisms over good intentions: the validation you added, the canary stage you introduced, the runbook or alarm that now exists. If you wrote a blameless postmortem and drove its action items, say so - that maps directly to Amazon's Correction of Errors practice.

What gets probed: whether you take real ownership (blaming a teammate or "the process" fails Earn Trust), whether your root cause survives three more "why"s, and whether the mechanism actually stuck. Quantify the recurrence: "zero repeats in the following year" is the ending they want.

**Follow-ups:** What signal existed before the failure that you missed? How did you communicate it to your customers or leadership?

</details>

## How to prepare

Priority order for this repo, given Amazon's loop shape:

- **[11-ai-system-design](../11-ai-system-design/)** - the highest-leverage dir. AWS design rounds are extreme-scale and multi-tenant by default; practise saying "control plane vs data plane," "cell-based isolation," "throttling and admission control" naturally. Closest case study: **[01-enterprise-rag-assistant](../11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)** (this is Amazon Q Business almost exactly - permissions-aware enterprise RAG); also do **[02-ai-code-assistant](../11-ai-system-design/case-studies/02-ai-code-assistant.md)** if you're targeting Q Developer.
- **[12-coding-challenges](../12-coding-challenges/)** - Amazon keeps classic DS&A rounds more than any frontier lab. Heaps, graphs, design-a-cache, streaming problems.
- **[01-ml-and-dl-foundations](../01-ml-and-dl-foundations/)** + **[02-llm-fundamentals](../02-llm-fundamentals/)** - the ML breadth round is a real filter, and AGI loops go deep on attention, KV caching, training techniques, and evaluation metrics.
- **[08-inference-and-production](../08-inference-and-production/)** - batching, KV-cache memory, quantization, latency decomposition. This is AWS's home turf; shallow answers here hurt more than anywhere else.
- **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - launch gates, LLM-judge calibration, canary/rollback thinking pairs directly with Amazon's operational culture.
- **[04-rag-and-retrieval](../04-rag-and-retrieval/)** and **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - Bedrock Knowledge Bases/Agents, Q, and the AGI SF Lab's agent focus make both fair game.

Company-specific moves:

1. **Write your LP stories first.** 8-10 STAR stories, quantified, first-person, covering at minimum: Customer Obsession, Ownership, Dive Deep, Invent and Simplify, Have Backbone/Disagree and Commit, Deliver Results, and a genuine failure. Practise them aloud - Bar Raiser follow-ups destroy stories you've only written down.
2. **Build something small on Bedrock.** A weekend RAG or agent project using Knowledge Bases and Guardrails teaches you the platform's real seams (provisioned vs on-demand throughput, model routing, guardrail layering) - exactly the vocabulary of their design rounds.
3. **Read the official prep pages** for your track on amazon.jobs ("how we hire," the applied-scientist interview-prep page) - Amazon is unusually explicit about what it grades.
4. **Skim the AWS Machine Learning Blog and Amazon Science blog** for posts from your target team (Bedrock, Q, Nova, AGI SF Lab) - referencing their actual architecture posts lands well and generates good questions for you to ask.
5. **For AGI-org loops:** weight prep toward ML depth - modern training techniques, distributed training, data curation, eval design - and expect fewer behavioural questions than a standard Amazon loop (per candidate reports; still prepare LP stories).

Compensation data for Amazon is on [levels.fyi](https://www.levels.fyi/companies/amazon/salaries).

## Sources

- [Amazon official: Applied Scientist interview prep](https://amazon.jobs/content/en/how-we-hire/applied-scientist-interview-prep) - official loop shape (phone screen + four 55-min interviews), STAR guidance
- [Amazon official: Leadership Principles](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) - the 16 LPs interviewers grade against
- [Amazon official: AGI team page](https://www.amazon.jobs/content/en/teams/agi) - AGI org scope
- [Amazon AGI Labs](https://labs.amazon.science/) - AGI SF Lab, agents focus
- [Amazon Science blog: Amazon opens new AI lab in San Francisco](https://www.amazon.science/blog/amazon-opens-new-ai-lab-in-san-francisco-focused-on-long-term-research-bets) - SF Lab mission and hiring
- [TechCrunch: Amazon forms an AI agent-focused lab led by Adept's co-founder](https://techcrunch.com/2024/12/09/amazon-forms-a-new-ai-agent-focused-lab-led-by-adept-co-founder/) - AGI SF Lab background
- [Dataford: Amazon AI Engineer interview guide](https://dataford.io/interview-guides/amazon/ai-engineer) - loop stages, Bar Raiser, evaluation areas
- [IGotAnOffer: Amazon Machine Learning Engineer interview](https://igotanoffer.com/blogs/tech/amazon-machine-learning-engineer-interview) - MLE loop structure (surfaced in search; page body not fully retrievable at review time)
- Publicly shared candidate reports on 1Point3Acres (e.g., [AGI ML onsite](https://www.1point3acres.com/interview/thread/1151585), [AGI SF Lab ML coding and design](https://www.1point3acres.com/interview/thread/1148854)) - AGI loop shape: coding, ML breadth/depth, science application; heavier LLM-training content, lighter behavioural (reported)
- [levels.fyi: Amazon](https://www.levels.fyi/companies/amazon/salaries) - compensation data
