# The AI Engineer 75

A Blind-75-style checklist, inspired by the well-known Blind 75 list for coding interviews, but for AI engineering interviews. These are the 75 highest-signal items pulled from across the whole repo: the questions, system design case studies, and coding challenges most likely to actually come up, and most likely to sink you if you can't answer them cold.

This is not a replacement for the full repo. It is the floor, not the ceiling: if you can work through every item below without opening the answer first, you are in reasonable shape for a loop. If you have more time, go back and do the full question banks in each topic.

**How to use this list:** work top to bottom. For each question, answer out loud before opening the linked answer. For each case study, spend 30-45 minutes designing it yourself on a doc before reading the worked solution. For each coding challenge, implement it from scratch before looking at the reference solution. Check items off as you go.

🟢 Foundational · 🟡 Core · 🔴 Advanced

---

## 🧠 ML & Deep Learning Foundations

- [ ] 🟢 [Explain the bias-variance tradeoff. How do you tell which one is hurting your model?](01-ml-and-dl-foundations/questions.md#1-explain-the-bias-variance-tradeoff-how-do-you-tell-which-one-is-hurting-your-model)
- [ ] 🟢 [Explain precision, recall, and F1. Give a concrete case where 99% accuracy means the model is useless.](01-ml-and-dl-foundations/questions.md#6-explain-precision-recall-and-f1-give-a-concrete-case-where-99-accuracy-means-the-model-is-useless)
- [ ] 🟡 [Explain backpropagation to me like I'm a strong software engineer who's never done ML. Why is it efficient?](01-ml-and-dl-foundations/questions.md#22-explain-backpropagation-to-me-like-im-a-strong-software-engineer-whos-never-done-ml-why-is-it-efficient)
- [ ] 🟡 [Derive cross-entropy loss from first principles. Why is it "the right" loss for classification and language modeling?](01-ml-and-dl-foundations/questions.md#26-derive-cross-entropy-loss-from-first-principles-why-is-it-the-right-loss-for-classification-and-language-modeling)

## 🧠 LLM & Transformer Fundamentals

- [ ] 🟢 [Walk me through what happens inside a single transformer decoder block.](02-llm-fundamentals/questions.md#2-walk-me-through-what-happens-inside-a-single-transformer-decoder-block)
- [ ] 🟢 [Explain self-attention step by step. What exactly are Q, K, and V?](02-llm-fundamentals/questions.md#3-explain-self-attention-step-by-step-what-exactly-are-q-k-and-v)
- [ ] 🟢 [Why do LLMs use subword tokenization instead of whole words or raw characters?](02-llm-fundamentals/questions.md#9-why-do-llms-use-subword-tokenization-instead-of-whole-words-or-raw-characters)
- [ ] 🟡 [Compare greedy decoding, top-k sampling, and top-p (nucleus) sampling.](02-llm-fundamentals/questions.md#12-compare-greedy-decoding-top-k-sampling-and-top-p-nucleus-sampling)
- [ ] 🟡 [What is the KV cache and why does it make generation fast?](02-llm-fundamentals/questions.md#13-what-is-the-kv-cache-and-why-does-it-make-generation-fast)
- [ ] 🟡 [Explain RoPE. What's the rotation intuition and why did it become the default?](02-llm-fundamentals/questions.md#26-explain-rope-whats-the-rotation-intuition-and-why-did-it-become-the-default)
- [ ] 🟢 [Describe the modern LLM training pipeline: pretraining → mid-training → SFT → RL.](02-llm-fundamentals/questions.md#33-describe-the-modern-llm-training-pipeline-pretraining-mid-training-sft-rl)
- [ ] 🟡 [Compare Kaplan and Chinchilla scaling laws. What did Chinchilla change?](02-llm-fundamentals/questions.md#43-compare-kaplan-and-chinchilla-scaling-laws-what-did-chinchilla-change)
- [ ] 🔴 [Explain Mixture-of-Experts: the router, top-k experts, total vs active parameters. Why does it win?](02-llm-fundamentals/questions.md#46-explain-mixture-of-experts-the-router-top-k-experts-total-vs-active-parameters-why-does-it-win)

## 🧭 Prompt & Context Engineering

- [ ] 🟢 [Explain the system, user, and assistant roles. What belongs in each?](03-prompt-engineering-and-context/questions.md#2-explain-the-system-user-and-assistant-roles-what-belongs-in-each)
- [ ] 🟢 [What is chain-of-thought prompting? When does it help, and when is it unnecessary or harmful?](03-prompt-engineering-and-context/questions.md#3-what-is-chain-of-thought-prompting-when-does-it-help-and-when-is-it-unnecessary-or-harmful)
- [ ] 🟡 [What is "context engineering," and how is it different from prompt engineering?](03-prompt-engineering-and-context/questions.md#6-what-is-context-engineering-and-how-is-it-different-from-prompt-engineering)
- [ ] 🟡 [How do you design good tool/function definitions for an LLM? What makes tool calling fail?](03-prompt-engineering-and-context/questions.md#18-how-do-you-design-good-toolfunction-definitions-for-an-llm-what-makes-tool-calling-fail)
- [ ] 🟡 [How do you structure a prompt to be resistant to prompt injection from retrieved or user-supplied content?](03-prompt-engineering-and-context/questions.md#19-how-do-you-structure-a-prompt-to-be-resistant-to-prompt-injection-from-retrieved-or-user-supplied-content)

## 🔎 RAG & Retrieval

- [ ] 🟢 [What is RAG, and what problem does it actually solve?](04-rag-and-retrieval/questions.md#1-what-is-rag-and-what-problem-does-it-actually-solve)
- [ ] 🟢 [Walk me through every stage of a production RAG pipeline, from raw documents to a cited answer.](04-rag-and-retrieval/questions.md#3-walk-me-through-every-stage-of-a-production-rag-pipeline-from-raw-documents-to-a-cited-answer)
- [ ] 🟡 [What chunking strategies do you know, and how do you pick one?](04-rag-and-retrieval/questions.md#4-what-chunking-strategies-do-you-know-and-how-do-you-pick-one)
- [ ] 🟡 [How does a bi-encoder embedding model work at retrieval time, and what's the key limitation of that architecture?](04-rag-and-retrieval/questions.md#6-how-does-a-bi-encoder-embedding-model-work-at-retrieval-time-and-whats-the-key-limitation-of-that-architecture)
- [ ] 🟡 [What is hybrid search, and why does pure vector search fail on some queries?](04-rag-and-retrieval/questions.md#9-what-is-hybrid-search-and-why-does-pure-vector-search-fail-on-some-queries)
- [ ] 🟡 [What is a reranker, and why add one after vector search?](04-rag-and-retrieval/questions.md#10-what-is-a-reranker-and-why-add-one-after-vector-search)
- [ ] 🟡 [What retrieval metrics would you track - recall@k, MRR, nDCG - and what does each actually tell you?](04-rag-and-retrieval/questions.md#41-what-retrieval-metrics-would-you-track---recallk-mrr-ndcg---and-what-does-each-actually-tell-you)
- [ ] 🟡 [What are the top failure modes of production RAG systems?](04-rag-and-retrieval/questions.md#45-what-are-the-top-failure-modes-of-production-rag-systems)
- [ ] 🔴 ["Long-context models made RAG obsolete." Argue both sides, then give your actual position.](04-rag-and-retrieval/questions.md#48-long-context-models-made-rag-obsolete-argue-both-sides-then-give-your-actual-position)

## 🎛️ Fine-tuning, RLHF & Alignment

- [ ] 🟢 [When would you fine-tune a model instead of using prompting or RAG?](05-fine-tuning-and-alignment/questions.md#1-when-would-you-fine-tune-a-model-instead-of-using-prompting-or-rag)
- [ ] 🟡 [Explain how LoRA works - the math, and what `r` and `alpha` mean.](05-fine-tuning-and-alignment/questions.md#6-explain-how-lora-works---the-math-and-what-r-and-alpha-mean)
- [ ] 🟢 [Walk me through the classic RLHF pipeline end to end.](05-fine-tuning-and-alignment/questions.md#10-walk-me-through-the-classic-rlhf-pipeline-end-to-end)
- [ ] 🟡 [What is reward hacking? Give concrete examples and mitigations.](05-fine-tuning-and-alignment/questions.md#19-what-is-reward-hacking-give-concrete-examples-and-mitigations)
- [ ] 🟡 [Explain DPO. What's the key insight that lets it skip the reward model and the RL loop?](05-fine-tuning-and-alignment/questions.md#20-explain-dpo-whats-the-key-insight-that-lets-it-skip-the-reward-model-and-the-rl-loop)
- [ ] 🔴 [Explain GRPO. Why has it displaced PPO for reasoning RL?](05-fine-tuning-and-alignment/questions.md#35-explain-grpo-why-has-it-displaced-ppo-for-reasoning-rl)

## 🤖 Agents, Tool Use & MCP

- [ ] 🟢 [What's the difference between a workflow and an agent?](06-agents-and-tool-use/questions.md#1-whats-the-difference-between-a-workflow-and-an-agent)
- [ ] 🟢 [Walk me through the core agent loop. What are the components and stop conditions?](06-agents-and-tool-use/questions.md#3-walk-me-through-the-core-agent-loop-what-are-the-components-and-stop-conditions)
- [ ] 🟢 [How does function/tool calling actually work mechanically, end to end?](06-agents-and-tool-use/questions.md#4-how-does-functiontool-calling-actually-work-mechanically-end-to-end)
- [ ] 🟢 [What is MCP and what problem does it solve?](06-agents-and-tool-use/questions.md#7-what-is-mcp-and-what-problem-does-it-solve)
- [ ] 🟡 [What makes a good tool definition? Give concrete design rules.](06-agents-and-tool-use/questions.md#10-what-makes-a-good-tool-definition-give-concrete-design-rules)
- [ ] 🟡 [When does multi-agent beat single-agent, and when does it make things worse?](06-agents-and-tool-use/questions.md#23-when-does-multi-agent-beat-single-agent-and-when-does-it-make-things-worse)
- [ ] 🟡 [How do you evaluate an agent? Compare trajectory evals and final-outcome evals.](06-agents-and-tool-use/questions.md#27-how-do-you-evaluate-an-agent-compare-trajectory-evals-and-final-outcome-evals)
- [ ] 🔴 [How does prompt injection work against agents via tool results, and what actually mitigates it?](06-agents-and-tool-use/questions.md#39-how-does-prompt-injection-work-against-agents-via-tool-results-and-what-actually-mitigates-it)
- [ ] 🔴 [What is the "lethal trifecta," and how do you design agent systems around it?](06-agents-and-tool-use/questions.md#40-what-is-the-lethal-trifecta-and-how-do-you-design-agent-systems-around-it)

## 🧪 Evals & Observability

- [ ] 🟢 [Walk me through the taxonomy of evaluation methods for LLM systems and when you'd use each.](07-evaluation-and-observability/questions.md#2-walk-me-through-the-taxonomy-of-evaluation-methods-for-llm-systems-and-when-youd-use-each)
- [ ] 🟢 [What is LLM-as-judge, and when is it the right tool?](07-evaluation-and-observability/questions.md#5-what-is-llm-as-judge-and-when-is-it-the-right-tool)
- [ ] 🟡 [What are the known biases of LLM judges, and how do you mitigate each?](07-evaluation-and-observability/questions.md#15-what-are-the-known-biases-of-llm-judges-and-how-do-you-mitigate-each)
- [ ] 🟡 [How do you evaluate a RAG pipeline? Why evaluate components separately from the end-to-end system?](07-evaluation-and-observability/questions.md#21-how-do-you-evaluate-a-rag-pipeline-why-evaluate-components-separately-from-the-end-to-end-system)
- [ ] 🟡 [You have 500 production transcripts flagged as failures. Walk me through your error-analysis process.](07-evaluation-and-observability/questions.md#26-you-have-500-production-transcripts-flagged-as-failures-walk-me-through-your-error-analysis-process)
- [ ] 🔴 [Your new prompt scores 78% vs the old prompt's 74% on a 100-example eval. Do you ship it?](07-evaluation-and-observability/questions.md#39-your-new-prompt-scores-78-vs-the-old-prompts-74-on-a-100-example-eval-do-you-ship-it)
- [ ] 🟡 [Design the observability stack for a production LLM application. What does a good trace look like?](07-evaluation-and-observability/questions.md#40-design-the-observability-stack-for-a-production-llm-application-what-does-a-good-trace-look-like)

## ⚡ Inference & Production

- [ ] 🟢 [Walk me through what happens inside the server when an LLM processes a request. Why are prefill and decode bottlenecked differently?](08-inference-and-production/questions.md#1-walk-me-through-what-happens-inside-the-server-when-an-llm-processes-a-request-why-are-prefill-and-decode-bottlenecked-differently)
- [ ] 🟢 [What is the KV cache, why is it needed, and how big does it get? Ballpark it for a 70B-class model at 128K context.](08-inference-and-production/questions.md#2-what-is-the-kv-cache-why-is-it-needed-and-how-big-does-it-get-ballpark-it-for-a-70b-class-model-at-128k-context)
- [ ] 🟢 [Define TTFT, TPOT, and tokens/sec. What drives each one, and what are reasonable targets for a chat product?](08-inference-and-production/questions.md#3-define-ttft-tpot-and-tokenssec-what-drives-each-one-and-what-are-reasonable-targets-for-a-chat-product)
- [ ] 🟡 [What's the difference between static and continuous batching, and why did continuous batching become universal?](08-inference-and-production/questions.md#8-whats-the-difference-between-static-and-continuous-batching-and-why-did-continuous-batching-become-universal)
- [ ] 🟡 [What is prompt (prefix) caching, and why is it one of the biggest cost levers available?](08-inference-and-production/questions.md#9-what-is-prompt-prefix-caching-and-why-is-it-one-of-the-biggest-cost-levers-available)
- [ ] 🟡 [Self-host an open-weights model or call a provider API - walk me through the decision.](08-inference-and-production/questions.md#24-self-host-an-open-weights-model-or-call-a-provider-api---walk-me-through-the-decision)
- [ ] 🟡 [Design the reliability layer for calls to an LLM provider: timeouts, retries, circuit breakers, idempotency.](08-inference-and-production/questions.md#39-design-the-reliability-layer-for-calls-to-an-llm-provider-timeouts-retries-circuit-breakers-idempotency)

## 🛡️ Safety, Security & Responsible AI

- [ ] 🟢 [What is prompt injection, and how is it different from a jailbreak?](09-safety-security-and-responsible-ai/questions.md#1-what-is-prompt-injection-and-how-is-it-different-from-a-jailbreak)
- [ ] 🟢 [Walk me through the OWASP Top 10 for LLM Applications. Which matter most for an agent?](09-safety-security-and-responsible-ai/questions.md#4-walk-me-through-the-owasp-top-10-for-llm-applications-which-matter-most-for-an-agent)
- [ ] 🟡 [What is the lethal trifecta, and how do you use it to secure an agent?](09-safety-security-and-responsible-ai/questions.md#6-what-is-the-lethal-trifecta-and-how-do-you-use-it-to-secure-an-agent)
- [ ] 🟡 [How do you handle PII in an LLM pipeline end to end?](09-safety-security-and-responsible-ai/questions.md#17-how-do-you-handle-pii-in-an-llm-pipeline-end-to-end)
- [ ] 🟡 [What do RLHF, DPO, and Constitutional AI/RLAIF actually do for safety, and why can't a system prompt replace them?](09-safety-security-and-responsible-ai/questions.md#21-what-do-rlhf-dpo-and-constitutional-airlaif-actually-do-for-safety-and-why-cant-a-system-prompt-replace-them)
- [ ] 🔴 [Design a secure architecture for an agent that reads untrusted web/email content AND has access to a user's private data. How do you defeat prompt injection by construction?](09-safety-security-and-responsible-ai/questions.md#32-design-a-secure-architecture-for-an-agent-that-reads-untrusted-webemail-content-and-has-access-to-a-users-private-data-how-do-you-defeat-prompt-injection-by-construction)

## 🖼️ Multimodal Models

- [ ] 🟢 [Walk me through how a modern VLM gets an image into an LLM.](10-multimodal/questions.md#1-walk-me-through-how-a-modern-vlm-gets-an-image-into-an-llm)
- [ ] 🟢 [Give me the intuition for how diffusion models generate images.](10-multimodal/questions.md#5-give-me-the-intuition-for-how-diffusion-models-generate-images)

## 🏗️ System Design

Work through these as timed mock interviews (45-60 minutes each, design first, then compare) before checking the case study.

- [ ] 🟡 [Design an enterprise RAG assistant with per-document access control and citations](11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)
- [ ] 🟡 [Design a customer support agent that can take real actions (refunds, cancellations)](11-ai-system-design/case-studies/03-customer-support-agent.md)
- [ ] 🟡 [Design a content moderation pipeline at 10M+ items/day](11-ai-system-design/case-studies/05-content-moderation-pipeline.md)
- [ ] 🟡 [Design a text-to-SQL agent over a large data warehouse](11-ai-system-design/case-studies/07-text-to-sql-agent.md)

## 🧑‍💻 Coding Challenges

No peeking at the reference solution until you have a working (or failing, but attempted) implementation of your own.

- [ ] 🟡 [Implement scaled dot-product and multi-head attention with a causal mask](12-coding-challenges/01_attention.py) (Medium)
- [ ] 🟡 [Implement byte-level BPE: train, encode, decode](12-coding-challenges/02_bpe_tokenizer.py) (Medium)
- [ ] 🟢 [Implement temperature, top-k, top-p, min-p, and repetition penalty sampling](12-coding-challenges/03_sampling.py) (Easy)
- [ ] 🟡 [Implement an autoregressive decode loop with and without a KV cache](12-coding-challenges/06_kv_cache.py) (Medium)
- [ ] 🟡 [Implement embed, index, retrieve, and context assembly for a mini-RAG pipeline](12-coding-challenges/08_semantic_search_rag.py) (Medium)
- [ ] 🟡 [Implement a tool-calling agent loop against a mock LLM](12-coding-challenges/10_agent_loop.py) (Medium)
- [ ] 🔴 [Implement an SSE parser and incremental tool-call argument assembly](12-coding-challenges/13_streaming_parser.py) (Hard)

---

**Total: 75 items.** Once you have cleared this list, go deeper with the full question banks in each [topic](README.md#topics), the remaining [system design case studies](11-ai-system-design/), and the rest of the [coding challenges](12-coding-challenges/). For a company-specific pass, see the [company interview questions](14-company-interview-questions/).
