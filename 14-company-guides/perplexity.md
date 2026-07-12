# 🔍 Perplexity - AI Engineer Interview Guide

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- **The loop is short and officially documented.** Perplexity publishes its own interview guide: recruiter screen → technical screen ("a standard technical programming interview" for engineers) → onsite of 4-5 interviews including a hiring-manager deep dive → a final conversation with a founder or leader → decision within about a week of the onsite. Publicly reported end-to-end times are among the fastest anywhere - often under two weeks.
- **Python, practical, production-flavoured.** Candidate reports converge on Python-first coding rounds built around realistic problems - data streams, dedup, provider failover, batching - graded on working code and edge-case handling, not LeetCode trickery.
- **RAG-at-web-scale is the home turf.** System design rounds reportedly centre on exactly what they build: retrieval pipelines, LLM serving, ranking, and search infrastructure, with latency as a first-class constraint.
- **Product usage is checked, not assumed.** Multiple reports say "why Perplexity" is probed with the expectation that you've used the product seriously and have specific opinions about it.
- **Speed and ownership are the culture screen.** The company is publicly explicit about shipping velocity; behavioural evaluation (including the founder round) looks for people who drive decisions and ship without hand-holding.

## Company context

Perplexity builds an AI answer engine: conversational search that retrieves from a live web index and generates cited answers, plus the Sonar API for developers, enterprise offerings, and the Comet browser with agentic capabilities. For engineers, it is one of the clearest examples of "RAG as the entire company" - the retrieval pipeline, the ranking stack, the inference layer, and the product are the same system, serving hundreds of millions of queries with hard latency budgets. "AI engineer" there mostly means building and operating that pipeline - search infrastructure, LLM serving, orchestration, evaluation - rather than pretraining models, though they also hire research roles that post-train and optimise models (e.g., the Sonar family).

## Roles & titles they hire

Titles seen on their public careers page and job boards (roles and locations change; check the live listings):

- **Software Engineer** - Search, Backend, Product, Infrastructure variants
- **Member of Technical Staff (AI Inference Engineer)** - model serving and inference optimisation; posted in San Francisco and London
- **Research Engineer / AI Research Scientist** - model post-training, ranking, answer quality
- **Forward-Deployed Engineer - API Platform** - customer-facing engineering around the Sonar API
- **AI Research Residency** - an entry path into research roles (publicly advertised)

Hubs: San Francisco Bay Area, New York, London.

## The interview loop

Perplexity's own careers site hosts an interview guide describing the loop, and secondary reports are consistent with it. Round content below the stage level is candidate-reported and varies by team.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter screen | ~30-45 min call | Background, motivation, why Perplexity specifically, compensation fit; expect product-usage questions |
| Technical screen | ~45-60 min live coding, Python strongly preferred (official guide calls it "a standard technical programming interview" for engineers) | Working code on practical problems; reasoning out loud; edge cases |
| Onsite | 4-5 interviews, typically virtual (official guide) | Mix of coding, system design, and a hiring-manager deep dive on past work |
| - Coding rounds | Practical problems: streams, text processing, service components (reported, varies) | Production readiness, correctness under changing requirements |
| - System design | RAG/search/serving-flavoured design; sometimes infra debugging scenarios (reported, varies) | Retrieval + ranking + LLM pipeline thinking, latency budgets, failure modes |
| - HM deep dive | Detailed walkthrough of past projects (official guide: "be prepared to discuss past work and experience anecdotes in detail") | Ownership, real depth on systems you claim to have built |
| Founder/leader interview | Final conversation with a founder or senior leader (official guide) | Mission alignment, product opinions, velocity mindset |
| Decision | Within ~1 week of onsite (official guide); post-offer chats for team matching | - |

Publicly aggregated timelines range from ~11 to ~23 days end-to-end - fast by industry standards.

## What they emphasise

- **Latency as a value system.** Their product promise is a cited answer in seconds over a live index. Expect any design you propose to be interrogated on time-to-first-token, tail latency, and what you cut when the budget is blown.
- **Retrieval and ranking depth.** This is a search company. Hybrid retrieval, reranking, dedup, freshness, and context selection are not one interview topic among many - they are the substance of the job.
- **Production readiness over algorithmic flash.** Reported coding rounds reward handling failure: timeouts, retries, degraded modes, provider outages. Code that "works on the happy path" undershoots.
- **Genuine product engagement.** Reports consistently mention being asked what you'd improve about Perplexity. Vague praise is a negative signal; a specific, measurable critique is a strong one.
- **Shipping velocity and ownership.** A small team serving enormous traffic means they select for people who make decisions, ship, and own outcomes - probed in the HM deep dive and founder round.
- **Python fluency.** Multiple independent reports: do the interviews in Python unless you have a strong reason not to.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Design an answer engine: a user types a question and gets a cited, streamed answer. Your end-to-end budget is 3 seconds to a complete short answer.

<details><summary><b>Answer</b></summary>

Pipeline: query understanding → parallel retrieval → rerank → LLM synthesis with inline citations - with stages overlapped, because sequential execution blows the budget.

**Query understanding (<100 ms):** classify intent (fresh/news, navigational, deep research) with a small model or rules; rewrite the question into 2-4 search queries. This routing decides index tier, cache TTL, and model choice.

**Retrieval (~300-600 ms):** fan out the rewritten queries in parallel against your index/search backends; take top ~30-50 candidates. Serve page content from a parsed-content cache - fetching and parsing live HTML at query time is a tail-latency disaster, so it's only a fallback. Hedge stragglers: proceed when, say, 80% of fanout returns.

**Rerank (~100-200 ms):** cross-encoder or lightweight scorer over candidates; select ~8-12 passages into the context budget, deduped and diversity-adjusted.

**Synthesis:** start prefill the moment top passages land; stream tokens immediately so perceived latency is time-to-first-token (~1 s target), not total time. Citations are generated as inline markers bound to source IDs present in the context.

**Cross-cutting:** query-level answer cache with intent-dependent TTL (minutes for news, days for stable facts); provider/model failover; graceful degradation (fewer sources, smaller model) instead of errors. Instrument every span - you cannot defend a 3 s budget without a trace waterfall.

**Follow-ups:** Where does this design break for "what happened in the last hour" queries? What changes if 30% of queries are follow-ups in an existing conversation?

</details>

### 2. You retrieved 50 candidate passages for a query but the model's useful context budget is ~10. How do you choose, and how do you know your choices are good?

<details><summary><b>Answer</b></summary>

Two-stage: cheap recall, expensive precision. First-stage retrieval should be hybrid - BM25 catches exact terms (names, error codes, dates) that dense embeddings blur; dense catches paraphrase. Fuse with reciprocal rank fusion (RRF) so you don't have to calibrate score scales against each other.

Then rerank the fused 50 with a cross-encoder, which reads query and passage jointly and is far more accurate than bi-encoder similarity - affordable at 50 candidates (tens of ms batched on GPU), ruinous at 50,000. On top of raw relevance apply: near-dup suppression (five copies of the same syndicated article waste 40% of the budget), source diversity (MMR or a per-domain cap), and freshness boosts for time-sensitive intents.

Ordering matters too: models attend better to the start and end of context ("lost in the middle"), so place the strongest passages at the edges.

Knowing it's good: offline, a labelled set measuring recall@10 and nDCG against human or carefully calibrated LLM-judge relevance labels; answer-level ablations (does swapping ranker A for B change groundedness and answer quality?); online, interleaving experiments or A/Bs reading downstream signals - citation click-through, follow-up-query rate, thumbs. The trap is optimising passage-level relevance metrics that don't move answer quality; the rerank stack should be evaluated end-to-end at least as often as component-wise.

**Follow-ups:** Your cross-encoder adds 150 ms p95 - when is that worth it and when do you distill it into the bi-encoder? How do you handle queries where the 50 candidates are all bad?

</details>

### 3. How do you ensure every claim in a generated answer is actually supported by its cited source?

<details><summary><b>Answer</b></summary>

You can't fully prevent it at generation time, so treat it as generate-then-verify plus measurement.

**Generation side:** constrain the model to cite from the provided source set only - sources get short IDs in context, and the decoder emits citation markers referencing them. Prompt for "answer only from the sources; say so if they don't cover it." This eliminates fabricated URLs but not the subtler failure: a real citation attached to a claim the source doesn't support.

**Verification side:** run an entailment check per claim - split the answer into sentences, and for each cited sentence ask an NLI model or small LLM whether the cited passage supports it. Score as citation precision (fraction of cited claims actually supported) and citation recall (fraction of claims that carry a citation). This can run async for monitoring, or inline for high-stakes queries at a latency cost; a distilled classifier makes inline checking affordable.

**Product side:** honesty beats fluency - when retrieval is thin, saying "sources disagree" or "I couldn't find reliable coverage" is the correct output, and your prompts and evals must reward it rather than punish the shorter answer.

**Measurement:** track citation precision/recall on a golden set per release, plus online proxies like citation click-and-return behaviour. Regressions here are release blockers, because unsupported-but-cited claims are worse than uncited ones - the citation launders false confidence.

**Follow-ups:** A sentence synthesises facts from three sources - how does per-claim verification handle multi-source composition? What's your fallback when the verifier and generator disagree at serving time?

</details>

### 4. How does an answer engine handle breaking news - a query about something that happened 20 minutes ago?

<details><summary><b>Answer</b></summary>

Freshness is a pipeline property; no single component fixes it.

**Detect recency intent.** Classify queries: explicit time markers ("today", "latest"), entities with active news cycles, or spiking query clusters. This classification drives everything downstream - index tier, cache policy, ranking weights.

**Tiered indexing.** A general web index refreshed on a crawl schedule can't do 20 minutes. You need a fast tier - news feeds, sitemaps, high-churn domains - ingested and indexed within minutes, queried alongside (or instead of) the main index for recency-flagged queries. Budget-wise, the fast tier is small; the trick is routing the right queries to it.

**Cache discipline.** Answer caches are the silent staleness bug: a cached "who won the game" from an hour ago is confidently wrong. TTL must be a function of query class - minutes (or bypass entirely) for breaking topics, days for stable facts.

**Ranking and synthesis.** Boost recency for these queries, but authority still matters - early reporting conflicts, and the model should attribute rather than adjudicate: "as of [time], X reports..., while Y reports...". Timestamps belong in the context so the model can reason about them, and in the answer so the user can.

**Failure honesty.** If the fast tier has nothing yet, say the event is too recent for reliable coverage rather than filling from stale context.

**Follow-ups:** How do you detect that a previously stable query has "gone hot" so you can invalidate its cache? How would you evaluate freshness quality continuously?

</details>

### 5. p95 time-to-first-token on answers regressed from 1.2 s to 3 s after a release. Walk me through finding and fixing it.

<details><summary><b>Answer</b></summary>

First, refuse to guess - get the trace waterfall. TTFT decomposes into: queue/routing → query understanding → retrieval fanout → rerank → prompt assembly → prefill → first token over the network. Per-span p50/p95 before and after the release localises the regression in minutes; without tracing you're doing archaeology.

Likely culprits by span:

- **Retrieval fanout:** a straggling backend drags p95 while p50 looks fine. Fix with tighter per-backend timeouts, hedged requests, and "proceed at N% complete."
- **Prompt assembly/prefill:** the most common self-inflicted wound - someone added sources or verbose instructions, prompt tokens grew 2-3×, and prefill is roughly linear in prompt length. Diff token counts across releases; trim context, and use prefix caching so static instruction blocks aren't re-prefilled per request.
- **Serving:** batch-scheduler contention between prefill and decode phases, KV-cache pressure causing queueing, or a quiet model/config swap. Check the inference layer's queue-time metric separately from compute time.
- **Rerank:** batch size or model change; 50→150 ms here is invisible in averages, visible at p95.

Note what *doesn't* help: speculative decoding accelerates decode throughput, not TTFT. The TTFT levers are shorter prompts, prefix caching, faster retrieval overlap, and starting prefill before the full context is finalised.

Then prevent recurrence: per-span latency budgets asserted in CI/canary, and token-count diffs surfaced in release review.

**Follow-ups:** p50 is unchanged and only p95 regressed - what does that tell you? How do you set per-span budgets when teams own different spans?

</details>

### 6. Implement a client pool over multiple LLM providers with failover: providers fail, time out, or rate-limit, and callers should just get a completion.

<details><summary><b>Answer</b></summary>

Core pieces: priority-ordered providers, per-provider health tracking, timeouts, and failover on retryable errors.

```python
import time, random

class Provider:
    def __init__(self, name, client, priority):
        self.name, self.client, self.priority = name, client, priority
        self.failures, self.open_until = 0, 0.0

    def available(self):
        return time.monotonic() >= self.open_until

    def record(self, ok):
        if ok:
            self.failures = 0
        else:
            self.failures += 1
            if self.failures >= 3:  # circuit opens
                backoff = min(60, 2 ** self.failures)
                self.open_until = time.monotonic() + backoff

class LLMPool:
    def __init__(self, providers, timeout=10.0):
        self.providers = sorted(providers, key=lambda p: p.priority)
        self.timeout = timeout

    def complete(self, prompt, **kw):
        errors = []
        for p in (x for x in self.providers if x.available()):
            try:
                resp = p.client.complete(prompt, timeout=self.timeout, **kw)
                p.record(True)
                return resp
            except (TimeoutError, RateLimitError, ServerError) as e:
                p.record(False)
                errors.append((p.name, e))
            except BadRequestError:
                raise  # our bug; failover won't fix it
        raise AllProvidersFailed(errors)
```

The judgment calls interviewers listen for: classify errors - 429/5xx/timeouts fail over, 4xx-your-fault does not; circuit-break so a dead provider stops eating its timeout on every request; add jitter if you retry the same provider. Extensions worth naming: async with `asyncio`, streaming (failover only before first token; mid-stream needs restart semantics), per-provider concurrency caps, and cost/latency-aware routing rather than static priority.

**Follow-ups:** How does failover interact with streaming responses already half-sent to the user? How would you test the circuit-breaker behaviour deterministically?

</details>

### 7. You're ingesting millions of web pages a day. Detect near-duplicates - same article, different boilerplate - efficiently.

<details><summary><b>Answer</b></summary>

Exact duplicates are trivial - hash normalized main content (after boilerplate extraction; this step matters more than the hashing). Near-duplicates need similarity-preserving signatures, because pairwise comparison at millions/day is O(n²) and dead on arrival.

**SimHash:** tokenize into shingles (word 3-5-grams), hash each to 64 bits, sum weighted ±1 per bit position, take the sign - a 64-bit fingerprint where similar documents differ in few bits. Near-dup ⇒ Hamming distance ≤ 3. Indexing trick: split 64 bits into 4 blocks of 16; any pair within distance 3 shares at least one exact block, so build 4 hash tables keyed by block, and candidate lookup is 4 exact-match probes instead of a scan. This is the classic web-crawl approach - tiny footprint (8 bytes/doc), fast, well-suited to "syndicated article with different chrome."

**MinHash + LSH** is the alternative when you care about Jaccard similarity at tunable thresholds: k independent min-hashes over the shingle set, banded into LSH buckets; more memory, more flexibility on the similarity cutoff.

Pipeline shape: boilerplate-strip → shingle → SimHash → block-table probe → verify candidates with actual shingle overlap (the signature is a filter, not a verdict). Verification cost is fine because candidates are rare.

Where it matters downstream: dedup at index time saves storage and, critically, keeps the reranker's candidate list from being five copies of one wire story.

**Follow-ups:** How do you pick shingle size, and what breaks with unigrams? Same story rewritten by two outlets - different shingles, same facts: is that a dup, and whose problem is it?

</details>

### 8. From a high-volume query stream, maintain the top-k most frequent queries right now, with bounded memory.

<details><summary><b>Answer</b></summary>

Exact counting needs a counter per distinct query - unbounded. For bounded memory, two standard answers:

**Count-Min Sketch + heap:** a d×w matrix of counters, d hash functions; increment one counter per row, estimate = min across rows. Overestimates only (collisions inflate), never underestimates; error ≤ εN with w = ⌈e/ε⌉, δ failure probability with d = ⌈ln(1/δ)⌉. Keep a k-sized heap of candidates updated on each increment.

**Space-Saving** is simpler and often better for top-k:

```python
class SpaceSaving:
    def __init__(self, capacity):
        self.capacity = capacity
        self.counts = {}  # item -> (count, error)

    def add(self, item):
        if item in self.counts:
            c, e = self.counts[item]
            self.counts[item] = (c + 1, e)
        elif len(self.counts) < self.capacity:
            self.counts[item] = (1, 0)
        else:
            victim = min(self.counts, key=lambda x: self.counts[x][0])
            c, _ = self.counts.pop(victim)
            self.counts[item] = (c + 1, c)  # inherit min count, track error

    def topk(self, k):
        return sorted(self.counts.items(), key=lambda x: -x[1][0])[:k]
```

Guarantee: any item with true frequency > N/capacity is present; each count overestimates by at most its tracked error. Use capacity ≈ 10-100× k.

For "right now," add time decay: sliding windows of per-epoch sketches, or exponential decay on counts. Production note: shard by hash of query for parallelism, merge sketches (CMS merges by cell-wise addition) for the global view - this is how trending-query detection stays cheap.

**Follow-ups:** How do you merge Space-Saving summaries from 20 shards correctly? What changes if you need top-k per country?

</details>

### 9. You need to embed millions of text chunks. The embedding service takes batches with a max batch size and a max total-token limit. Write the batcher and make it fast.

<details><summary><b>Answer</b></summary>

Two separate wins: legal packing (respect both constraints) and throughput (minimise padding waste and keep the GPU busy).

```python
def make_batches(texts, token_counts, max_items, max_tokens):
    # Sort by length so batches are length-homogeneous: less padding,
    # since padded batch cost ~ len(batch) * max_len_in_batch.
    order = sorted(range(len(texts)), key=lambda i: token_counts[i])
    batches, cur, cur_tokens = [], [], 0
    for i in order:
        t = token_counts[i]
        if t > max_tokens:
            raise ValueError(f"item {i} exceeds token limit; split upstream")
        if cur and (len(cur) == max_items or cur_tokens + t > max_tokens):
            batches.append(cur)
            cur, cur_tokens = [], 0
        cur.append(i)
        cur_tokens += t
    if cur:
        batches.append(cur)
    return batches  # indices; caller preserves original order on write-back
```

Why sort by length: with padding, a batch costs `batch_size × longest_item`; mixing a 20-token chunk with a 500-token one wastes most of the compute. Length-sorted batches routinely give 2-5× effective throughput on skewed length distributions.

Then the systems layer, which is most of the real speed: pipeline with a bounded queue so tokenization/IO overlaps inference; N concurrent in-flight batches tuned to the service's concurrency limit; retries with per-item fallback (a poison item shouldn't kill its batch - bisect the batch to isolate it); checkpoint completed IDs so a crash at 80% doesn't restart at zero; and preserve input order or key results by stable ID.

**Follow-ups:** The service starts returning 429s under your concurrency - how does the batcher adapt? How would you dedupe identical chunks before embedding, and how much does that save on real corpora?

</details>

### 10. Implement beam search for an autoregressive model. When would an answer engine actually use it?

<details><summary><b>Answer</b></summary>

```python
import math

def beam_search(step_fn, bos, eos, beam=4, max_len=64, alpha=0.7):
    # step_fn(seq) -> list[(token, logprob)] for the next position
    beams = [([bos], 0.0)]
    done = []
    for _ in range(max_len):
        cand = []
        for seq, score in beams:
            for tok, lp in step_fn(seq):
                cand.append((seq + [tok], score + lp))
        cand.sort(key=lambda x: x[1], reverse=True)
        beams = []
        for seq, score in cand:
            if seq[-1] == eos:
                done.append((seq, score / (len(seq) ** alpha)))
            else:
                beams.append((seq, score))
            if len(beams) == beam:
                break
        if not beams:
            break
    done += [(s, sc / (len(s) ** alpha)) for s, sc in beams]
    return max(done, key=lambda x: x[1])[0]
```

Key details interviewers probe: scores are **sum of log-probs** (products underflow); finished hypotheses leave the active beam; **length normalization** (`score / len^α`) is mandatory or beam search systematically prefers short outputs; complexity is O(beam × vocab) sort work per step, and in a real implementation `step_fn` is a batched forward pass over all beams with per-beam KV caches - memory scales with beam width.

When to use it: beam search maximises approximate sequence likelihood, which pays off in closed-ended tasks - translation, constrained rewriting, short structured outputs. Open-ended answer generation mostly doesn't use it: it's beam×-expensive, and high-likelihood text is often degenerate and repetitive ("neural text degeneration"). Answer engines typically run greedy or low-temperature nucleus sampling with a KV cache. Where beam-like machinery shows up instead: query rewriting, structured extraction, and as the conceptual basis for speculative-decoding verification.

**Follow-ups:** Why does raw beam search favour short sequences, exactly? What does beam width 8 do to your KV-cache memory and TTFT?

</details>

### 11. How would you evaluate answer quality for an answer engine, continuously and at scale?

<details><summary><b>Answer</b></summary>

Layered, because no single measure survives contact with reality.

**Offline golden sets.** A few thousand queries stratified by intent (fresh/news, factual, how-to, ambiguous, adversarial), with graded rubrics per dimension: correctness, groundedness (claims supported by retrieved sources), citation precision/recall, completeness, refusal appropriateness. Refresh continuously - a static set rots as the query mix and the web shift.

**LLM-as-judge, calibrated.** Human labels for everything don't scale; LLM judges score every release cheaply but must be validated against a human-labelled subset (report agreement, e.g. Cohen's κ), use rubric-anchored prompts rather than "rate 1-10," and be checked for known biases - verbosity preference, position bias in pairwise comparisons (swap order and average), self-preference toward outputs of the same model family.

**Component metrics** so failures localise: retrieval recall@k and nDCG, reranker quality, groundedness verifier precision. An answer-level regression with healthy retrieval metrics points at synthesis; degraded recall points upstream.

**Online.** A/B tests reading behavioural proxies - follow-up/rephrase rate (rephrasing suggests the first answer failed), citation clicks, session retention, explicit feedback. Interleaving for ranking changes. Proxies are noisy individually; directionally consistent movement across several is the signal.

**Regression gating.** Golden-set evals in CI for prompt/model/retrieval changes, canary comparison in production, and an incident loop: every bad-answer report becomes a test case.

The senior insight: evals are the product spec. "Good answer" is defined operationally by this stack, so disagreements about quality get resolved by improving the eval, not by taste.

**Follow-ups:** Your LLM judge scores rose but user follow-up rate worsened - what happened? How do you evaluate answers to questions with no consensus ground truth?

</details>

### 12. You clearly use Perplexity - what's broken, and what would you ship to fix it?

<details><summary><b>Answer</b></summary>

This is a product-sense question wearing casual clothes, and reports suggest some version of it is common. The failure mode is generic flattery or a feature wishlist untethered from feasibility.

Strong structure: **specific observed failure → hypothesised cause in the pipeline → measurable fix → how you'd validate it.**

Example of the shape (substitute your own real observation): "Follow-up questions in long threads sometimes lose constraints I stated earlier - I asked for vegetarian restaurants, and three turns later got steakhouses. My guess: conversation context gets compressed or truncated during query rewriting for retrieval, dropping earlier constraints. I'd ship constraint extraction into a persistent structured state that's appended to every rewritten retrieval query, measure with a multi-turn golden set scoring constraint retention, and watch rephrase-rate on long sessions online."

That answer demonstrates: you actually use the product (specific, reproducible observation), you can map symptom → architecture (rewriting/context management), you think in shippable increments (state tracking, not "rebuild memory"), and you close the loop with measurement (offline set + online proxy).

Prepare two or three of these from real usage before interviewing - including at least one where you compare against a competitor (Google AI-mode results, ChatGPT search) and articulate where Perplexity wins or loses and why that's an engineering property (index freshness, citation UX, latency) rather than magic.

**Follow-ups:** Which of your proposed fixes is a prompt change vs a systems change, and how does that affect rollout risk? What would make you kill the feature after launch?

</details>

## How to prepare

Priority order for this repo, given Perplexity's focus:

1. **[04-rag-and-retrieval](../04-rag-and-retrieval/)** - the core of the job: hybrid retrieval, reranking, chunking, freshness, citation grounding. Go deepest here.
2. **[11-ai-system-design](../11-ai-system-design/)** - especially the **[semantic search case study](../11-ai-system-design/case-studies/04-semantic-search.md)**, the closest analogue to their product; the **[enterprise RAG assistant](../11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)** covers the cited-answer pipeline shape.
3. **[08-inference-and-production](../08-inference-and-production/)** - TTFT, streaming, KV/prefix caching, batching, failover; latency questions are near-certain.
4. **[12-coding-challenges](../12-coding-challenges/)** - practical Python under time pressure; their reported rounds are streams, text processing, and service components, not puzzle trivia.
5. **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - groundedness, citation metrics, LLM-judge calibration, online proxies.
6. **[02-llm-fundamentals](../02-llm-fundamentals/)** - decoding strategies, context handling; enough depth to implement (see beam search above).

Company-specific moves:

- **Read their official interview guide** at perplexity.ai/hub/careers/interview-guide - few companies document their loop; take the free information.
- **Use the product hard for two weeks.** Regular search, Deep Research, follow-up threads, the Sonar API if you can, Comet if available to you. Log concrete failures and delights; question 12 above is built from exactly this.
- **Build a toy answer engine** (search API → fetch/parse → rerank → streamed cited answer) and instrument per-stage latency. Nothing prepares you better for their system-design round than having felt the retrieval tail-latency problem yourself.
- **Do every practice problem in Python** - multiple independent reports say it's the expected language.
- **Skim their blog posts** on the Sonar models and pplx-api for how they talk about serving and model choices, and be ready to discuss the answer-engine competitive landscape (Google AI Overviews/AI Mode, ChatGPT search) in engineering terms.

## Sources

- [Perplexity - official interview guide](https://www.perplexity.ai/hub/careers/interview-guide) (confirmed to exist; page blocks automated fetching, so its contents are cited here as quoted by the search results and secondary sources below)
- [Perplexity - careers page](https://www.perplexity.ai/hub/careers)
- [JobsByCulture - Perplexity AI Interview Prep 2026](https://jobsbyculture.com/blog/perplexity-interview-prep-2026) (fetched)
- [LinkJob - 2026 Perplexity AI interview process and questions (candidate report)](https://www.linkjob.ai/interview-questions/perplexity-ai-interview/) (fetched)
- [Medium - "How I Actually Passed My 2025 Perplexity AI Interview" (candidate report)](https://medium.com/@anqi.silvia/how-i-actually-passed-my-2025-perplexity-ai-interview-actual-questions-4007209bce5b) (fetched)
- [Interview Query - Perplexity AI Software Engineer prep guide](https://www.interviewquery.com/prep-guides/perplexity-ai-software-engineer) (seen in search results; not fetched)
- [Glassdoor - Perplexity AI interview questions](https://www.glassdoor.com/Interview/Perplexity-AI-Interview-Questions-E8515634.htm) (seen in search results; not fetched)
