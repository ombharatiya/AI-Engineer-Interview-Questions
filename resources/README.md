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
| The Llama 3 Herd of Models (2024) | [arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783) | The most complete public recipe for training a frontier-scale model: data mix, infra, post-training, multimodal. |
| Mixtral of Experts (Jiang et al., 2024) | [arxiv.org/abs/2401.04088](https://arxiv.org/abs/2401.04088) | The reference open MoE - know active vs. total parameters and why MoE changes serving economics. |
| DeepSeek-R1 (2025) | [arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948) | Reasoning via large-scale RL (GRPO) with verifiable rewards; the paper behind most "how are reasoning models trained?" questions. |
| Let's Verify Step by Step (Lightman et al., 2023) | [arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050) | Process reward models vs. outcome reward models - key vocabulary for reasoning-model and eval discussions. |
| Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al., 2024) | [arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314) | The test-time compute scaling result; grounds "when should you spend inference tokens instead of training a bigger model?" |

---

## 2. Must-read engineering blogs & posts

These are where "how it actually works in production" knowledge lives - the material interviewers draw practical questions from.

- **Jay Alammar - The Illustrated Transformer** - [jalammar.github.io/illustrated-transformer](https://jalammar.github.io/illustrated-transformer/) - still the fastest way to rebuild your mental model of attention the night before an interview.
- **Lilian Weng - Lil'Log** - [lilianweng.github.io](https://lilianweng.github.io/) - her [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) and [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) posts are effectively the syllabus for agent and prompting questions.
- **Chip Huyen** - [huyenchip.com](https://huyenchip.com/) - production ML/LLM systems thinking; her posts map almost one-to-one onto AI system design interview rounds.
- **Eugene Yan** - [eugeneyan.com](https://eugeneyan.com/) - "Patterns for Building LLM-based Systems & Products" is a masterclass in the eval/RAG/guardrail patterns interviewers expect you to know.
- **Hamel Husain** - [hamel.dev](https://hamel.dev/) - his evals writing ("Your AI Product Needs Evals" and follow-ups) is the source for the error-analysis-first eval answers that distinguish strong candidates.
- **Simon Willison** - [simonwillison.net](https://simonwillison.net/) - coined and documented prompt injection (see his [prompt injection tag](https://simonwillison.net/tags/prompt-injection/)); the reference for LLM security questions and pragmatic tooling takes.
- **Anthropic engineering** - [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) argues workflows-before-agents (a favourite interviewer stance); [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) is a concrete, numbers-backed RAG improvement worth citing verbatim.
- **OpenAI Cookbook** - [cookbook.openai.com](https://cookbook.openai.com/) - working code for RAG, evals, function calling, and fine-tuning; good for grounding answers in real API mechanics.

---

## 3. Courses & hands-on

Interviewers can tell within minutes whether you've built things or only read about them. These close that gap.

- **Andrej Karpathy - Neural Networks: Zero to Hero** - [karpathy.ai/zero-to-hero.html](https://karpathy.ai/zero-to-hero.html) - build backprop, a language model, and GPT from scratch; the single best preparation for "explain it from first principles" questions.
- **nanoGPT** - [github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) - a readable GPT training loop; if you can walk through this repo, you can survive any transformer-internals grilling.
- **minbpe** - [github.com/karpathy/minbpe](https://github.com/karpathy/minbpe) - BPE tokenization from scratch; tokenizer questions ("why do models claim 9.11 > 9.9?") stop being scary after this.
- **fast.ai - Practical Deep Learning** - [course.fast.ai](https://course.fast.ai/) - the fastest route to solid DL intuition if your foundations are shaky; top-down and code-first.
- **Hugging Face courses** - [huggingface.co/learn](https://huggingface.co/learn) - the LLM/NLP course covers the transformers ecosystem you'll be assumed to know; the [Agents course](https://huggingface.co/learn/agents-course) is a practical tour of tool use and agent patterns.
- **DeepLearning.AI short courses** - [deeplearning.ai/short-courses](https://www.deeplearning.ai/short-courses/) - 1-2 hour courses on RAG, evals, agents, and fine-tuning, often taught with the relevant vendor; efficient for patching specific gaps.
- **Full Stack Deep Learning / LLM Bootcamp** - [fullstackdeeplearning.com](https://fullstackdeeplearning.com/) - production-focused lectures that align closely with how AI system design interviews are framed.
- **Eval-focused cohort courses** - Hamel Husain and Shreya Shankar teach a well-known "AI Evals for Engineers" cohort course on Maven; worth knowing the curriculum exists since evals are the hottest interview topic of 2025-2026 (find it by name on maven.com).

---

## 4. Books

- **AI Engineering - Chip Huyen (O'Reilly, 2025)** - the closest thing to an official textbook for this interview loop: evals, RAG, fine-tuning decisions, inference optimization, all framed as engineering tradeoffs.
- **Designing Machine Learning Systems - Chip Huyen (O'Reilly, 2022)** - pre-LLM ML systems thinking (data, deployment, monitoring, feedback loops) that still underpins half of system design interviews.
- **Build a Large Language Model (From Scratch) - Sebastian Raschka (Manning, 2024)** - implement GPT end-to-end in PyTorch; companion code at [github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch). Ideal for coding-round prep.
- **Hands-On Large Language Models - Jay Alammar & Maarten Grootendorst (O'Reilly, 2024)** - visual, practical coverage of embeddings, transformers, and applications; the fastest reading of the four.
- **Deep Learning - Goodfellow, Bengio & Courville (MIT Press, 2016)** - [deeplearningbook.org](https://www.deeplearningbook.org/) (free online) - reference-grade foundations; use selectively for optimization/regularization chapters, don't read cover to cover.

---

## 5. Staying current

Interviews as of 2026 routinely reference things released in the last six months. You need a low-effort pipeline for staying current.

**Newsletters & feeds**
- **Latent Space** - [latent.space](https://www.latent.space/) - defined the "AI Engineer" role; best signal on what skills the market (and interviewers) currently care about.
- **Interconnects - Nathan Lambert** - [interconnects.ai](https://www.interconnects.ai/) - the best public writing on post-training, RLHF/DPO/GRPO, and reasoning models; directly feeds alignment-question answers.
- **Simon Willison's weblog** - [simonwillison.net](https://simonwillison.net/) - near-daily, pragmatic coverage of new models and tools; his model release notes are perfect interview-day briefings.
- **Ahead of AI - Sebastian Raschka** - [magazine.sebastianraschka.com](https://magazine.sebastianraschka.com/) - research digests with enough technical depth to actually explain the papers, not just list them.

**Podcasts**
- **Latent Space podcast** - practitioner interviews about building with LLMs; good for absorbing the vocabulary of production AI engineering.
- **Dwarkesh Podcast** - [dwarkeshpatel.com](https://www.dwarkeshpatel.com/) - long-form interviews with researchers (Sutskever, Amodei, Karpathy, et al.); best for research-depth context at frontier-lab interviews.

**Communities**
- **r/LocalLLaMA** - [reddit.com/r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) - the pulse of the open-weights world: quantization, local serving, and new model release chatter.
- **Hugging Face and EleutherAI Discords** - where practitioners debug training and inference in the open; lurking teaches you real failure modes.

---

## 6. Practice & benchmarking

- **LMArena** - [lmarena.ai](https://lmarena.ai/) - crowdsourced pairwise model battles (Elo-style); know how it works because "how would you compare two models?" is a standard eval question.
- **Hugging Face leaderboard ecosystem** - [huggingface.co](https://huggingface.co/) - hosts most public leaderboards as Spaces (the original Open LLM Leaderboard is now retired - knowing *why* benchmark saturation and contamination killed it is itself good interview material).
- **SWE-bench** - [swebench.com](https://www.swebench.com/) - the benchmark for agentic coding on real GitHub issues; the reference point for any coding-agent design discussion.
- **MTEB leaderboard** - [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) - where embedding models are compared; check it before answering "which embedding model would you pick?"

> **Caution - leaderboard-driven thinking is a red flag.** Saying "I'd pick whatever tops the leaderboard" signals junior judgment. Public benchmarks suffer contamination, saturation, and distribution mismatch with your task. The strong-candidate answer is always: leaderboards for a shortlist, *your own task-specific evals* for the decision.

---

## 7. Docs worth reading end-to-end

Vendor docs are underrated interview prep - they encode each lab's official position on prompting, tool use, and agents.

- **OpenAI docs** - [platform.openai.com/docs](https://platform.openai.com/docs) - read the prompting, function calling / tool use, and agents guides; also structured outputs, which comes up constantly in production-integration questions.
- **Anthropic (Claude) docs** - [platform.claude.com/docs](https://platform.claude.com/docs) - the prompt engineering section is the most thorough of any vendor (system prompts, XML structuring, chaining); read the tool use and agent guides too.
- **Google AI (Gemini) docs** - [ai.google.dev](https://ai.google.dev/) - read the long-context and prompting strategy sections; Gemini's 1M+ token context makes it the standard example in "long context vs. RAG" debates.
- **vLLM docs** - [docs.vllm.ai](https://docs.vllm.ai/) - read the pages on PagedAttention, continuous batching, and quantization support; this is exactly the material inference/serving interview rounds are built from.
- **Model Context Protocol (MCP)** - [modelcontextprotocol.io](https://modelcontextprotocol.io/) - read the core spec concepts (tools, resources, prompts, transports); as of 2026 MCP is the assumed answer to "how do you standardise tool integration for agents?"

---

*Back to the [main guide](../README.md).*
