# 🏢 Company Interview Questions

Interview questions, loop maps and prep priorities for 33 companies, tiered from frontier labs to applied AI shops and spanning the US, Europe, China and India, including inference silicon, vertical AI, autonomy and robotics.

Everything here is built from public information: job postings, engineering blogs, technical reports and publicly shared candidate reports. No confidential or leaked material. Processes change and vary by team, so every page carries a "last reviewed" date, marks uncertain stage detail as reported, and lists its sources at the bottom. Treat these as maps, not contracts.

Every page follows the same shape: **TL;DR**, **company context**, **roles and titles they hire**, **the interview loop** stage by stage, **what they emphasise**, 12 to 15 representative questions with worked answers, **how to prepare**, and **sources**.

## Frontier labs

| Company | Page | What the loop centres on |
|---|---|---|
| Anthropic | [anthropic.md](anthropic.md) | Mission alignment tested seriously, practical staged coding over puzzles, evals as an engineering discipline, a values round that decides offers |
| OpenAI | [openai.md](openai.md) | Shipping-grade code under time pressure, test coverage as a graded criterion, depth behind every decision, full-stack LLM literacy |
| Google DeepMind | [google-deepmind.md](google-deepmind.md) | Breadth on real fundamentals, code that runs unaided, research taste even for engineers, scale engineering |
| Meta | [meta-ai.md](meta-ai.md) | The software engineering bar first, directing AI rather than resisting it, business-metric fluency, end-to-end ownership |
| xAI | [xai.md](xai.md) | Shipping over pedigree, practical code under changing requirements, reading unfamiliar code fast, appetite for intensity |
| Mistral AI | [mistral.md](mistral.md) | Model internals as shipped (GQA, sliding-window attention, sparse MoE), inference economics, open-weight conviction and EU context |
| DeepSeek | [deepseek.md](deepseek.md) | Efficiency as a first principle, implementation over ideas, breadth across the LLM stack, RL for reasoning |
| Moonshot AI | [moonshot-ai.md](moonshot-ai.md) | Long context as a real problem rather than a spec number, KV-cache and serving economics, MoE at trillion-parameter scale |
| Zhipu AI | [zhipu-ai.md](zhipu-ai.md) | GLM-lineage fluency, agentic and reasoning and coding capability, RL at scale, bilingual and multimodal grounding |
| Sarvam AI | [sarvam-ai.md](sarvam-ai.md) | Indic tokenization and fertility, code-mixed Indian speech and text, low-latency voice pipelines, adaptation with scarce data |

## Big tech

| Company | Page | What the loop centres on |
|---|---|---|
| Microsoft | [microsoft.md](microsoft.md) | Growth mindset stated explicitly, thought process over the right answer, classic CS fundamentals even for AI roles, enterprise-grade thinking |
| Amazon | [amazon.md](amazon.md) | Leadership Principles operationalised, Dive Deep as a technical signal, operational excellence, frugality applied to GPUs |
| Apple | [apple.md](apple.md) | Efficiency engineering, privacy-preserving ML as architecture, hardware-software co-design, product judgment and discretion |
| NVIDIA | [nvidia.md](nvidia.md) | Hardware-software co-design over model trivia, performance maths on the spot, C++ and systems depth, CUDA reading fluency |
| Qwen (Alibaba) | [qwen-alibaba.md](qwen-alibaba.md) | Model internals as shipped, multilingual and Chinese-first thinking, coding and maths reasoning, serving economics |

## AI-native and infrastructure

| Company | Page | What the loop centres on |
|---|---|---|
| Databricks | [databricks.md](databricks.md) | A deliberately high coding bar, concurrency as a first-class skill, written design communication, production pragmatism |
| Scale AI | [scale-ai.md](scale-ai.md) | Speed with correctness, human-in-the-loop systems thinking, evaluation as a discipline, post-training literacy |
| Perplexity | [perplexity.md](perplexity.md) | Latency as a value system, retrieval and ranking depth, production readiness over algorithmic flash, Python fluency |
| Cursor (Anysphere) | [cursor-anysphere.md](cursor-anysphere.md) | End-to-end ability in a real codebase, what you build unprompted, authentic daily use of the product, latency and cost obsession |
| Cohere | [cohere.md](cohere.md) | Retrieval as a first-class discipline, enterprise deployment constraints, agentic workflows with supervision, evaluation rigour |
| Hugging Face | [hugging-face.md](hugging-face.md) | Open-source contributions over credentials, autonomy, ecosystem fluency, written communication and demo sense |
| Together AI | [together-ai.md](together-ai.md) | Performance engineering as product, inference economics, full-stack systems ownership, research-to-production speed |
| Glean | [glean.md](glean.md) | Search and IR fundamentals rather than LLM plumbing, permissions as a first-class constraint, evaluation discipline |
| Cognition (Devin, Windsurf) | [cognition-devin.md](cognition-devin.md) | The harness is the product, context engineering over orchestration cleverness, long-horizon reliability, benchmarks as a floor |
| Groq | [groq.md](groq.md) | Compiler-scheduled determinism, memory hierarchy as the whole argument, scale-out sharding, latency as the product |
| ElevenLabs | [elevenlabs.md](elevenlabs.md) | Real-time latency as a product constraint, end-to-end ownership, safety and misuse as engineering, evaluation without ground truth |
| Character.AI | [character-ai.md](character-ai.md) | Cost per message rather than per GPU-hour, KV cache as the binding constraint, cross-turn caching, kernel-level ownership |

## Applied, vertical and forward-deployed

| Company | Page | What the loop centres on |
|---|---|---|
| Palantir | [palantir.md](palantir.md) | Decomposition of ambiguity, learning velocity over accumulated knowledge, ontology-first thinking for AI work, mission seriousness |
| Sierra | [sierra.md](sierra.md) | AI-leveraged building end to end, reliability as a discipline, pass^k thinking, release engineering for agents |
| Harvey | [harvey.md](harvey.md) | Retrieval that respects document structure, citation grounding as a product requirement, hallucination measured rather than asserted |
| Abridge | [abridge.md](abridge.md) | Speech under real-world conditions, grounding as a product feature, hallucination as patient safety, evaluation where ground truth is fuzzy |
| Waymo | [waymo.md](waymo.md) | Safety as an engineering artefact, evaluation of rare events, modular versus end-to-end resolved as a hybrid, simulation as infrastructure |
| Figure AI | [figure-ai.md](figure-ai.md) | Real robots over simulation, one model driving many behaviours, the full-body pixels-to-actuators story, latency as a hard constraint |

## How to use this section

1. **Read the TL;DR and the loop map first.** Knowing that a company runs a values round, a take-home, or a solution-architecture presentation changes what you prepare far more than any single question does.
2. **Work the representative questions cold.** Answer out loud before opening the worked answer, the same discipline as the [AI Engineer 75](../AI-ENGINEER-75.md).
3. **Use "what they emphasise" to pick your revision topics.** A serving-heavy company wants [08 Inference](../08-inference-and-production/README.md); a retrieval-heavy one wants [04 RAG](../04-rag-and-retrieval/README.md).
4. **Confirm stage detail with your recruiter.** Loops change quietly, and anything marked "reported, varies" is exactly that.

---

**Related:** [Main index](../README.md) · [The AI Engineer 75](../AI-ENGINEER-75.md) · [Night-before cheat sheet](../CHEATSHEET.md) · [Glossary](../GLOSSARY.md) · [Role guides](../15-role-guides/README.md)
