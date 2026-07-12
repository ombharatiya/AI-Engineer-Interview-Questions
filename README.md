# AI Engineer Interview Questions

A complete, practical prep resource for AI Engineer, LLM Engineer, and Applied AI interviews, and for every other engineering role that now gets AI questions in the loop.

This is not a list of trivia. Every topic has a crash-course primer, a full question bank with detailed answers, and pointers to where the idea shows up in a real interview. There are runnable coding challenges, worked system design case studies, company-specific guides, and role-specific navigation for engineers coming from backend, frontend, data, DevOps, QA, mobile, and security backgrounds.

**How to use this repo:** pick a starting point below, work through it with `questions.md` open and the answer collapsed until you've tried it yourself, and use [STUDY_PLAN.md](STUDY_PLAN.md) if you want a schedule instead of browsing.

---

## Find your path

**By role.** If you're not applying for a pure "AI Engineer" title, start here. AI questions have shown up in backend, frontend, product, data, DevOps, QA, mobile, and security loops, and the depth expected varies enormously by role.

| Role | Guide |
|---|---|
| Backend Engineer | [15-role-guides/backend-engineer.md](15-role-guides/backend-engineer.md) |
| Frontend Engineer | [15-role-guides/frontend-engineer.md](15-role-guides/frontend-engineer.md) |
| Product / Full-stack Engineer | [15-role-guides/product-engineer.md](15-role-guides/product-engineer.md) |
| Forward Deployed Engineer | [15-role-guides/forward-deployed-engineer.md](15-role-guides/forward-deployed-engineer.md) |
| Data Engineer | [15-role-guides/data-engineer.md](15-role-guides/data-engineer.md) |
| DevOps / Platform / MLOps Engineer | [15-role-guides/devops-platform-engineer.md](15-role-guides/devops-platform-engineer.md) |
| QA / SDET Engineer | [15-role-guides/qa-sdet-engineer.md](15-role-guides/qa-sdet-engineer.md) |
| Mobile Engineer | [15-role-guides/mobile-engineer.md](15-role-guides/mobile-engineer.md) |
| Security Engineer | [15-role-guides/security-engineer.md](15-role-guides/security-engineer.md) |
| "Am I an ML Engineer or AI Engineer?" | [15-role-guides/ml-engineer-vs-ai-engineer.md](15-role-guides/ml-engineer-vs-ai-engineer.md) |

**By company.** Loop structure and emphasis differ a lot between a frontier lab, a big tech AI org, and a fast-moving startup. See [14-company-guides](14-company-guides/) for the full list and tiering.

**By topic.** Working through the fundamentals in order, or brushing up on one area before an interview: see the topic table below.

---

## Topics

| # | Topic | Questions | What it covers |
|---|-------|-----------|-----------------|
| 01 | [ML & Deep Learning Foundations](01-ml-and-dl-foundations/) | 32 | Bias-variance, optimization, regularization, metrics, loss functions, the fundamentals a fine-tuning or evals answer is built on |
| 02 | [LLM & Transformer Fundamentals](02-llm-fundamentals/) | 41 | Attention, positional encodings, tokenization, scaling laws, MoE, decoding, KV cache, reasoning models |
| 03 | [Prompt Engineering & Context Engineering](03-prompt-engineering-and-context/) | 24 | Few-shot design, chain-of-thought, structured outputs, prompt caching, context rot and compaction |
| 04 | [RAG & Retrieval](04-rag-and-retrieval/) | 36 | Chunking, embeddings, hybrid search, reranking, agentic RAG, retrieval evaluation |
| 05 | [Fine-tuning, RLHF & Alignment](05-fine-tuning-and-alignment/) | 36 | SFT, LoRA/QLoRA, DPO/PPO/GRPO, distillation, GPU memory math for training |
| 06 | [Agents, Tool Use & MCP](06-agents-and-tool-use/) | 37 | Tool calling, MCP, planning patterns, multi-agent design, agent evaluation and security |
| 07 | [Evals & Observability](07-evaluation-and-observability/) | 31 | LLM-as-judge, benchmark limits, RAG and agent evals, tracing, regression testing |
| 08 | [Inference, Serving & Production LLM Systems](08-inference-and-production/) | 36 | Prefill vs. decode, KV cache paging, quantization, speculative decoding, cost engineering |
| 09 | [Safety, Security & Responsible AI](09-safety-security-and-responsible-ai/) | 26 | Prompt injection, OWASP LLM Top 10, guardrails, agent security, data governance |
| 10 | [Multimodal Models](10-multimodal/) | 21 | Vision-language architecture, diffusion, ASR/TTS, voice agents, multimodal RAG |
| 11 | [AI System Design](11-ai-system-design/) | 8 case studies | A reusable answer framework plus eight worked case studies |
| 12 | [Coding Challenges](12-coding-challenges/) | 13 challenges | Implement attention, BPE, sampling, KV cache, an agent loop, and more, from scratch |
| 13 | [Interview Process & Behavioral](13-interview-process-and-behavioral/) | 22 | Loop anatomy by company type, take-homes, portfolio projects, AI-specific behavioral questions |

Plus: [resources/](resources/) for curated papers, blogs, courses, and books, and [CHEATSHEET.md](CHEATSHEET.md) for the night before your interview.

---

## System design case studies

Full worked examples in [11-ai-system-design/case-studies](11-ai-system-design/case-studies/), each following the same template: requirements, architecture, evaluation plan, cost estimate, failure modes, and likely follow-ups.

1. [Enterprise RAG Assistant](11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)
2. [AI Code Assistant](11-ai-system-design/case-studies/02-ai-code-assistant.md)
3. [Customer Support Agent](11-ai-system-design/case-studies/03-customer-support-agent.md)
4. [Semantic Search at Scale](11-ai-system-design/case-studies/04-semantic-search.md)
5. [Content Moderation Pipeline](11-ai-system-design/case-studies/05-content-moderation-pipeline.md)
6. [Document Intelligence Pipeline](11-ai-system-design/case-studies/06-document-intelligence-pipeline.md)
7. [Text-to-SQL Agent](11-ai-system-design/case-studies/07-text-to-sql-agent.md)
8. [Meeting Assistant](11-ai-system-design/case-studies/08-meeting-assistant.md)

## Coding challenges

Thirteen self-contained Python files in [12-coding-challenges](12-coding-challenges/), numpy and the standard library only, each with a reference solution and a real test suite. Implement it yourself before reading the solution.

`attention` · `BPE tokenizer` · `sampling strategies` · `positional encodings` · `layernorm & softmax` · `KV cache` · `mini-GPT forward pass` · `semantic search / RAG` · `text chunking` · `agent loop` · `rate limiter & retry` · `eval metrics` · `streaming parser`

## Company guides

Public-information interview guides in [14-company-guides](14-company-guides/): loop structure, what each company emphasizes, and representative questions built from their known focus areas, not leaked material. See each guide's "Last reviewed" note and sources.

**Frontier labs:** [Anthropic](14-company-guides/anthropic.md) · [OpenAI](14-company-guides/openai.md) · [Google DeepMind](14-company-guides/google-deepmind.md) · [Meta](14-company-guides/meta-ai.md) · [xAI](14-company-guides/xai.md) · [Mistral AI](14-company-guides/mistral.md)

**Big tech:** [Microsoft](14-company-guides/microsoft.md) · [Amazon](14-company-guides/amazon.md) · [Apple](14-company-guides/apple.md) · [NVIDIA](14-company-guides/nvidia.md)

**AI-native & infra:** [Databricks](14-company-guides/databricks.md) · [Scale AI](14-company-guides/scale-ai.md) · [Perplexity](14-company-guides/perplexity.md) · [Cursor (Anysphere)](14-company-guides/cursor-anysphere.md) · [Cohere](14-company-guides/cohere.md) · [Hugging Face](14-company-guides/hugging-face.md) · [Together AI](14-company-guides/together-ai.md) · [Glean](14-company-guides/glean.md)

**Applied / forward-deployed:** [Palantir](14-company-guides/palantir.md) · [Sierra](14-company-guides/sierra.md)

---

## Contributing

Corrections, new questions, and new case studies are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the format.

## License

[MIT](LICENSE).
