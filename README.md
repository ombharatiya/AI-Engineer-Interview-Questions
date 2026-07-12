# AI Engineer Interview Questions

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Topics](https://img.shields.io/badge/topics-13-informational.svg)](#topics)
[![Questions](https://img.shields.io/badge/questions-321-orange.svg)](#topics)

A complete, practical prep resource for AI Engineer, LLM Engineer, and Applied AI interviews, and for every other engineering role that now gets AI questions in the loop. Each topic has a crash-course primer, a full question bank with worked answers, runnable coding challenges, worked system design case studies, and company guides built from public information, not leaked material.

Work through a topic with `questions.md` open and the answer collapsed until you've tried it yourself, or follow [STUDY_PLAN.md](STUDY_PLAN.md) if you want a schedule instead of browsing.

**13 topics** · **321 questions** · **8 system design case studies** · **13 coding challenges** · **20 company guides** · **10 role guides**

---

## Company guides

Loop structure and emphasis differ a lot between a frontier lab, a big tech AI org, and a fast-moving startup. Guides are built from public information (job postings, engineering blogs, published interview reports), not leaked material, and each one has a "last reviewed" note and sources.

| Company | Tier | Guide |
|---|---|---|
| Anthropic | Frontier lab | [Guide](14-company-guides/anthropic.md) |
| OpenAI | Frontier lab | [Guide](14-company-guides/openai.md) |
| Google DeepMind | Frontier lab | [Guide](14-company-guides/google-deepmind.md) |
| Meta | Frontier lab | [Guide](14-company-guides/meta-ai.md) |
| xAI | Frontier lab | [Guide](14-company-guides/xai.md) |
| Mistral AI | Frontier lab | [Guide](14-company-guides/mistral.md) |
| Microsoft | Big tech | [Guide](14-company-guides/microsoft.md) |
| Amazon | Big tech | [Guide](14-company-guides/amazon.md) |
| Apple | Big tech | [Guide](14-company-guides/apple.md) |
| NVIDIA | Big tech | [Guide](14-company-guides/nvidia.md) |
| Databricks | AI-native & infra | [Guide](14-company-guides/databricks.md) |
| Scale AI | AI-native & infra | [Guide](14-company-guides/scale-ai.md) |
| Perplexity | AI-native & infra | [Guide](14-company-guides/perplexity.md) |
| Cursor (Anysphere) | AI-native & infra | [Guide](14-company-guides/cursor-anysphere.md) |
| Cohere | AI-native & infra | [Guide](14-company-guides/cohere.md) |
| Hugging Face | AI-native & infra | [Guide](14-company-guides/hugging-face.md) |
| Together AI | AI-native & infra | [Guide](14-company-guides/together-ai.md) |
| Glean | AI-native & infra | [Guide](14-company-guides/glean.md) |
| Palantir | Applied / forward-deployed | [Guide](14-company-guides/palantir.md) |
| Sierra | Applied / forward-deployed | [Guide](14-company-guides/sierra.md) |

---

## Start here: The AI Engineer 75

Not sure where to spend limited prep time? [AI-ENGINEER-75.md](AI-ENGINEER-75.md) is a Blind-75-style checklist: the 75 highest-signal questions, case studies, and coding challenges pulled from across the whole repo. If you only do one thing before an interview, do this - it's the fastest way to find out whether you're actually ready.

---

## Find your path

**By role.** Not applying for a pure "AI Engineer" title? Start here. AI questions now show up in backend, frontend, product, data, DevOps, QA, mobile, and security loops, and the depth expected varies a lot by role.

| Role | Guide |
|---|---|
| Backend Engineer | [Guide](15-role-guides/backend-engineer.md) |
| Frontend Engineer | [Guide](15-role-guides/frontend-engineer.md) |
| Product / Full-stack Engineer | [Guide](15-role-guides/product-engineer.md) |
| Forward Deployed Engineer | [Guide](15-role-guides/forward-deployed-engineer.md) |
| Data Engineer | [Guide](15-role-guides/data-engineer.md) |
| DevOps / Platform / MLOps Engineer | [Guide](15-role-guides/devops-platform-engineer.md) |
| QA / SDET Engineer | [Guide](15-role-guides/qa-sdet-engineer.md) |
| Mobile Engineer | [Guide](15-role-guides/mobile-engineer.md) |
| Security Engineer | [Guide](15-role-guides/security-engineer.md) |
| "Am I an ML Engineer or AI Engineer?" | [Guide](15-role-guides/ml-engineer-vs-ai-engineer.md) |

**By company.** See the [company guides table](#company-guides) above.

**By topic.** See the topics table below.

---

## Topics

| # | Topic | Questions | What it covers |
|---|-------|-----------|-----------------|
| 01 | [ML & Deep Learning Foundations](01-ml-and-dl-foundations/) | 32 | Bias-variance, optimization, regularization, metrics, loss functions, the fundamentals a fine-tuning or evals answer is built on |
| 02 | [LLM & Transformer Fundamentals](02-llm-fundamentals/) | 41 | Attention, positional encodings, tokenization, scaling laws, MoE, decoding, KV cache, reasoning models |
| 03 | [Prompt Engineering & Context Engineering](03-prompt-engineering-and-context/) | 24 | Few-shot design, chain-of-thought, structured outputs, prompt caching, context rot and compaction |
| 04 | [RAG & Retrieval](04-rag-and-retrieval/) | 36 | Chunking, embeddings, hybrid search, reranking, agentic RAG, retrieval evaluation |
| 05 | [Fine-tuning, RLHF & Alignment](05-fine-tuning-and-alignment/) | 36 | SFT, LoRA/QLoRA, DPO/PPO/GRPO, distillation, GPU memory maths for training |
| 06 | [Agents, Tool Use & MCP](06-agents-and-tool-use/) | 37 | Tool calling, MCP, planning patterns, multi-agent design, agent evaluation and security |
| 07 | [Evals & Observability](07-evaluation-and-observability/) | 31 | LLM-as-judge, benchmark limits, RAG and agent evals, tracing, regression testing |
| 08 | [Inference, Serving & Production LLM Systems](08-inference-and-production/) | 36 | Prefill vs. decode, KV cache paging, quantization, speculative decoding, cost engineering |
| 09 | [Safety, Security & Responsible AI](09-safety-security-and-responsible-ai/) | 26 | Prompt injection, OWASP LLM Top 10, guardrails, agent security, data governance |
| 10 | [Multimodal Models](10-multimodal/) | 21 | Vision-language architecture, diffusion, ASR/TTS, voice agents, multimodal RAG |
| 11 | [AI System Design](11-ai-system-design/) | 8 case studies | A reusable answer framework plus eight worked case studies |
| 12 | [Coding Challenges](12-coding-challenges/) | 13 challenges | Implement attention, BPE, sampling, KV cache, an agent loop, and more, from scratch |
| 13 | [Interview Process & Behavioral](13-interview-process-and-behavioral/) | 22 | Loop anatomy by company type, take-homes, portfolio projects, AI-specific behavioural questions |

Plus: [resources/](resources/) for curated papers, blogs, courses, and books; [STUDY_PLAN.md](STUDY_PLAN.md) for a day-by-day schedule; [CHEATSHEET.md](CHEATSHEET.md) for the night before your interview.

---

## System design case studies

Full worked examples in [11-ai-system-design/case-studies](11-ai-system-design/case-studies/), each following the same template: requirements, architecture, evaluation plan, cost estimate, failure modes, and likely follow-ups.

| # | Case study |
|---|---|
| 1 | [Enterprise RAG Assistant](11-ai-system-design/case-studies/01-enterprise-rag-assistant.md) |
| 2 | [AI Code Assistant](11-ai-system-design/case-studies/02-ai-code-assistant.md) |
| 3 | [Customer Support Agent](11-ai-system-design/case-studies/03-customer-support-agent.md) |
| 4 | [Semantic Search at Scale](11-ai-system-design/case-studies/04-semantic-search.md) |
| 5 | [Content Moderation Pipeline](11-ai-system-design/case-studies/05-content-moderation-pipeline.md) |
| 6 | [Document Intelligence Pipeline](11-ai-system-design/case-studies/06-document-intelligence-pipeline.md) |
| 7 | [Text-to-SQL Agent](11-ai-system-design/case-studies/07-text-to-sql-agent.md) |
| 8 | [Meeting Assistant](11-ai-system-design/case-studies/08-meeting-assistant.md) |

---

## Coding challenges

Thirteen self-contained Python files in [12-coding-challenges](12-coding-challenges/), numpy and the standard library only, each with a reference solution and a real test suite. Read only the problem statement, implement it yourself, then run the file directly, for example `python3 12-coding-challenges/01_attention.py`.

| # | Challenge | Difficulty | Concepts |
|---|-----------|------------|----------|
| 01 | [Attention](12-coding-challenges/01_attention.py) | Medium | Scaled dot-product attention, multi-head, causal masking |
| 02 | [BPE Tokenizer](12-coding-challenges/02_bpe_tokenizer.py) | Medium | Byte-level BPE: train, encode, decode |
| 03 | [Sampling Strategies](12-coding-challenges/03_sampling.py) | Easy | Temperature, top-k, top-p, min-p, repetition penalty |
| 04 | [Positional Encodings](12-coding-challenges/04_positional_encodings.py) | Medium | Sinusoidal PE, RoPE |
| 05 | [LayerNorm & Softmax](12-coding-challenges/05_layernorm_and_softmax.py) | Easy | Stable softmax/log-softmax, LayerNorm, RMSNorm |
| 06 | [KV Cache](12-coding-challenges/06_kv_cache.py) | Medium | Autoregressive decode loop with vs. without KV cache |
| 07 | [Mini-GPT Forward Pass](12-coding-challenges/07_mini_gpt_forward.py) | Hard | Full GPT block forward pass: embeddings, attention, MLP, logits |
| 08 | [Semantic Search / RAG](12-coding-challenges/08_semantic_search_rag.py) | Medium | Embed, index, cosine retrieval, context assembly |
| 09 | [Text Chunking](12-coding-challenges/09_text_chunking.py) | Easy | Fixed, sliding-window, recursive, sentence chunkers |
| 10 | [Agent Loop](12-coding-challenges/10_agent_loop.py) | Medium | Tool-calling agent loop with a mock LLM |
| 11 | [Rate Limiter & Retry](12-coding-challenges/11_rate_limiter_and_retry.py) | Medium | Token bucket, exponential backoff with jitter |
| 12 | [Eval Metrics](12-coding-challenges/12_eval_metrics.py) | Medium | pass@k unbiased estimator, QA F1/EM, judge harness skeleton |
| 13 | [Streaming Parser](12-coding-challenges/13_streaming_parser.py) | Hard | SSE parser, incremental tool-call argument assembly |

---

## Contributing

Corrections, new questions, and new case studies are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the format.

## License

[MIT](LICENSE).
