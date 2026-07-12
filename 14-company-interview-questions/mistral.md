# 🌬️ Mistral AI - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- Official skeleton (from their careers page): intro conversations → **2-5 technical exercises** → values conversation → reference checks. Candidate reports describe 4-5 stages over roughly 2-5 weeks.
- Two distinct tracks: **research/science** (transformer internals, PyTorch from scratch, distributed training) and **applied AI / forward-deployed** (pair programming against the Mistral API, RAG vs fine-tuning judgment, customer-facing pragmatism).
- Expect at least one round that tests whether you understand **how their models actually work**: grouped-query attention, sliding-window attention, sparse MoE routing, KV-cache economics. They ship these techniques in open-weight models, so "I've read the config file" depth is table stakes.
- Applied-track candidates report live **refactoring and API-integration pair programming** - code craft with real APIs, not LeetCode marathons.
- Culture screen is real: their published values are audacity, rigor, customer centricity, speed, and low-ego. Have a substantive answer for "why open weights?" and "why Mistral over a US lab?" - enterprise/EU deployment fluency (on-prem, data residency) is a differentiator.

## Company context

Mistral AI is the European frontier lab: it trains competitive open-weight models (the Mistral 7B and Mixtral lines popularised grouped-query attention, sliding-window attention, and production sparse MoE), and monetises through La Plateforme (API), Le Chat (assistant), and enterprise deployments - including on-prem and VPC installs for European companies with data-residency constraints. Teams are lean relative to US labs, so "AI engineer" at Mistral usually means owning more of the stack: an applied AI engineer might scope a customer's RAG system, fine-tune a model, and ship the serving infrastructure; a research engineer sits close to training runs and inference kernels rather than behind layers of platform teams.

## Roles & titles they hire

From their public job board (jobs.lever.co/mistral):

- **AI Scientist** - research + full MLOps stack (fine-tuning, evaluation, deployment); publication record expected
- **Research Engineer, Machine Learning** - large-scale training systems for the open-weight models; platform or embedded-with-research flavours
- **Applied Scientist / Research Engineer** - client-facing research collaborations across text, image, and speech
- **Applied AI, Forward Deployed Machine Learning Engineer** - customer-facing technical org; fine-tuning experience and strong Python required
- **Applied AI Engineer, Fullstack Software Engineer** - product engineering around Le Chat / La Plateforme
- Plus conventional **Software Engineer** roles (infra, platform, frontend)

Locations cluster around Paris and London, with EMEA postings mentioning Luxembourg, Marseille, Amsterdam, Munich, Zurich, Warsaw, and Lausanne; hybrid is common.

## The interview loop

Public info is moderate: the official careers page confirms the skeleton, and Glassdoor plus individual candidate write-ups fill in stage detail. Exact rounds vary by track and seniority.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter / intro call | ~30 min (reported, varies) | Motivation, team fit, "why Mistral specifically" |
| Technical screen | ~60 min live coding, Python-first (reported, varies) | Applied track: refactoring real-ish code, code craft. Research track: ML-flavoured implementation |
| Technical exercises (2-5 total, per official page) | Mix of live coding, pair programming, deep-dive discussion | See track split below |
| - LLM deep-dive | Structured discussion / quiz | Transformer internals, attention variants, MoE, inference optimization; applied track gets RAG vs fine-tuning judgment (reported, varies) |
| - Pair programming | Build with the Mistral API + a third-party API | API fluency, context-enrichment design, error handling, working style (reported by an applied-AI candidate; varies) |
| - System design | Whiteboard | LLM serving at scale, training-cluster design, or customer RAG/agent architecture depending on track (reported, varies) |
| Project / culture round | Present a project you've worked on | Ownership, engineering judgment, communication (Glassdoor-reported) |
| Values conversation | Discussion | Alignment with audacity, rigor, customer centricity, speed, low-ego (official) |
| Reference checks | - | Standard (official) |

Timeline reports vary widely - Glassdoor's average is around two weeks, but some candidates report scheduling churn stretching it much longer. One caveat worth knowing: at least one public negative report describes unclear assessment criteria and interviewer no-shows, so ask your recruiter directly what each round evaluates.

## What they emphasize

- **Model internals as shipped, not as taught.** Their differentiation came from architecture-level efficiency (GQA, sliding-window attention, sparse MoE). Interviews reportedly probe these at tensor level - implement it, not just name it.
- **Inference economics.** Open-weight + enterprise self-hosting means customers run the models; KV-cache math, batching, and quantization are product concerns, not niche infra trivia.
- **Pragmatic API/product craft (applied track).** The customer-facing org lives in fine-tuning jobs, RAG pipelines, and integration code. Reported rounds test refactoring and building against their real API under pair-programming conditions.
- **Open-weights conviction and EU context.** Expect culture-round questions about why open models matter strategically, and expect enterprise conversations to touch data residency and European regulatory awareness (the EU AI Act shapes their customers' requirements).
- **Lean-team ownership.** Their values page explicitly asks for builders comfortable with ambiguity, directness, and low-ego collaboration. "I only do modelling" reads poorly; end-to-end ownership reads well.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Mistral 7B shipped with grouped-query attention and sliding-window attention. What does each buy you, and what does each cost?

<details><summary><b>Answer</b></summary>

They attack two different bottlenecks. **GQA** attacks KV-cache memory and bandwidth at inference: instead of one K/V head per query head (32 in Mistral 7B), groups of query heads share a smaller set of KV heads (8). KV-cache size scales with KV heads, so this is a 4× reduction - from ~512 KB to ~128 KB per token at fp16 - which directly increases the batch size and context length a GPU can serve. Cost: slightly less expressive attention than full MHA, but empirically near-zero quality loss at this grouping ratio, which is why it's now the default in most open models.

**Sliding-window attention** attacks the quadratic cost of long contexts: each layer attends only to the last W tokens (4096 in Mistral 7B). Compute per token becomes O(W) instead of O(n), and with a rolling-buffer KV cache, memory is capped at W tokens per sequence regardless of context length. Information still propagates beyond the window because each layer's receptive field stacks - after L layers, a token can be influenced by roughly W×L positions back. Cost: direct long-range attention is gone; retrieval-style tasks that need exact attention to a token 30k positions back can degrade, which is why later models mix full-attention and windowed layers or drop SWA when long-context recall is the priority.

The shared theme - and the answer interviewers want - is that both are inference-economics decisions made at architecture time.

**Follow-ups:** Why does KV-cache bandwidth, not FLOPs, dominate decode latency? What breaks if you apply the rolling buffer but forget to keep positions consistent (RoPE) across the wrap-around?

</details>

### 2. Implement causal multi-head attention in PyTorch, then convert it to grouped-query attention.

<details><summary><b>Answer</b></summary>

The core, with the GQA change isolated to one line of head bookkeeping plus a `repeat_interleave`:

```python
import torch, torch.nn.functional as F

def gqa(x, wq, wk, wv, wo, n_heads, n_kv_heads):
    B, T, D = x.shape
    hd = D // n_heads
    q = (x @ wq).view(B, T, n_heads, hd).transpose(1, 2)      # B,H,T,hd
    k = (x @ wk).view(B, T, n_kv_heads, hd).transpose(1, 2)   # B,Hkv,T,hd
    v = (x @ wv).view(B, T, n_kv_heads, hd).transpose(1, 2)
    # expand KV heads to match query heads (each KV head serves a group)
    rep = n_heads // n_kv_heads
    k = k.repeat_interleave(rep, dim=1)
    v = v.repeat_interleave(rep, dim=1)
    att = (q @ k.transpose(-2, -1)) / hd**0.5
    mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1)
    att = att.masked_fill(mask, float("-inf"))
    out = F.softmax(att, dim=-1) @ v                          # B,H,T,hd
    return out.transpose(1, 2).reshape(B, T, D) @ wo
```

Standard MHA is the special case `n_kv_heads == n_heads`; MQA is `n_kv_heads == 1`. Points that get probed: causal mask via `triu` with `diagonal=1` (mask strictly-future, not the diagonal), scaling by head dim not model dim, and where the savings actually live - `wk`/`wv` are `D × (n_kv_heads*hd)`, and at inference you cache k/v *before* the repeat, so the cache shrinks by `n_heads/n_kv_heads`. Mention that `repeat_interleave` materializes copies and production kernels avoid it by indexing, and that real code would use `F.scaled_dot_product_attention` for fused kernels.

**Follow-ups:** Add a KV cache and write the single-token decode path. Where does RoPE get applied and why to q and k only?

</details>

### 3. Explain how a Mixtral-style sparse mixture-of-experts model works. Why does a model with ~47B parameters run at the cost of a ~13B one?

<details><summary><b>Answer</b></summary>

In Mixtral 8x7B, the attention layers are ordinary; the FFN in each transformer block is replaced by 8 expert FFNs plus a small router. For every token at every layer, the router (a linear layer over the hidden state) scores all 8 experts, picks the **top 2**, and the block's output is the softmax-weighted sum of those two experts' outputs. Total parameters are ~46.7B because you store all 8 experts per layer, but each token only executes 2 of them, so active parameters per token are ~12.9B - decode FLOPs and speed resemble a 13B dense model while quality benefits from the larger parameter pool.

The catch is that the economics are asymmetric. FLOPs scale with active params, but **memory scales with total params**: you must hold all 47B weights in VRAM (or shuffle experts, which murders latency). So MoE buys quality-per-FLOP, not quality-per-GB - great when you're bandwidth/compute-bound with memory to spare, bad for single consumer GPUs.

Training adds two classic problems. **Load balancing:** left alone, routers collapse onto a few favoured experts; an auxiliary load-balancing loss penalises uneven expert utilisation to keep all experts trained and hardware evenly used. **Routing non-differentiability and instability:** top-k selection is discrete, gradients flow only through the selected experts' weights, and expert-parallel training needs all-to-all communication to ship tokens to whichever device holds their expert - a systems and stability tax dense models don't pay.

**Follow-ups:** Why is batched inference harder for MoE than dense models (expert imbalance within a batch)? When would you recommend a dense model over an MoE to a customer self-hosting on limited VRAM?

</details>

### 4. Estimate the KV-cache memory for serving Mistral 7B, and design the rolling-buffer cache that sliding-window attention enables.

<details><summary><b>Answer</b></summary>

Per-token KV cache = 2 (K and V) × layers × kv_heads × head_dim × bytes. For Mistral 7B at fp16: 2 × 32 × 8 × 128 × 2 = **131,072 bytes ≈ 128 KB per token**. A 4,096-token sequence costs ~512 MB; 30 concurrent sequences at that length ≈ 15.7 GB - more than the ~14 GB of bf16 weights. That comparison is the punchline: at realistic batch sizes, *cache, not weights, is the capacity constraint*, which is why GQA (already a 4× cut vs. 32 KV heads) and cache-aware schedulers like vLLM's paged attention exist.

Sliding-window attention caps what you need to remember: a token only ever attends to the previous W = 4096 positions, so the cache can be a fixed ring buffer of W slots per layer. Write position is `pos % W`; once you've generated more than W tokens, new entries overwrite the oldest. Two implementation details matter. First, positional consistency: with RoPE applied to q/k before caching, the stored k's rotation must correspond to its absolute position, and attention must use true positions - you can't renumber slots after wrap-around. Second, the attention mask during prefill of long prompts must combine causal + window constraints, and chunked prefill has to handle the boundary where part of the window lives in the previous chunk.

Result: memory per sequence is O(W), constant in total generation length - which turns "context length" from a memory question into a purely quality question.

**Follow-ups:** How does paged attention interact with a ring buffer? What changes for Mixtral (same attention, so same cache math - but why do people assume otherwise)?

</details>

### 5. A customer has 2,000 pages of internal PDFs and wants an assistant that answers questions over them. Fine-tune or RAG? Walk me through the decision.

<details><summary><b>Answer</b></summary>

RAG, almost certainly - and the reasoning matters more than the verdict. Fine-tuning teaches *behaviour* (style, format, task procedure, domain vocabulary); it is unreliable for injecting *facts*, and knowledge baked into weights can't be updated per document, cited, or access-controlled. 2,000 pages is also tiny by pretraining standards but expensive to turn into good instruction-tuning data. RAG keeps facts in a store you can update instantly, gives you citations for trust, and lets you enforce per-user document permissions at retrieval time - usually non-negotiable for enterprise.

The honest answer also names when fine-tuning enters: (a) the model keeps failing at the *form* of the task - domain jargon, required output schema, tone - even with retrieved context present; (b) you want a smaller, cheaper model to match a bigger one's behaviour on this narrow task; (c) latency/cost pressure argues for shorter prompts than few-shot examples allow. In practice the mature answer is RAG first, measure, then fine-tune the generator on top of RAG traces if quality gaps are behavioural. They're complements, not rivals.

Then show system judgment: PDF parsing quality (tables, scans → OCR) usually dominates outcomes; chunking with structure awareness; hybrid retrieval (BM25 + embeddings) with a reranker; and a golden Q&A set (even 50 questions) to measure retrieval hit rate and answer faithfulness before and after any change. Committing to fine-tuning without an eval set is the anti-pattern the question hunts for.

**Follow-ups:** The customer insists on fine-tuning because "we don't want our data leaving in prompts" - how do you respond? How do you evaluate faithfulness cheaply?

</details>

### 6. What does it take, memory-wise, to fine-tune a 7B model? Compare full fine-tuning, LoRA, and QLoRA.

<details><summary><b>Answer</b></summary>

Rule of thumb for full fine-tuning with AdamW in mixed precision: **~16 bytes per parameter** of state - bf16 weights (2) + bf16 gradients (2) + fp32 master weights (4) + fp32 Adam first and second moments (4 + 4). For 7B that's ~112 GB before activations, so a single 80 GB GPU can't do it naively; you're into multi-GPU sharding (FSDP/ZeRO-3 splits weights, grads, and optimizer state across devices), plus activation checkpointing to trade compute for activation memory.

**LoRA** freezes the base model (bf16, ~14 GB) and trains low-rank adapters ΔW = BA (rank 8-64) injected into attention/MLP projections - typically well under 1% of parameters. Gradients and optimizer states exist only for adapters, so total footprint is roughly weights + activations + a rounding error: a single 80 GB GPU handles it comfortably, or a 24 GB card with care. **QLoRA** additionally quantizes the frozen base to 4-bit (NF4, ~3.5-4 GB for 7B) and dequantizes on the fly for forward/backward, putting 7B fine-tuning on a single consumer GPU - at the price of slower steps and a small quality gap on some tasks.

Selection logic for a customer: QLoRA to prototype cheaply; LoRA for most production fine-tunes (adapters are also swappable per-tenant on one serving base - operationally elegant); full fine-tuning when you're making deep behavioural changes, doing continued pretraining on domain corpora, or the last quality points justify a GPU cluster.

**Follow-ups:** Why is fp32 master-weight storage kept in mixed-precision training? What batch-size/sequence-length terms drive activation memory?

</details>

### 7. Design an on-prem deployment of an open-weight model for a European bank that cannot send data to any external API.

<details><summary><b>Answer</b></summary>

This is Mistral's home turf, so treat it as a real product design, not a toy. Requirements first: workloads (assistant? document processing? code?), concurrency and latency targets, the bank's GPU reality (often a handful of A100/H100 nodes, not a cloud fleet), and compliance constraints - data residency, audit logging, model-risk documentation (EU AI Act obligations for the bank as a deployer, plus internal model governance).

Architecture: model weights and inference entirely inside the bank's network. An inference layer (vLLM or an enterprise serving stack) with continuous batching and paged KV cache; model choice sized to hardware - a small dense model or MoE depending on VRAM (MoE needs total-params memory, see Q3). In front of it: a gateway providing authn/z, per-team quotas, full request/response audit logging to the bank's SIEM, and PII redaction hooks. RAG components (embedding model, vector store) must equally be self-hosted - teams forget the embedding API is also an external call. Fine-tuned adapters per department can share one base model via LoRA hot-swapping.

Operations is where such deployments die: you own model upgrades (pin versions, re-run eval suites before swapping), capacity planning (KV-cache math from Q4 decides concurrent users per node), monitoring (TTFT, tokens/sec, GPU utilisation, plus quality drift on a golden set), and an incident story for hallucination-with-consequences (human-in-the-loop for customer-facing outputs). Offline eval sets built from the bank's real tasks are your only quality instrument - no vendor dashboard is coming to save you.

**Follow-ups:** The bank has 4×A100 80GB total - what model and quantization do you pick and how many concurrent users does that support? How do you handle model updates without regressions?

</details>

### 8. Why does continuous batching outperform static batching for LLM serving? What are the tradeoffs?

<details><summary><b>Answer</b></summary>

Static batching forms a batch of requests, runs them together, and returns when *all* finish. Generation lengths vary wildly, so short requests wait for the longest one - padded, wasted compute - and new arrivals wait for the whole batch to drain. GPU utilisation craters and tail latency inflates.

Continuous (iteration-level) batching reschedules at every decode step: each step, the engine runs one forward pass over the union of all active sequences; finished sequences exit immediately and queued requests join immediately (their prefill is chunked in alongside others' decode). The GPU always works on a full batch, so throughput improves severalfold in mixed-length workloads - this is the core idea behind vLLM, TGI, and TensorRT-LLM schedulers, and it composes with paged KV cache, which makes admission cheap by eliminating contiguous cache pre-allocation.

Tradeoffs to name: (1) **TTFT vs. inter-token latency** - admitting new prefills into a running batch steals compute from decoding, adding jitter to existing streams; chunked prefill and prefill/decode-priority policies tune this. (2) **Memory admission control** - batch size is bounded by KV-cache capacity, which grows per step; overcommit and you must preempt (swap or recompute) sequences mid-generation. (3) **Fairness/SLOs** - pure throughput scheduling starves long requests; production systems need priority queues. (4) MoE models complicate it further because per-token expert routing makes per-step cost uneven across a batch.

The interview signal: you think in tokens/sec/GPU *and* p95 TTFT simultaneously, and you know they fight each other.

**Follow-ups:** How does speculative decoding interact with a continuous-batching scheduler? What metric would you alert on to detect cache thrashing?

</details>

### 9. You need to quantize a model for a customer's hardware. How do you choose a scheme, and how do you prove quality hasn't regressed?

<details><summary><b>Answer</b></summary>

Choose by hardware and bottleneck. Decode is memory-bandwidth-bound, so **weight-only int4** (AWQ/GPTQ-family) is the workhorse: ~4× smaller weights, faster decode, runs on older GPUs. On H100-class hardware, **fp8** (weights + activations, sometimes KV cache) keeps near-lossless quality with tensor-core speedups and is the low-drama default. Under extreme memory pressure, quantize the **KV cache** too (int8/fp8) - often the bigger win at long contexts (Q4 math). Aggressive schemes below 4-bit are a last resort; quality falls off a cliff unevenly.

Proving no regression is the part most engineers do badly, and the part a customer-facing Mistral engineer must own. Perplexity deltas are necessary but insufficient - quantization damage is task-uneven, hitting math, code, and long-context recall hardest while leaving casual chat intact. So: (1) run the customer's **golden task set** (their real prompts, graded) before/after - this is the contract; (2) run capability probes in the damage-prone areas (reasoning, extraction fidelity, multilingual if relevant - outlier-sensitive layers can degrade non-English disproportionately); (3) do a **paired diff review**: same prompts, both models, human or LLM-judge comparison on a few hundred cases, looking for behavioural drift not just accuracy; (4) check calibration-set bias - AWQ/GPTQ use calibration data, and unrepresentative calibration (English-only web text for a French legal customer) skews what gets preserved.

Ship with a rollback path and per-scheme version pinning; "int4 broke the invoice extractor" should be a one-config revert.

**Follow-ups:** Why does weight-only quantization speed up decode but barely help prefill? When would you serve two precisions of the same model behind a router?

</details>

### 10. Pair-programming: build a service that takes a user question, enriches it with data from a third-party API, and answers via a chat-model API. How do you structure it?

<details><summary><b>Answer</b></summary>

This mirrors the applied-track pair-programming round, and the evaluation is engineering craft, not cleverness. Structure it in layers with seams for testing:

```python
@dataclass
class Enrichment:
    source: str
    content: str
    fetched_at: datetime

class WeatherClient:          # third-party API behind an interface
    def lookup(self, query: str) -> Enrichment | None: ...

class Answerer:
    def __init__(self, llm: LLMClient, enrichers: list):
        self.llm, self.enrichers = llm, enrichers

    def answer(self, question: str) -> Answer:
        ctx = [e for c in self.enrichers if (e := c.lookup(question))]
        prompt = render_prompt(question, ctx)   # pure function -> testable
        return self.llm.chat(prompt)
```

Things to do *out loud*: define the enrichment interface first so the third-party client is swappable and mockable; make prompt construction a pure function you can unit-test; treat the enricher as optional - on timeout or error, degrade to answering without enrichment (with a caveat in the prompt) rather than failing the request. Add timeouts and bounded retries with backoff on both APIs, but never retry non-idempotent operations blindly. Validate and truncate third-party payloads before they enter the prompt - token budget and prompt-injection hygiene (the API response is untrusted content; label it as data in the prompt). Log the full trace (question, enrichments, prompt, response, latencies) because that trace *is* your future eval set.

One public rejection report cited the candidate's "skills with APIs were not meeting their expectations," which suggests fluency matters: read error responses, handle pagination/auth cleanly, don't fight the SDK.

**Follow-ups:** The third-party API rate-limits you at 10 rps - what changes? How would you eval whether enrichment actually improves answers?

</details>

### 11. How does function calling actually work with an LLM, and how do you make it reliable enough for production agents?

<details><summary><b>Answer</b></summary>

Mechanically: you send tool schemas (name, description, JSON-schema parameters) alongside the conversation; the model is fine-tuned to emit either prose or a structured tool-call (name + JSON arguments); *your* runtime executes the tool and appends the result as a tool-role message; the model then continues - an agent is just this loop with state. The model never executes anything; it proposes. That distinction drives the whole reliability story.

Failure modes and their mitigations: **malformed or hallucinated calls** (wrong tool name, invalid JSON, fabricated params) → validate every call against the schema, use constrained decoding/JSON mode where the API supports it, and return machine-readable errors to the model so it can self-correct - one retry with the validation error appended fixes a large share. **Wrong tool selection** → fewer, better-described tools beat many overlapping ones; descriptions are prompts, so write them like docs with examples; measure selection accuracy on a labelled set. **Loops and runaway cost** → hard cap on iterations, budget tracking, and a terminal "give up and ask the user" path. **Side effects** → make tools idempotent where possible, and gate irreversible actions (send, delete, pay) behind confirmation rather than trusting the model's judgment.

Production hardening: log every step of every trajectory; build evals at two levels - per-step (was this call correct given the state?) and end-to-end task success; and pin model versions, because tool-calling behaviour shifts across model updates more than prose quality does. Smaller open models can do reliable function calling, but they need tighter schemas and more aggressive validation than frontier models.

**Follow-ups:** Parallel tool calls - when do they help and what do they break? How do you regression-test an agent before a model upgrade?

</details>

### 12. After fine-tuning on a customer's task, target-task accuracy is up but the model got worse at everything else. What happened and what do you do?

<details><summary><b>Answer</b></summary>

Catastrophic forgetting: gradient updates concentrated on a narrow distribution have overwritten capabilities the base model encoded elsewhere. It's the default outcome of enthusiastic fine-tuning, not an anomaly - and the first question is whether it even matters. If the model serves *only* this task behind an API, some general-capability loss is acceptable; if it backs a general assistant, it's a launch blocker. Scope the requirement before engineering.

Diagnosis: run a held-out general suite (instruction following, reasoning, safety refusals, and - relevant for Mistral's market - the customer's other languages) before and after; forgetting is typically uneven, and safety behaviours and multilingual ability are notoriously fragile. Check the training config for the usual culprits: learning rate too high, too many epochs over a small dataset (memorisation), or a dataset that's 100% one format so the model collapses into that format for every input.

Mitigations, in the order I'd try them: (1) **LoRA instead of full fine-tuning** - low-rank updates constrain how far you move from the base, and you can lower rank/alpha to dial intervention strength; (2) **mix replay data** - blend 5-20% general instruction data into the training set so gradients keep general behaviours alive; (3) **shorter training, lower LR, early stopping on both curves** - target-task metric *and* general-suite metric; (4) if the base model can already do the task with good prompting + retrieved examples, question whether fine-tuning was the right tool at all (Q5 logic). Re-run the full eval matrix after every change; forgetting hides where you don't measure.

**Follow-ups:** Why are safety refusals particularly prone to being fine-tuned away, and what does that imply for customer fine-tuning platforms? What would you monitor post-deployment?

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - the single highest-leverage dir. Mistral's reported deep-dive rounds live here: attention variants (MHA/GQA/MQA), RoPE, sliding-window attention, MoE routing, tokenization. Be able to *implement*, not just describe.
2. **[08-inference-and-production](../08-inference-and-production/)** - KV-cache math, continuous batching, paged attention, quantization, speculative decoding. Open-weight + enterprise self-hosting makes inference economics a company-wide obsession.
3. **[04-rag-and-retrieval](../04-rag-and-retrieval/)** and **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - the applied-AI track's confirmed territory (a public candidate report includes "define RAG" and RAG-vs-fine-tuning for a large PDF corpus). Know LoRA/QLoRA memory math cold.
4. **[11-ai-system-design](../11-ai-system-design/)** - use the 8-step framework for "design LLM serving for an MoE model" and "design an on-prem enterprise deployment" prompts. Closest existing case study: **[content moderation pipeline](../11-ai-system-design/case-studies/05-content-moderation-pipeline.md)** - Mistral ships a moderation classifier as an API product, and every enterprise deployment they sell needs exactly this guardrail layer.
5. **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - function calling is a first-class feature of their models and platform; expect applied questions here.

Company-specific moves:

- **Read the Mistral 7B and Mixtral of Experts papers** (both on arXiv). They're short and unusually readable. Being fluent in GQA, sliding-window attention, the rolling-buffer KV cache, and top-2 expert routing covers a striking fraction of the reported technical deep-dive.
- **Build something real on La Plateforme** - function calling plus one third-party API, mirroring the reported pair-programming round. Fluency with their SDK, error handling, and structured outputs is directly what one candidate was rejected for lacking.
- **Run an open-weight Mistral model locally** (vLLM or llama.cpp) and quantize it. Speaking about int4-vs-fp16 tradeoffs from experience beats book knowledge in a lab that ships weights.
- **Prepare the culture round like a technical round**: a crisp project presentation with real ownership stories, plus substantive answers to "why open weights?", "why a European lab?", and questions mapped to their five published values (audacity, rigor, customer centricity, speed, low-ego).
- **Refresh practical pair-programming hygiene** - reported screens involve refactoring and collaborative coding, so practise thinking aloud and reading unfamiliar code fast.

## Sources

- [Mistral AI careers page](https://mistral.ai/careers/) - official process skeleton (intro conversations, 2-5 technical exercises, values conversation, reference checks) and published values
- [Mistral AI job board (Lever)](https://jobs.lever.co/mistral) - role titles and locations cited above
- [techinterview.org Mistral guide](https://www.techinterview.org/companies/mistral/) - third-party prep guide; stage breakdown and technical focus areas (unofficial)
- [Dataford Mistral AI Engineer guide](https://dataford.io/interview-guides/mistral-ai/ai-engineer) - third-party prep guide; PyTorch implementation and LLM-theory round descriptions (unofficial)
- [Taro candidate experience, Applied AI Engineer, Oct 2025](https://www.jointaro.com/interviews/companies/mistral-ai/experiences/applied-ai-engineer-france-october-15-2025-no-offer-negative-5a1aac6b/) - single public candidate report (refactoring screen, RAG/fine-tuning discussion, Mistral-API pair programming)
- [Glassdoor Mistral AI interviews](https://www.glassdoor.com/Interview/Mistral-AI-Interview-Questions-E9945031.htm) - aggregated candidate reviews (project presentation, live coding, system design, values rounds; timeline reports)
