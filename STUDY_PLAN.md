# 📅 Study Plans

Three plans depending on how much runway you have. All of them assume ~2 hours/day on weekdays and a longer weekend block. Whichever plan you pick, the method is the same:

1. **Read the crash course** (`README.md`) in each topic first - it's the compressed theory.
2. **Self-quiz with `questions.md`** - read the question, answer *out loud* before opening the collapsible answer. Speaking your answers is the single highest-leverage habit in interview prep.
3. **Type out the coding challenges yourself** - don't read the solutions first. The interview is a blank editor, not a multiple-choice test.
4. **Practice system design on a whiteboard or doc**, talking through the [framework](11-ai-system-design/) before checking the case study.
5. The night before any interview: [CHEATSHEET.md](CHEATSHEET.md).

---

## 🔥 1-week cram (interview on the calendar)

Triage plan. Skip depth, maximise coverage of what's most likely to be asked.

| Day | Focus | Material |
|-----|-------|----------|
| 1 | LLM fundamentals | [02-llm-fundamentals](02-llm-fundamentals/) crash course + Basic/Intermediate questions |
| 2 | RAG + prompting | [04-rag-and-retrieval](04-rag-and-retrieval/) + [03-prompt-engineering-and-context](03-prompt-engineering-and-context/) crash courses, skim questions |
| 3 | Agents + evals | [06-agents-and-tool-use](06-agents-and-tool-use/) + [07-evaluation-and-observability](07-evaluation-and-observability/) crash courses + Basic questions |
| 4 | Coding reps | [12-coding-challenges](12-coding-challenges/): 01 attention, 03 sampling, 08 mini-RAG - implement before peeking |
| 5 | System design | [11-ai-system-design](11-ai-system-design/) framework + the case study closest to the company's product |
| 6 | Production + safety | [08-inference-and-production](08-inference-and-production/) Basic/Intermediate + [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/) crash course |
| 7 | Simulate + rest | [13-interview-process-and-behavioral](13-interview-process-and-behavioral/) - prep 5 STAR stories; evening: [CHEATSHEET.md](CHEATSHEET.md) only |

Skip if you must: [10-multimodal](10-multimodal/) (unless the role touches vision/audio), Advanced questions everywhere.

---

## 🎯 4-week standard plan (most people)

One theme per week; coding challenges spread throughout so implementation skills compound.

### Week 1 - Foundations & the model
- Days 1-2: [01-ml-and-dl-foundations](01-ml-and-dl-foundations/) - full pass.
- Days 3-5: [02-llm-fundamentals](02-llm-fundamentals/) - full pass, including Advanced.
- Weekend: challenges [01 attention](12-coding-challenges/), 02 BPE, 03 sampling, 04 positional encodings, 05 layernorm/softmax.

### Week 2 - Context: prompting, RAG, fine-tuning
- Days 1-2: [03-prompt-engineering-and-context](03-prompt-engineering-and-context/) - full pass.
- Days 3-4: [04-rag-and-retrieval](04-rag-and-retrieval/) - full pass.
- Day 5: [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/) - crash course + Basic/Intermediate.
- Weekend: challenges 08 semantic search/RAG, 09 chunking; finish fine-tuning Advanced questions.

### Week 3 - Agents, evals, production
- Days 1-2: [06-agents-and-tool-use](06-agents-and-tool-use/) - full pass.
- Day 3: [07-evaluation-and-observability](07-evaluation-and-observability/) - full pass. Do not skip this; it's the most senior-signalling topic in the repo.
- Days 4-5: [08-inference-and-production](08-inference-and-production/) - full pass.
- Weekend: challenges 06 KV cache, 10 agent loop, 11 rate limiter, 12 eval metrics.

### Week 4 - Design, safety, polish
- Day 1: [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/) + [10-multimodal](10-multimodal/) crash courses.
- Days 2-3: [11-ai-system-design](11-ai-system-design/) - framework, then 3 case studies as mock interviews: 45 minutes talking into a doc *before* reading the solution.
- Day 4: [13-interview-process-and-behavioral](13-interview-process-and-behavioral/) - write your 5-7 STAR stories down.
- Day 5: challenges 07 mini-GPT forward, 13 streaming parser (the hard ones).
- Weekend: full mock loop - one coding challenge cold, one design prompt from the rapid-fire list, behavioural answers out loud. Then [CHEATSHEET.md](CHEATSHEET.md).

---

## 🏗 8-week deep plan (career transition into AI engineering)

Weeks 1-4: same as the 4-week plan, at half pace - and **build while you learn**:

- After Week 2's material → build a small RAG app over your own notes/docs **with an eval harness** (even 30 golden questions). This single project teaches more than any tutorial.
- After Week 3's material → add an agent with 2-3 tools to it, plus tracing.

Weeks 5-8:

| Week | Focus |
|------|-------|
| 5 | Depth: re-do every **Advanced** section across topics 02, 04, 05, 06, 08. Read 5-6 foundational papers from [resources](resources/) (Attention, InstructGPT, LoRA, DPO, ReAct at minimum). |
| 6 | Projects: polish one portfolio project to "shows evals + error analysis + tradeoff writeup" standard (see project ideas in [13-interview-process-and-behavioral](13-interview-process-and-behavioral/)). |
| 7 | System design: all 8 case studies in [11-ai-system-design](11-ai-system-design/) as timed mocks. All 13 coding challenges done cold. |
| 8 | Interview simulation: mock loops with a friend or by recording yourself; behavioural stories rehearsed; company-specific research; [CHEATSHEET.md](CHEATSHEET.md) passes. |

---

## Retention tips

- **Spaced repetition beats rereading.** Second pass on a topic 3-4 days after the first, third pass a week later. The `questions.md` files are already flashcard-shaped - question first, answer hidden.
- **Track your misses.** Keep a running list of questions you fumbled; re-quiz only those on later passes.
- **Explain to a human (or a rubber duck).** If you can't explain the KV cache to a non-ML friend, you don't own it yet.
- **Do the numbers by hand once.** GPU memory maths, KV cache size, cost-per-request token maths - each done once on paper sticks forever.
