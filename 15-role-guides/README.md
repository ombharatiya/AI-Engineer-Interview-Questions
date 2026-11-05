# 🧑‍🔧 Role Guides

AI questions now show up in backend, frontend, product, data, DevOps, QA, mobile and security loops, and the depth expected varies a lot by role. A backend engineer is not graded on RoPE, and a security engineer is not graded on chunk sizes. These guides tell you which parts of the repo are yours and which you can safely skip.

Every guide follows the same shape:

- **How this role's interviews changed (2024 to 2026)** - what actually moved, stage by stage.
- **What you're actually expected to know** - calibrated depth per topic, including the topics you can skip.
- **Study map** - which sections of this repo to read, in which order, for this role.
- **Role-specific interview questions** - the questions this role really gets at the AI boundary, with worked answers.
- **Portfolio moves** - the project that proves this skill set to an interviewer.
- **Red flags interviewers see from this role** - the failure patterns specific to your background.

## The guides

| Role | Guide | What the loop tests | Questions |
|---|---|---|---|
| Backend Engineer | [backend-engineer.md](backend-engineer.md) | Building reliable systems around a slow, expensive, rate-limited, non-deterministic dependency: streaming, timeouts, token-based rate limits, cost per call | 15 |
| Frontend Engineer | [frontend-engineer.md](frontend-engineer.md) | Making a slow, occasionally wrong backend feel fast, trustworthy and safe: streaming UI, partial state, citation and error affordances | 16 |
| Product / Full-stack Engineer | [product-engineer.md](product-engineer.md) | Shipping a working LLM feature end to end in days, knowing when not to use AI, and proving it works with scrappy but real evals | 15 |
| Forward Deployed Engineer | [forward-deployed-engineer.md](forward-deployed-engineer.md) | The two-halves loop: full-stack plus AI application depth, and the decomp interview where you carve a vague business problem into a buildable v1 | 17 |
| Data Engineer | [data-engineer.md](data-engineer.md) | RAG ingestion as an ETL problem: parsing, chunking, embedding, incremental sync, delete propagation, re-index migrations | 15 |
| DevOps / Platform / MLOps Engineer | [devops-platform-engineer.md](devops-platform-engineer.md) | Running GPU fleets, minutes-long cold starts, 140 GB deploy artifacts, and a dependency whose failures look like wrong answers rather than 500s | 17 |
| QA / SDET Engineer | [qa-sdet-engineer.md](qa-sdet-engineer.md) | Testing rebuilt around distributions instead of exact values: eval harnesses as test suites, judge calibration, red-team regression, CI gates | 15 |
| Mobile Engineer | [mobile-engineer.md](mobile-engineer.md) | On-device versus cloud, streaming over a flaky radio, shipping gigabytes of weights without wrecking battery life or app size | 15 |
| Security Engineer | [security-engineer.md](security-engineer.md) | Threat-modelling a system where instructions and data share one channel: injection, tool scopes, OWASP LLM Top 10, agent blast radius | 16 |
| "Am I an ML Engineer or an AI Engineer?" | [ml-engineer-vs-ai-engineer.md](ml-engineer-vs-ai-engineer.md) | Decoding the four titles, mapping each to a loop, transition paths in both directions, and the boundary questions both roles get | 15 |

## How to use these

1. **Read your guide's study map first.** It tells you which of the 13 topic sections matter for your loop and in what order, which is a much shorter list than the full repo.
2. **Decode the job description, not the title.** If an "AI Engineer" posting lists CUDA and pretraining, it is a research engineering loop wearing a different name. The [title decoder](ml-engineer-vs-ai-engineer.md) covers this.
3. **Read a second guide if the role straddles two.** Platform roles that own the gateway want the backend guide too, and anything customer-facing benefits from the FDE guide.
4. **Then go broad.** The [AI Engineer 75](../AI-ENGINEER-75.md) is the cross-role baseline, and the [cheat sheet](../CHEATSHEET.md) is the night-before pass.

---

**Related:** [Main index](../README.md) · [The AI Engineer 75](../AI-ENGINEER-75.md) · [Study plans](../STUDY_PLAN.md) · [Glossary](../GLOSSARY.md) · [Company interview questions](../14-company-interview-questions/README.md)
