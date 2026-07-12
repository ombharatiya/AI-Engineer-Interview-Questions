# 🏗️ AI System Design

AI system design is now a standard interview loop stage for AI/GenAI/LLM engineer roles at frontier labs, big tech, and AI startups - usually a 45-60 minute whiteboard session like "Design a customer support agent" or "Design semantic search for our catalog." It tests whether you can turn a fuzzy product idea into a shippable, measurable, affordable system with a model inside it. Senior candidates fail this round more often on missing evals and cost math than on missing boxes in the diagram.

## How these interviews differ from classic system design

Classic system design intuitions still apply (load balancing, sharding, caching, queues), but four things change fundamentally:

| Dimension | Classic system design | AI system design |
|---|---|---|
| Core component | Deterministic services you write | A **model you don't fully control** - treated as a fallible, versioned dependency |
| Correctness | Provable: tests, invariants, ACID | **Probabilistic quality**: you can't prove correctness, so **evals replace correctness proofs** - you argue with measured accuracy, faithfulness, task success rates |
| Cost model | Mostly fixed infra; marginal request cost ≈ 0 | **Cost per request is significant** (fractions of a cent to dollars). Token math is the new capacity planning; model choice is a first-class cost lever |
| Latency | Single number (p99 of an RPC) | **Shaped latency**: time-to-first-token vs tokens/sec vs total; streaming UX; agent loops take seconds-to-minutes |
| Failure modes | Crashes, timeouts, data loss | Plus **semantic failures**: hallucination, prompt injection, refusal, drift after a silent model update |
| Iteration | Ship features | **Quality flywheel**: log traces → build eval sets → improve prompts/retrieval/models → re-measure |

If your answer would be identical with a deterministic service where the model sits, you're not answering an AI system design question.

## The 8-step answer framework

Use this skeleton for any prompt. In a 45-minute interview: ~5 min on step 1, ~10 min on steps 2-3, ~15 min on step 4, ~15 min on steps 5-8 (interviewers weight evals and ops heavily - don't run out of time before them).

### 1. Requirements & success metrics
Clarify users, scale (QPS, corpus size, growth), latency expectations, and **what "good" means numerically** - e.g. "answer accuracy ≥ 90% on a golden set, deflection rate ≥ 50%, p95 TTFT < 1.5s, cost < $0.05/query." Name the north-star metric and the guardrail metrics before drawing anything.

### 2. Model strategy
API vs self-host (data sensitivity, scale economics, latency control, ops burden), and **tiering**: route easy/high-volume traffic to a small cheap model, hard traffic to a frontier model. State fallbacks across providers and how you'll pin + upgrade model versions.

### 3. Data & context strategy
How does the model get the knowledge it needs? Default decision order: **prompting → RAG → tools → fine-tuning**. RAG for facts that change; fine-tuning for style/format/narrow skills, not knowledge freshness; tools for live state and actions. Define chunking, indexing, freshness pipeline, and ACLs here.

### 4. High-level architecture
Draw the request path: client → gateway → (router) → orchestration → retrieval/tools → model → guardrails → response, plus the offline paths (ingestion, eval, training). Say what's synchronous vs queued, what's cached, where state lives.

### 5. Evals & quality loop
The step that separates seniors: a **golden set** (100-1,000 labelled cases), automated scoring (exact-match where possible, LLM-as-judge with a rubric where not, calibrated against human labels), component-level metrics (retrieval recall@k separate from answer faithfulness), CI gating on prompt/model changes, and online A/B or interleaving.

### 6. Deployment & ops
Latency budget per stage, streaming, caching (prompt caching, semantic caching, KV cache implications), rate limits and provider quota management, graceful degradation (fallback model, "I don't know" responses, cached answers), tracing every LLM call with prompt/version/tokens/latency.

### 7. Safety & guardrails
Input guards (injection detection, PII redaction, topic filters), output guards (schema validation, citation checks, moderation), **action guards** for agents (allowlisted tools, spend/blast-radius caps, human approval for irreversible actions), and tenant isolation.

### 8. Iteration plan
What ships in week 1 vs quarter 1: start with the simplest system that can be measured (often a single prompt + retrieval), instrument everything, and let eval data drive complexity. Explicitly name what you would *not* build yet.

## Reusable building blocks

Most AI systems assemble the same ~10 blocks. Naming these fluently signals experience:

| Block | What it does | Design notes |
|---|---|---|
| **Model gateway** | Single choke point for all LLM calls: auth, quotas, retries, provider failover, usage metering | Buy or build thin; never let services call providers directly |
| **Router** | Sends each request to the right model tier (small/fast vs frontier) by classifier, heuristics, or task type | Biggest single cost lever; measure quality delta per tier |
| **Retrieval service** | Hybrid (BM25 + dense) search over chunked, permission-tagged corpus with reranking | Own service with its own evals (recall@k, nDCG) |
| **Context builder** | Assembles the prompt: system instructions, retrieved chunks, memory, tool schemas, under a token budget | Deterministic and testable; log the exact final prompt |
| **Orchestrator** | Runs multi-step flows: agent loops, tool dispatch, retries, timeouts, max-iteration caps | Durable execution (queue-backed) for long-running agents |
| **Guardrails layer** | Input/output/action checks: injection, PII, schema validation, moderation, policy engine for tool calls | Fail closed on actions, fail open (with logging) on style |
| **Eval harness** | Runs golden sets against any prompt/model/retrieval config; scores, diffs, gates CI | Version everything: prompts, datasets, judge prompts |
| **Tracing & observability** | Per-request trace of every model call, tool call, retrieval, with tokens/cost/latency/feedback attached | The raw material for eval sets and debugging |
| **Caches** | Exact-match response cache, semantic cache, provider prompt caching for shared prefixes | Prompt caching often cuts input cost 50-90% on long shared contexts |
| **Feedback store** | Thumbs, edits, acceptances, escalations, linked to traces | Feeds the quality flywheel and fine-tuning data |
| **Human-in-the-loop queue** | Review UI for low-confidence outputs and high-risk actions | Design the escalation path before the model is trusted |

## What interviewers grade

- **Clarifying questions first.** Jumping straight to an architecture is the most common fail. Scope, scale, quality bar, and constraints are never fully specified on purpose.
- **Tradeoff articulation.** Every choice ("RAG over fine-tuning", "self-host the completion model") stated with the alternative, the reason, and what would change your mind.
- **Eval literacy.** Can you say concretely how you'd know the system works - datasets, metrics, judges, online experiments? This is the sharpest senior/junior discriminator in 2026 loops.
- **Cost awareness.** Back-of-envelope token math: requests/day × tokens/request × $/token. Being within 10x with clearly stated assumptions is the bar.
- **Pragmatism.** Simplest thing first, complexity justified by measured need. "I'd start with one prompt and a golden set" beats a 12-box agent swarm.
- **Failure-mode thinking.** Injection, hallucinated citations, provider outage, silent model updates, stale indexes - raised unprompted.
- **Latency realism.** Knowing that TTFT, streaming, and agent loop counts dominate perceived speed, and budgeting per stage.

## Red flags interviewers watch for

- Designing for the model as an infallible oracle - no eval plan, no fallback, no "when it's wrong" path.
- Fine-tuning as the first answer to a knowledge-freshness problem.
- No numbers anywhere: no QPS, no token counts, no cost estimate, no latency budget.
- Agent maximalism: multi-agent swarms for a problem a single prompt + retrieval solves.
- Ignoring ACLs/tenancy in enterprise scenarios ("just embed everything into one index").
- Treating "LLM-as-judge" as free and infallible rather than a component that itself needs calibration.
- No mention of prompt injection when the design ingests untrusted content or takes actions.

## Rapid-fire practice prompts

Practice the 8-step skeleton on these until it's reflexive (one-liners on purpose - generating the clarifying questions is the exercise):

1. Design a company-wide knowledge assistant over wikis, docs, and tickets.
2. Design an AI coding assistant with inline completion, chat, and agentic edits.
3. Design a customer support agent that can look up orders and issue refunds.
4. Design semantic search for a 100M-item e-commerce catalog.
5. Design a content moderation system for user-generated posts at 10k posts/sec.
6. Design a document intelligence pipeline for invoices and contracts.
7. Design a natural-language-to-SQL analytics agent for business users.
8. Design a meeting assistant: transcription, summaries, action items, follow-up search.
9. Design an email triage and drafting assistant for a sales team.
10. Design a personalised news/feed summariser for 10M daily users.
11. Design an AI feature flag: roll out a new model to 5% of traffic safely.
12. Design a batch pipeline to classify and tag 500M legacy documents.
13. Design a voice agent for restaurant reservations end-to-end.
14. Design a code review bot for a 2,000-engineer monorepo.
15. Design an LLM gateway for a company with 40 teams calling 5 model providers.

## Case studies

Full worked solutions following a consistent template (problem → clarifications → requirements → architecture → deep-dives → data strategy → evals → cost math → failure modes → ops → follow-ups):

1. [Enterprise RAG Assistant](case-studies/01-enterprise-rag-assistant.md) - company-wide knowledge assistant: ACLs, freshness, citations, hybrid search, eval harness.
2. [AI Code Assistant](case-studies/02-ai-code-assistant.md) - IDE completion + chat + agents: latency tiers, FIM, repo context, privacy, acceptance-rate evals.
3. [Customer Support Agent](case-studies/03-customer-support-agent.md) - tool-using agent over orders/refunds: action guardrails, handoff, deflection metrics, injection defence.
4. [Semantic Search at Scale](case-studies/04-semantic-search.md) - e-commerce search: hybrid retrieval, reranking, ANN index ops, embedding refresh, sub-100ms budgets.
5. [Content Moderation](case-studies/05-content-moderation-pipeline.md) - high-throughput classification with tiered models and human review.
6. [Document Intelligence](case-studies/06-document-intelligence-pipeline.md) - extraction from invoices/contracts with schema validation and HITL.
7. [Text-to-SQL Agent](case-studies/07-text-to-sql-agent.md) - NL analytics over a warehouse with correctness verification.
8. [Meeting Assistant](case-studies/08-meeting-assistant.md) - transcription, summarisation, action items, and search over meetings.

## Further reading

- [Building Effective Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents) - the canonical "start simple, add agency only when needed" argument.
- [Patterns for Building LLM-based Systems & Products - Eugene Yan](https://eugeneyan.com/writing/llm-patterns/) - evals, RAG, guardrails, caching as reusable patterns.
- [What We Learned from a Year of Building with LLMs - O'Reilly](https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/) - practitioner field notes across the whole stack.
- [LLM Powered Autonomous Agents - Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/) - the reference taxonomy for agent components.
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) - why context assembly and ordering matter.
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - the classic on why the model is the small box in the diagram.
- [Designing Data-Intensive Applications - Kleppmann](https://dataintensive.net/) - the classic-system-design half of the interview still rests on this.
