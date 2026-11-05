# 📚 Curated Resources

Everything here is chosen for one purpose: getting you through AI Engineer / GenAI / LLM Engineer interviews. Each entry has a one-line annotation on why it matters for interview prep specifically. Where a link is omitted, the resource is easy to find by name - we only link URLs we're certain of.

---

## 1. Foundational papers

You don't need to have read every paper cover to cover, but interviewers expect you to know what each of these contributed and why it mattered. Read the abstract, the key figure, and the ablations.

| Paper | Link | Why it matters for interviews |
|---|---|---|
| Attention Is All You Need (Vaswani et al., 2017) | [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762) | The transformer paper - you *will* be asked to explain self-attention, and this is the source of truth. |
| Language Models are Few-Shot Learners (GPT-3, Brown et al., 2020) | [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165) | Origin of in-context learning and few-shot prompting - the "why does prompting work at all" question traces here. |
| Training language models to follow instructions with human feedback (InstructGPT, Ouyang et al., 2022) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) | The SFT → reward model → RLHF pipeline every alignment question is built on. |
| Training Compute-Optimal Large Language Models (Chinchilla, Hoffmann et al., 2022) | [arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556) | The ~20 tokens/parameter scaling result - the canonical answer to "how do you trade off model size vs. data?" |
| LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021) | [arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685) | The default parameter-efficient fine-tuning method; know the low-rank decomposition and where the adapters go. |
| QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023) | [arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314) | 4-bit NF4 quantization + LoRA - the standard answer to "fine-tune a 70B model on one GPU." |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020) | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) | The paper that named RAG; useful for contrasting the original trained-end-to-end formulation with today's in-context RAG. |
| Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., 2022) | [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903) | Formalised few-shot CoT prompting and the root of test-time compute discussions (the zero-shot "let's think step by step" trick is Kojima et al., 2022 - [arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916)). |
| ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022) | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) | The thought → action → observation loop underneath essentially every agent framework you'll be asked to design. |
| Direct Preference Optimization (Rafailov et al., 2023) | [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290) | "DPO vs. RLHF/PPO" is a near-guaranteed alignment question; know why dropping the explicit reward model works. |
| Constitutional AI: Harmlessness from AI Feedback (Bai et al., 2022) | [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073) | RLAIF and self-critique from principles - the standard contrast case to human-feedback-only alignment. |
| FlashAttention (Dao et al., 2022) | [arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135) | IO-aware exact attention; the go-to example for "attention is memory-bound, not compute-bound" in inference questions. |
| LLaMA (Touvron et al., 2023) | [arxiv.org/abs/2302.13971](https://arxiv.org/abs/2302.13971) | Started the open-weights era; shows what "train past Chinchilla-optimal for cheap inference" means in practice. |
| Llama 2 (Touvron et al., 2023) | [arxiv.org/abs/2307.09288](https://arxiv.org/abs/2307.09288) | Unusually detailed RLHF and safety-tuning writeup - great source for concrete alignment-pipeline answers. |
| The Llama 3 Herd of Models (2024) | [arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783) | One of the most complete public recipes for training a frontier-scale model: data mix, infra, post-training, multimodal. |
| GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints (Ainslie et al., 2023) | [arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245) | Grouped-query attention, now the default KV-cache saving in open models; the baseline every "MHA vs. MQA vs. GQA vs. MLA" answer starts from. |
| Mixtral of Experts (Jiang et al., 2024) | [arxiv.org/abs/2401.04088](https://arxiv.org/abs/2401.04088) | The reference open MoE - know active vs. total parameters and why MoE changes serving economics. |
| DeepSeekMath (Shao et al., 2024) | [arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300) | Introduced GRPO; read the method section to explain group-relative advantages without a value network. |
| DeepSeek-V3 Technical Report (2024) | [arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437) | Multi-head latent attention, fine-grained MoE, multi-token prediction and FP8 training in one open report; a frequent source of architecture and serving follow-ups. |
| DeepSeek-R1 (2025) | [arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948) | Reasoning via large-scale RL (GRPO) with verifiable rewards; the paper behind most "how are reasoning models trained?" questions. |
| DAPO: An Open-Source LLM Reinforcement Learning System at Scale (2025) | [arxiv.org/abs/2503.14476](https://arxiv.org/abs/2503.14476) | The best-known fixes to vanilla GRPO (decoupled clipping, dynamic sampling, no KL term); useful when an interviewer pushes past "we used GRPO". |
| Let's Verify Step by Step (Lightman et al., 2023) | [arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050) | Process reward models vs. outcome reward models - key vocabulary for reasoning-model and eval discussions. |
| Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al., 2024) | [arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314) | The test-time compute scaling result; grounds "when should you spend inference tokens instead of training a bigger model?" |
| Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023) | [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172) | The U-shaped position result behind "where do you put the evidence in a long prompt?" and the case for reranking before stuffing. |
| Fast Inference from Transformers via Speculative Decoding (Leviathan et al., 2022) | [arxiv.org/abs/2211.17192](https://arxiv.org/abs/2211.17192) | The draft-then-verify scheme and the rejection-sampling argument for why the output distribution is unchanged. |
| Efficient Memory Management for Large Language Model Serving with PagedAttention (Kwon et al., 2023) | [arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180) | The vLLM paper; block-based KV management is the foundation for continuous batching and prefix caching questions. |
| DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving (Zhong et al., 2024) | [arxiv.org/abs/2401.09670](https://arxiv.org/abs/2401.09670) | The clearest statement of why prefill and decode belong on separate pools, and where the goodput framing comes from. |
| Defeating Prompt Injections by Design (CaMeL, Debenedetti et al., 2025) | [arxiv.org/abs/2503.18813](https://arxiv.org/abs/2503.18813) | Prompt-injection defence by architecture rather than detection: separate control and data flow, enforce policy in an interpreter. |

---

## 2. Must-read engineering blogs & posts

These are where "how it actually works in production" knowledge lives - the material interviewers draw practical questions from.

- **Jay Alammar - The Illustrated Transformer** - [jalammar.github.io/illustrated-transformer](https://jalammar.github.io/illustrated-transformer/) - still the fastest way to rebuild your mental model of attention the night before an interview.
- **Lilian Weng - Lil'Log** - [lilianweng.github.io](https://lilianweng.github.io/) - her [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) and [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) posts are effectively the syllabus for agent and prompting questions.
- **Chip Huyen** - [huyenchip.com](https://huyenchip.com/) - production ML/LLM systems thinking; her posts map almost one-to-one onto AI system design interview rounds.
- **Eugene Yan** - [eugeneyan.com](https://eugeneyan.com/) - [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) is a masterclass in the eval/RAG/guardrail patterns interviewers expect you to know.
- **Hamel Husain** - [hamel.dev](https://hamel.dev/) - his evals writing ([Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) and follow-ups) is the source for the error-analysis-first eval answers that distinguish strong candidates.
- **Simon Willison** - [simonwillison.net](https://simonwillison.net/) - coined the term prompt injection (see his [prompt injection tag](https://simonwillison.net/tags/prompt-injection/)) and named [the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/); the reference for LLM security questions and pragmatic tooling takes.
- **Anthropic engineering** - [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) argues workflows-before-agents (a favourite interviewer stance); [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) is a concrete, numbers-backed RAG improvement; [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) cover context budgets, compaction and progressive disclosure.
- **OpenAI Cookbook** - [developers.openai.com/cookbook](https://developers.openai.com/cookbook) - working code for RAG, evals, function calling, and fine-tuning; good for grounding answers in real API mechanics.

---

## 3. Courses & hands-on

Interviewers can tell within minutes whether you've built things or only read about them. These close that gap.

- **Andrej Karpathy - Neural Networks: Zero to Hero** - [karpathy.ai/zero-to-hero.html](https://karpathy.ai/zero-to-hero.html) - build backprop, a language model, and GPT from scratch; the single best preparation for "explain it from first principles" questions.
- **nanoGPT** - [github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) - a readable GPT training loop; if you can walk through this repo, you can survive any transformer-internals grilling.
- **minbpe** - [github.com/karpathy/minbpe](https://github.com/karpathy/minbpe) - BPE tokenization from scratch; tokenizer questions ("why do models claim 9.11 > 9.9?") stop being scary after this.
- **fast.ai - Practical Deep Learning** - [course.fast.ai](https://course.fast.ai/) - the fastest route to solid DL intuition if your foundations are shaky; top-down and code-first.
- **Hugging Face courses** - [huggingface.co/learn](https://huggingface.co/learn) - the LLM/NLP course covers the transformers ecosystem you'll be assumed to know; the [Agents course](https://huggingface.co/learn/agents-course) is a practical tour of tool use and agent patterns.
- **DeepLearning.AI short courses** - [deeplearning.ai/courses](https://www.deeplearning.ai/courses) - 1-2 hour courses on RAG, evals, agents, and fine-tuning, often taught with the relevant vendor; efficient for patching specific gaps.
- **Eval-focused cohort courses** - Hamel Husain and Shreya Shankar teach a well-known "AI Evals for Engineers" cohort course on Maven; worth knowing the curriculum exists since evals are among the most heavily tested topics in 2026 loops (find it by name on maven.com).

---

## 4. Books

- **AI Engineering - Chip Huyen (O'Reilly, 2025)** - the closest thing to an official textbook for this interview loop: evals, RAG, fine-tuning decisions, inference optimization, all framed as engineering tradeoffs.
- **Designing Machine Learning Systems - Chip Huyen (O'Reilly, 2022)** - pre-LLM ML systems thinking (data, deployment, monitoring, feedback loops) that still underpins half of system design interviews.
- **Build a Large Language Model (From Scratch) - Sebastian Raschka (Manning, 2024)** - implement GPT end-to-end in PyTorch; companion code at [github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch). Ideal for coding-round prep.
- **Hands-On Large Language Models - Jay Alammar & Maarten Grootendorst (O'Reilly, 2024)** - visual, practical coverage of embeddings, transformers, and applications; the quickest read on this list.
- **Deep Learning - Goodfellow, Bengio & Courville (MIT Press, 2016)** - [deeplearningbook.org](https://www.deeplearningbook.org/) (free online) - reference-grade foundations; use selectively for optimization/regularization chapters, don't read cover to cover.

---

## 5. Staying current

Interviews as of 2026 routinely reference things released in the last six months. You need a low-effort pipeline for staying current.

**Newsletters & feeds**
- **Latent Space** - [latent.space](https://www.latent.space/) - popularised the "AI Engineer" label; best signal on what skills the market (and interviewers) currently care about.
- **Interconnects - Nathan Lambert** - [interconnects.ai](https://www.interconnects.ai/) - the best public writing on post-training, RLHF/DPO/GRPO, and reasoning models; directly feeds alignment-question answers.
- **Simon Willison's weblog** - [simonwillison.net](https://simonwillison.net/) - near-daily, pragmatic coverage of new models and tools; his model release notes are perfect interview-day briefings.
- **Ahead of AI - Sebastian Raschka** - [magazine.sebastianraschka.com](https://magazine.sebastianraschka.com/) - research digests with enough technical depth to actually explain the papers, not just list them.

**Podcasts**
- **Latent Space podcast** - practitioner interviews about building with LLMs; good for absorbing the vocabulary of production AI engineering.
- **Dwarkesh Podcast** - [dwarkesh.com](https://www.dwarkesh.com/) - long-form interviews with researchers (Sutskever, Amodei, Karpathy, et al.); best for research-depth context at frontier-lab interviews.

**Communities**
- **r/LocalLLaMA** - [reddit.com/r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) - the pulse of the open-weights world: quantization, local serving, and new model release chatter.
- **Hugging Face and EleutherAI Discords** - where practitioners debug training and inference in the open; lurking teaches you real failure modes.

---

## 6. Practice & benchmarking

- **Arena (formerly LMArena, originally Chatbot Arena)** - [arena.ai](https://arena.ai/) - crowdsourced pairwise model battles (Elo-style); know how it works because "how would you compare two models?" is a standard eval question.
- **Hugging Face leaderboard ecosystem** - [huggingface.co](https://huggingface.co/) - hosts most public leaderboards as Spaces (the original Open LLM Leaderboard is now retired - knowing *why* benchmark saturation and contamination killed it is itself good interview material).
- **SWE-bench** - [swebench.com](https://www.swebench.com/) - agentic coding on real GitHub issues; the reference point for any coding-agent design discussion. The Verified subset is close to saturated at the frontier, so check which variant a quoted score refers to and how much of it is the harness.
- **MTEB leaderboard** - [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) - where embedding models are compared; check it before answering "which embedding model would you pick?"

> **Caution - leaderboard-driven thinking is a red flag.** Saying "I'd pick whatever tops the leaderboard" signals junior judgment. Public benchmarks suffer contamination, saturation, and distribution mismatch with your task. The strong-candidate answer is always: leaderboards for a shortlist, *your own task-specific evals* for the decision.

---

## 7. Docs worth reading end-to-end

Vendor docs are underrated interview prep - they encode each lab's official position on prompting, tool use, and agents.

- **OpenAI docs** - [developers.openai.com/api/docs](https://developers.openai.com/api/docs) - read the prompting, function calling / tool use, and agents guides; also structured outputs, which comes up constantly in production-integration questions.
- **Anthropic (Claude) docs** - [platform.claude.com/docs](https://platform.claude.com/docs) - the prompt engineering section is the most thorough of any vendor (system prompts, XML structuring, chaining); read the tool use and agent guides too.
- **Google AI (Gemini) docs** - [ai.google.dev](https://ai.google.dev/) - read the long-context and prompting strategy sections; Gemini's 1M+ token context makes it the standard example in "long context vs. RAG" debates.
- **vLLM docs** - [docs.vllm.ai](https://docs.vllm.ai/) - read the pages on PagedAttention, continuous batching, prefix caching, and quantization support; this is exactly the material inference/serving interview rounds are built from.
- **SGLang docs** - [docs.sglang.io](https://docs.sglang.io/) - the main alternative serving engine; skim RadixAttention and structured-output support so you can compare it with vLLM.

---

## 8. Agent protocols and standards

These are the specs behind most 2026 agent-design questions. Read the overview and the security sections, then skim the rest.

- **Model Context Protocol (MCP) specification** - [modelcontextprotocol.io/specification/latest](https://modelcontextprotocol.io/specification/latest) - the current revision is dated 2026-07-28, and its changelog (stateless requests with no `initialize` handshake, server-to-client input via multi round-trip requests) is worth reading if you learned MCP on an older version. Know the server primitives (tools, resources, prompts), the client features (elicitation, now delivered as a multi round-trip request; sampling and roots are deprecated in 2026-07-28 and should not be adopted in new implementations), the stdio and Streamable HTTP transports, and the authorisation model; MCP is the assumed answer to "how do you standardise tool integration for agents?" Official extensions (MCP Apps, Tasks, Skills, Server Cards, the auth extensions) now carry a maturity stage of Experimental, Beta or Stable, so check the stage before you rely on one. The [project blog](https://blog.modelcontextprotocol.io/) carries the roadmap and is where a new revision would be announced.
- **Agent2Agent (A2A) protocol specification** - [a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/) - Agent Cards, tasks and their lifecycle, streaming and push notifications; the reference for "how does one agent call another across a company boundary?" Hosted by the Agentic AI Foundation alongside MCP since August 2026. The official `a2a` command-line client is a quick way to fetch an Agent Card and follow a task through its states.
- **Agent Skills** - [agentskills.io](https://agentskills.io/) - the open format for `SKILL.md` folders and progressive disclosure, governed by the Agentic AI Foundation since October 2026; read the specification page and the guidance on writing descriptions.
- **AGENTS.md** - [agents.md](https://agents.md/) - the convention for repository-level instructions to coding agents, and the contrast case to on-demand skills.
- **OWASP Top 10 for LLM Applications (2026 edition)** - [genai.owasp.org/resource/owasp-genai-llm-top-10-2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (source at [github.com/GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10)) - the shared vocabulary for AI security reviews; know each category well enough to name a mitigation. The IDs changed from the 2025 list (excessive agency is now LLM03, improper output handling LLM10), and the older llm-top-10 landing page still shows 2025, so say which edition you mean.
- **OpenTelemetry GenAI semantic conventions** - [github.com/open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai) - the standard attribute names for LLM, agent, tool and A2A spans, useful when an observability question asks how traces stay portable across vendors. The conventions have moved to this repo (the old opentelemetry.io page is no longer maintained) and are still at Development status, so operation and span names can change between versions.

---

*Back to the [main guide](../README.md).*
