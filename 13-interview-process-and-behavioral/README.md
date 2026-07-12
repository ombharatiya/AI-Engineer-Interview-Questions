# 💼 Interview Process & Behavioral

Every AI engineering loop ends the same way: a behavioural round where they decide whether they'd actually want to work with you, and a debrief where "strong technically, but couldn't explain what they shipped" kills offers. This section is a field guide to the whole process - what the 2026 loop actually looks like stage by stage, how it differs by company type, what take-homes and portfolios need to prove, and how to tell your AI work stories so they land. Everyone gets asked this material, from new grads to staff candidates; seniors get asked it harder.

## Anatomy of the 2026 AI Engineer loop

A typical full loop is 4-6 rounds over 2-5 weeks. Stages vary, but this is the common skeleton:

**1. Recruiter screen (30 min).** Logistics, motivation, level calibration, comp expectations. Two things matter: have a crisp 90-second summary of your most impressive AI project (with a number in it), and don't anchor low on comp - deflect with "I'm optimising for the right role; I trust we can make comp work if there's mutual fit" until you have data (see offer section below).

**2. Coding (1-2 rounds).** The bar is real and has *risen* at AI companies, not fallen. Expect one of:
- **LeetCode-lite / practical DSA**: strings, hashmaps, heaps, BFS/DFS at medium difficulty, graded on working code and communication more than optimal asymptotics.
- **"Build a thing that calls an LLM"**: increasingly common. E.g. "implement a chat loop with tool calling", "build a rate-limited async client that batches requests", "parse this messy output into a schema with retries". Tests API fluency, async Python, error handling, and whether you've actually done this before. Practice writing a tool-use loop from scratch without a framework.
- **AI-assisted coding rounds**: some companies now *let or require* you to use Copilot/Claude during the interview and grade how you direct the tool, verify its output, and catch its bugs. Ask the recruiter which rules apply.

**3. ML/AI domain deep-dive (1 round).** Conceptual depth on your resume's claims: transformers, sampling, fine-tuning vs RAG vs prompting, evals, hallucination mitigation. Sections 01-10 of this repo are this round. The interviewer probes until you break - knowing where your knowledge ends and saying so beats bluffing every time.

**4. AI system design (1 round).** "Design a support copilot / enterprise RAG / agent platform." Section 11 covers this. Differentiator: leading with evals, cost, and failure modes rather than boxes and arrows.

**5. Behavioral (1 round, sometimes woven throughout).** The questions in [questions.md](questions.md). At senior+ levels this round carries as much weight as any technical round.

**6. Sometimes: take-home or paid work trial.** Covered below. Startups especially; a few run 1-5 day paid on-site trials in place of parts of the loop.

## How loops differ by company type

| | Frontier labs (OpenAI, Anthropic, Google DeepMind, Meta) | Big tech (AWS, Azure, GCP orgs, product teams) | AI-native startups | Enterprises adopting AI |
|---|---|---|---|---|
| **Coding bar** | Very high; often multiple rounds, real-world flavored | High, standard DSA + practical | Practical > algorithmic; ship a working thing fast | Moderate; language/stack fluency |
| **Domain round** | Deep - expect paper-level fluency on attention, RLHF/GRPO, scaling, inference | Breadth + how you'd productionise | Applied: RAG, agents, evals, "what would you build with X" | Integration: APIs, data pipelines, vendor tradeoffs |
| **System design** | Research infra or serving at extreme scale | Classic distributed systems + AI layer | Product-shaped: 0→1 feature design | Reliability, compliance, cost governance |
| **What wins offers** | Depth + research fluency + exceptional coding | Scale experience, process maturity, cross-team stories | Shipping speed, breadth, product sense, portfolio | Risk management, stakeholder skills, pragmatism |
| **Watch out for** | Long loops, research-y curveballs | Level-mapping games, org-dependent bar | Founder gut-feel rounds, work trials | Buzzword screens by non-experts |

Calibrate your prep: for a frontier lab, over-invest in sections 01-02 and 05; for a startup, have a portfolio project you can demo and defend end to end; for big tech, rehearse cross-functional behavioural stories with scope and numbers.

## Role-title decoder

Titles are inconsistent across companies - read the job description, not the title. Rough decoding:

- **AI Engineer / GenAI Engineer**: builds products *on top of* models - RAG, agents, prompting, evals, serving integration. Mostly software engineering with an LLM-specific layer. Asked: everything in this repo except deep training math.
- **ML Engineer (MLE)**: trains, tunes, and deploys models; owns pipelines, feature stores, training infra. More classical ML + infra. Asked: ML foundations, MLOps, distributed training, plus increasingly the LLM layer.
- **Research Engineer (RE)**: implements and scales research ideas at labs - training runs, ablations, performance engineering. Heavy coding bar + solid ML theory; publications optional but paper fluency required. Asked: implement attention from scratch, debug a training run, GPU/parallelism questions.
- **Applied Scientist / Research Scientist**: designs experiments, owns metrics and modelling choices; RS usually requires publications. Asked: statistics, experimental design, modelling depth, paper discussions.

If an "AI Engineer" JD lists CUDA and pretraining, it's an RE role in disguise. If an "MLE" JD is all LangChain and vector DBs, it's AI Engineering. Interview prep should follow the JD's actual content.

## Take-home assignments

Typical ask: "Build a small RAG/agent/extraction service over this data; ~4-8 hours." What graders actually score, in rough priority order:

1. **It runs.** One-command setup, pinned deps, no missing API key surprises. Working and boring beats ambitious and broken - graders spend 15 minutes, and a crash in minute one is fatal.
2. **Evals included.** The single biggest differentiator in 2026. Even 15 hand-written test cases with a pass/fail script signals more seniority than any architecture choice. Include a failure analysis: "it fails on X because Y."
3. **README with tradeoffs.** What you built, what you deliberately didn't, what you'd do with another week. Naming your shortcuts ("no streaming, sync calls only - acceptable at this scale because...") reads as senior; hiding them reads as junior.
4. **Sensible engineering**: typed code, error handling on every LLM call, cost/token awareness, no framework soup for a 300-line problem.

**Scoping your time**: timebox to the stated hours plus ~25%. Spend it roughly 50% core functionality, 25% evals + error analysis, 25% README and cleanup. Do not gold-plate the UI.

**When to decline**: unpaid work exceeding ~a day, assignments suspiciously identical to the company's actual roadmap, or take-homes issued before any human has talked to you. It's fine to counter-offer: "I can't do 20 hours unpaid, but here's a repo of mine that demonstrates the same skills - happy to walk through it live."

**On AI assistance**: assume they'll ask you to defend every line in a follow-up call. Use whatever tools you want, but if you can't explain a design choice, you didn't make it.

## Portfolio & projects that actually impress

One deep project with evals and a writeup beats ten "I cloned a YouTube tutorial" repos. Concrete ideas, each with what it signals:

1. **RAG app over a messy real corpus** (your notes, a gnarly docs site, court filings) with a real eval harness - retrieval metrics, faithfulness checks, and an error-analysis writeup clustering the failures. *Demonstrates: retrieval fundamentals + the eval maturity most candidates lack.*
2. **An agent with sandboxed tool execution** - e.g. a coding or data-analysis agent that runs tools in Docker with permission gating, timeouts, and an audit log. *Demonstrates: agent design plus the security thinking interviewers rarely see.*
3. **Tokenizer + transformer from scratch** - BPE tokenizer and a small GPT-style model in pure PyTorch (Karpathy's zero-to-hero path), trained on a toy corpus, with notes on what you learned. *Demonstrates: fundamentals that survive the deepest domain round.*
4. **An inference benchmark writeup** - same model on vLLM vs llama.cpp vs a provider API: TTFT/throughput curves vs batch size and context length, cost per million tokens, methodology stated. *Demonstrates: serving knowledge and empirical rigor.*
5. **A fine-tune with before/after evals** - LoRA a small open model on a narrow task; compare against a prompted frontier model on quality, latency, and cost; publish the verdict even if fine-tuning *lost*. *Demonstrates: you know when fine-tuning is and isn't worth it - a top-tier interview signal.*
6. **LLM-as-judge calibration study** - build a judge for some task, measure agreement against your own human labels, document position/length/self-preference biases you found. *Demonstrates: eval sophistication beyond "we used GPT to grade it."*
7. **Structured-extraction pipeline** - thousands of messy documents → validated schema, with retries, cost tracking, and an accuracy report. *Demonstrates: unglamorous production engineering, which is most of the actual job.*
8. **An MCP server for a real tool or data source** - with auth, input validation, and tests, usable from Claude/IDE clients. *Demonstrates: current integration patterns and API design.*
9. **A model router / semantic cache** - small classifier or heuristic routing easy queries to a cheap model, hard ones to a frontier model, with a measured quality-vs-cost frontier. *Demonstrates: cost engineering with data.*
10. **A voice or multimodal app with a latency budget** - document the end-to-end pipeline and where every millisecond goes, plus what you did about the worst hop. *Demonstrates: streaming, UX-under-latency, systems thinking.*

Every project needs three artifacts: a README with numbers, an evals/ directory, and a short writeup of what surprised you. The writeup is what interviewers actually read.

## Resume tips for AI roles

- **Metrics on every bullet, evals where possible.** "Shipped RAG assistant" is noise. "Shipped support RAG assistant to 40k users; raised answer-acceptance from 61%→78% on a 500-case eval; cut cost/query ~70% via caching + model routing" gets an interview. If you can't share internal numbers, use relative deltas and scale indicators.
- **Ship dates and durations.** "Prototype→GA in 9 weeks" signals velocity. Recency matters in this field - lead with 2024-2026 work.
- **Link to artifacts.** GitHub repos, writeups, demos, papers. A resume claim with a clickable proof is worth three without.
- **Name the layer you owned.** "Owned retrieval + eval pipeline" beats a vague "worked on AI chatbot." Interviewers drill exactly where your bullets claim ownership - make sure you can go three questions deep on each one.
- **Kill the keyword soup.** A skills line with 30 frameworks reads as junior. List what you'd be comfortable being grilled on, nothing else.
- **Don't inflate.** "Fine-tuned GPT-4" when you wrote prompts, or "trained an LLM" when you ran LoRA on a 7B for an afternoon, will be discovered in round one and poisons everything after.

## Staying current without drowning

You cannot read everything; interviewers don't expect you to. They expect a *system*. A sane weekly diet (~3 hours):

- **One curated digest** for breadth - pick one or two of: a good newsletter, Latent Space, Simon Willison's blog, Hacker News AI threads.
- **One thing read deeply** - a paper, a model card, or a serious engineering blog post. Depth on one thing per week compounds; skimming forty abstracts doesn't.
- **Release notes of the providers you use** - model deprecations, API changes, pricing. This is job-relevant in a way most papers aren't.
- **One hands-on hour** - try the new model/tool on *your own* eval set or side project. "I ran it on my benchmark and noticed X" is an elite interview answer; "I saw a thread about it" is not.

And explicitly *skip*: the all-day feed, launch-day hot takes, and any paper you can't connect to something you build.

## Questions YOU should ask interviewers

Great questions are diagnostic for you *and* signal seniority. Ask about:

- **Evals culture**: "How do you know a prompt or model change is safe to ship? Walk me through the last one." (No real answer = you'll be firefighting vibes-driven regressions.)
- **Data access**: "What data can the team actually use for training/evals, and how long does access take?" (Months-long data approval kills AI teams quietly.)
- **GPU/budget reality**: "What's the compute and API budget situation - do experiments queue behind production?"
- **How they ship**: "What's the path from notebook to production? Who can push a prompt change, and what gates it?"
- **On-call**: "Are AI features on-call? What does an incident look like - who debugs a quality regression at 2am?"
- **Model strategy**: "What happened during your last model migration/deprecation?" (Tells you how coupled they are to one vendor and how much tech debt you're inheriting.)
- **For startups**: runway, who the design partners/customers are, and what the last pivot was.

## Offer evaluation basics

General guidance only - do your own research with current data:

- **Level mapping is the game.** The same experience maps to different levels at different companies, and comp is set by level. Before negotiating dollars, negotiate level - one level is usually worth far more than any within-band bump. Use [levels.fyi](https://www.levels.fyi/) and peer conversations to calibrate titles across companies.
- **AI startup equity**: understand the difference between your strike price (409A) and the preferred price from the last round; the headline "your equity is worth $X" uses the latter. Ask about total dilution expectations, exercise windows, and whether the company has allowed secondary sales. High valuations in AI mean high preference stacks - model the downside, not just the unicorn case.
- **Cash vs. equity mix**: frontier labs and big tech pay heavily in equity (liquid at public cos, less so elsewhere). A startup offer that's 40% below big-tech cash needs a believable equity story to compete - make them make it.
- **Comp research sources**: levels.fyi, H-1B salary disclosures (public record in the US), recruiter conversations at peer companies, and simply asking your network. Never negotiate from a single data point.
- **Non-comp terms that matter in AI roles**: compute/GPU access, publication policy, IP carve-outs for side projects, on-call expectations, and remote policy. For research-adjacent roles, publication rights can be worth more than a pay bump for your long-term market value.

## Interview questions

22 behavioural and experience questions specific to AI work, with answer guidance, in [questions.md](questions.md).

## Red flags interviewers watch for

- **No numbers anywhere.** Every project story lacks users, latency, cost, or eval metrics - signals you watched the work happen rather than owning it.
- **"We didn't have time for evals."** The single fastest seniority downgrade in 2026. Even scrappy teams hand-label 50 cases.
- **Blaming the model.** "GPT-whatever just hallucinated" with no mitigation story shows you stopped debugging at the API boundary.
- **Claiming the team's win in first person singular** - then failing two follow-up questions deep on how it actually worked.
- **Resume inflation on training claims.** Saying "fine-tuned"/"trained" for what was prompt engineering unravels in minutes and taints every other claim.
- **Framework name-dropping instead of understanding** - can recite LangChain/LlamaIndex but can't describe what an agent loop does without them.
- **No questions for the interviewer**, or only questions about perks - reads as low ownership and low curiosity.
- **Badmouthing a previous employer or team** - even when justified, it transfers the negativity onto you.

## Further reading

- [levels.fyi](https://www.levels.fyi/) - level mapping and compensation data across companies.
- [Machine Learning Interviews Book - Chip Huyen](https://huyenchip.com/ml-interviews-book/) - the classic free book on ML interview loops, roles, and preparation.
- [Applied LLMs - What We Learned from a Year of Building with LLMs](https://applied-llms.org/) - practitioner lessons (evals, RAG, ops) that map directly to interview stories.
- [Your AI Product Needs Evals - Hamel Husain](https://hamel.dev/blog/posts/evals/) - the eval-maturity playbook interviewers increasingly expect you to have internalised.
- [Simon Willison's blog](https://simonwillison.net/) - high-signal, hands-on coverage of new models and tools; a model for "staying current" done right.
- [Latent Space](https://www.latent.space/) - podcast/newsletter on AI engineering as a discipline, including hiring and role definitions.
- [Neural Networks: Zero to Hero - Andrej Karpathy](https://karpathy.ai/zero-to-hero.html) - the canonical from-scratch path for the fundamentals portfolio project.
- [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/) - industry context on hiring processes, levels, and how tech companies actually run loops.
