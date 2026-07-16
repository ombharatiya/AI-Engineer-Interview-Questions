# Interview Process & Behavioral - Interview Questions

35 questions: 10 basic, 13 intermediate, 12 advanced. Answers here are guidance - what the interviewer is probing, how to structure a strong answer (STAR-ish: Situation → Task → Action → Result, with numbers), a brief example sketch, and the pitfalls that sink candidates.

## Basic

### 1. Walk me through an LLM feature you shipped end to end.

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you've actually owned an AI feature through the full lifecycle - problem framing, design choices, evals, launch, and iteration - or just touched one layer. This is the anchor question; your answer here seeds every follow-up in the loop.

**Strong answer structure:** one sentence of business context → the user problem → your design choices *and the alternatives you rejected* → how you evaluated it pre-launch → launch mechanics (rollout, guardrails) → post-launch results with numbers → one thing you'd do differently. Two to three minutes, then let them steer.

**Example sketch:** "Support team drowning in tickets. I owned an answer-drafting assistant: RAG over our help centre and resolved tickets. Key decisions: retrieval with a reranker instead of fine-tuning because content changed weekly; drafts routed through human agents rather than direct-to-customer to bound the blast radius. Built a 300-case eval from real tickets graded on faithfulness and resolution-fit before launch. Rolled out to 10% of agents behind a flag. Result: ~35% faster handle time, draft acceptance climbed from 58% to 74% over six weeks as we mined rejections into eval cases. I'd invest in structured logging from day one next time - our first two weeks of debugging were archaeology."

**Pitfalls:** describing only the happy path; no numbers; narrating the team's work in first person singular and then failing depth probes ("what was your chunking strategy?" - silence); leading with the framework you used instead of the decisions you made; going ten minutes without pausing.

**Follow-ups:** What was the hardest technical decision and what did you almost do instead? What broke after launch? If you rebuilt it today, what changes with current models?

</details>

### 2. How do you keep up with the field without it consuming your life?

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you have a sustainable *system* versus either total firehose immersion (burnout risk, no depth) or having quietly stopped learning in 2023. In a field that reinvents itself every six months, this is a genuine job-competency question.

**Strong answer structure:** describe a concrete weekly routine with named sources, then - critically - how new information reaches your *hands*, not just your eyes. Filtering criteria matter more than volume: what you deliberately ignore is as much signal as what you read.

**Example sketch:** "I timebox ~3 hours a week. One curated source for breadth - Simon Willison's blog and one newsletter. One thing read deeply - a paper or model card, not skimmed. Release notes for the providers we actually use, because a deprecation notice is more job-relevant than most papers. And the part that matters: when something looks significant, I run it against a personal eval set I maintain from side projects. When the last big model dropped, I had it benchmarked on my own tasks within two days - that's how I found its structured-output regression before it hit our roadmap discussions. I deliberately skip launch-day hot takes and anything I can't connect to something I'd build."

**Pitfalls:** "I read Twitter/X a lot" with no synthesis step; listing twelve newsletters (nobody reads twelve newsletters); pretending to have read papers you can't discuss - interviewers will pull the thread; the opposite failure of dismissing all new developments as hype, which reads as calcified.

**Follow-ups:** What's the most recent development that changed how you build? Tell me about something hyped that you evaluated and rejected - why?

</details>

### 3. Explain a complex AI concept to me as if I were a non-technical stakeholder. Pick one you've actually had to explain at work.

<details><summary><b>Answer</b></summary>

**What they're probing:** communication under constraint - can you compress without lying? AI engineers spend enormous time setting executive and PM expectations; someone who can only communicate in jargon becomes a bottleneck no matter how strong technically.

**Strong answer structure:** name the real situation and the stake ("the VP wanted to know why the chatbot 'lies'"), give the actual explanation you used - in genuinely plain language, with an analogy that preserves the mechanism - then close with what the stakeholder *did differently* because they understood. The behaviour change is the proof the explanation worked.

**Example sketch:** "Our GM wanted to know why we couldn't just 'fix' hallucinations. I said: the model is an extremely well-read colleague answering from memory, always fluently, never checking a source unless we force it to. It doesn't have a 'lying' switch - confidence and correctness are separate dials. So our fix isn't 'patch the bug,' it's 'make it cite sources and measure how often the citations actually support the answer.' That reframing got us budget for the eval pipeline instead of a demand for a hotfix, and the GM started asking 'what's our faithfulness number' in reviews - which was the real win."

**Pitfalls:** choosing a trivially easy concept (tokens) to dodge the challenge; an analogy so loose it's wrong ("it's basically autocomplete" - then why does it write working code?); condescension; explaining for five minutes without checking whether the audience is following - do the same in the interview: pause and ask.

**Follow-ups:** How would you explain to that same stakeholder why the model aced the demo but failed in production? Explain RAG vs fine-tuning to a CFO deciding budget.

</details>

### 4. Tell me about the AI project you're most proud of. Why that one?

<details><summary><b>Answer</b></summary>

**What they're probing:** what you consider excellent work - your taste. The choice of project reveals values: do you prize technical difficulty, user impact, craft, or scale? There's no wrong value, but "proud because it was hard" with no outcome is a weak signal, and taste is heavily weighted at senior levels.

**Strong answer structure:** pick the project with the best *arc* - genuine difficulty, a decision that was yours, a measured outcome - rather than the biggest brand name. State upfront why you're proud ("proud because we were told it was impossible at that latency" / "because the eval methodology outlived the feature"), then compress the story: constraint, your key decision, result, legacy.

**Example sketch:** "A document-extraction pipeline, and I'm proud of it precisely because it was unglamorous. Legal team, 80k contracts, needed clause extraction at >95% precision or the whole thing was a liability. Everyone wanted to demo agents; I built a boring pipeline - schema-validated extraction, confidence-based routing to human review, an eval set lawyers signed off on. Hit 97% precision on the eval, processed the backlog in three weeks, and the human-review routing meant the 3% failure mode had a safety net rather than a lawsuit. Two years later the eval set is still their regression suite. I'm proud that I chose reliability over spectacle and it compounded."

**Pitfalls:** picking your most famous project when your ownership was thin - depth probes expose it immediately; pride with no measured outcome; humility theater ("well, the team really did everything"); trashing the alternative approaches colleagues wanted, which turns a taste question into a collaboration red flag.

**Follow-ups:** What was your specific contribution versus the team's? What's the weakest part of that project in hindsight? What did reviewers/users criticise?

</details>

### 5. Why do you want to work on AI systems - and why here specifically?

<details><summary><b>Answer</b></summary>

**What they're probing:** motivation durability and homework. AI teams are flooded with candidates chasing the hot field; interviewers filter for people who'll still be engaged when the work is data cleaning and eval triage, not magic. The "why here" half checks whether you understand what *this* company actually does with AI versus its press releases.

**Strong answer structure:** ground the "why AI" in something you've *done*, not something you've felt - a specific moment the technology surprised you into commitment, plus honesty about the unglamorous parts you've experienced and stayed for. For "why here": name something concrete - their product's actual AI surface, a technical blog post, an engineering decision they made publicly - and connect it to what you want to get better at.

**Example sketch:** "I moved into AI work after a weekend prototype - an extraction script - did in two hours what my team had scoped as a quarter of NLP work. That ratio broke my model of what software could do, and three years in, the thing that keeps me is the evaluation problem: we've never had software this capable that's this hard to *verify*, and I like living in that gap. Why here: your engineering blog post on how you eval prompt changes before rollout told me quality is an engineering discipline here, not a vibes process - that's the kind of team I do my best work on. And I've used the product; the latency on your assistant feature suggests interesting serving problems I want in on."

**Pitfalls:** "AI is the future" (says nothing); pure mission-statement recitation back at them; visible ignorance of the company's actual product; motivation framed entirely around personal brand ("I want to be where the action is") - teams read that as flight risk when the hype migrates.

**Follow-ups:** What part of AI work do you find tedious, and how do you handle it? Where do you want to be technically in three years?

</details>

### 6. Tell me about a time you had to learn a new AI technology or technique quickly to deliver something.

<details><summary><b>Answer</b></summary>

**What they're probing:** your learning *process* under deadline - the meta-skill this field runs on. Frameworks and model APIs churn constantly; they're hiring your ability to go from zero to shipping-quality judgment in days, and they want to see the mechanism, not just the outcome.

**Strong answer structure:** the trigger and the deadline → your learning strategy, specifically (what you read first, what you built first, who you asked, what you deliberately skipped) → how you validated your new understanding was correct rather than plausible → shipped result → what stuck with you afterward.

**Example sketch:** "Two weeks to add tool calling to our assistant; I'd only done plain completions. Day one: read the provider's official docs end to end and built the smallest possible loop - one tool, no framework - because I learn structure by building the primitive, not by adopting an abstraction that hides it. Day two: broke it on purpose - malformed arguments, parallel calls, a tool that throws - so I'd met the failure modes before production did. Then wrote ten eval cases for tool-selection accuracy before writing the real integration, because I didn't trust my own judgment of 'working' yet. Shipped in nine days. The skipped part was any agent framework - right call in hindsight; when we hit a parsing bug in week three I could see straight down to the API layer."

**Pitfalls:** "I watched some tutorials and figured it out" (no process = luck); learning stories where nothing shipped; claiming mastery of something in a weekend - interviewers test the claim immediately; not mentioning how you verified correctness, which in AI work is the entire trick.

**Follow-ups:** What do you decide *not* to learn? How do you tell genuinely new techniques from renamed old ones?

</details>

### 7. I ask you about something at the edge of your resume - say the internals of an optimizer you've never implemented. You don't know. What do you actually say?

<details><summary><b>Answer</b></summary>

I say I don't know, then I show the shape of what I do know and how I'd close the gap. Something like: "I haven't implemented Adam from scratch. I know it keeps running estimates of the first and second moments of the gradient and scales the step per parameter, and I know the practical consequences: it's forgiving on learning rate, and weight decay interacts with it badly enough that AdamW exists. Past that I'd be guessing." Three sentences, and they do three things: draw a clear boundary, prove the boundary is real rather than total ignorance, and hand you a follow-up.

What kills candidates is the middle path - hedging, generating plausible filler, watching your face to see whether it landed. Domain interviewers probe until you break by design, so the break is the point of the exercise, not an accident. A calibrated "I don't know" is a positive signal, because the job is full of moments where guessing costs money.

Two failure modes on the other side. Don't over-apologise or spiral; one clean sentence, then move on. And never say "I don't know" about something on your own resume. If my bullet claims I owned the retrieval layer, "I'm not sure how the reranker was configured" is a much worse answer than not knowing Adam, because it reads as claiming someone else's work. I make sure I can go three questions deep on every bullet I wrote.

When I have partial ground, I say what closing the gap would take: "I'd read the paper and reproduce it on a small run, probably an afternoon." That's not deflection if it's specific and time-boxed. Also fine: ask for a hint and reason out loud from first principles. Being wrong out loud and then correcting yourself when nudged tests better than silence, because it shows me updating rather than performing.

**Follow-ups:** What's on your resume right now that you'd be least comfortable being drilled on? Have you ever caught a candidate bluffing while interviewing them, and what gave it away?

</details>

### 8. We send you a take-home: build a RAG service over this corpus, we say roughly six hours. What do you do before writing any code?

<details><summary><b>Answer</b></summary>

I send an email, then I timebox. The email asks three things: what does done mean to you (working prototype or production-shaped), is there a written rubric, and can I use a hosted API and coding assistants. Asking is not a demerit. It's the first observable signal you get from me, and it mirrors how I'd start a real ticket.

Then I timebox to the stated hours plus about 25%, split roughly 50% core path, 25% evals and error analysis, 25% README and cleanup. The one thing I won't do is spend six hours on features and zero on evaluation. A small ingestion-plus-retrieval-plus-answer path with 15 hand-written test cases and a pass/fail script beats a sprawling multi-agent thing with no way to tell whether it works. Graders spend ~15 minutes; a crash in minute one means nothing else I did counts. Working and boring wins.

Every scope cut goes in the README explicitly: "sync calls only, no streaming; fixed-size chunking with overlap because the corpus is uniform prose; with another week I'd add a reranker, but I'd measure recall@k first." Naming the shortcut reads senior. Hiding it reads junior, because you'll find it anyway.

On negotiating: if the ask is realistically 20 hours unpaid, I say so and counter. "I can't commit 20 hours, but here's a repo of mine that demonstrates the same skills and I'll walk through it live, or I'm happy to do a paid trial." Reasonable companies take that. The ones that don't have told me something useful. I'd also decline a take-home that looks suspiciously like their actual roadmap, or one issued before any human has spoken to me.

And I write it assuming a defence round, because there almost always is one. Use whatever tools you like, but if you can't justify a design choice in a 45 to 90 minute walkthrough, you didn't make it.

**Follow-ups:** What would you cut first if you hit hour four and only had the ingestion path working? How would you decide whether a take-home is a reasonable ask or free consulting?

</details>

### 9. You've been a backend engineer for six years. Why AI engineering now, and what actually transfers?

<details><summary><b>Answer</b></summary>

Most of this job is still software engineering, which is exactly why I'm credible for it. Practitioners commonly put it at roughly 80% ordinary engineering - APIs, queues, retries, latency budgets, data plumbing - and ~20% model-specific work. I'm not switching careers, I'm adding a layer to one I already have.

What transfers concretely: async Python and concurrency, because LLM calls are slow network calls, and batching, streaming and backpressure decide your p95. Error handling against unreliable dependencies, because a model returning malformed JSON is just a flaky upstream with better PR. Observability, cost accounting, schema design, and the instinct to ask what happens when this thing fails at 3am.

What doesn't transfer, and I'd rather name it than pretend: comfort with non-determinism. Backend engineering trains you on same input, same output, assert equals. LLM systems break that contract, and you cannot unit test your way out. You need eval sets, sampled scoring, and statistical thinking about regressions. That was the real adjustment for me. I made it by building an extraction pipeline where I wrote the eval harness before the feature, and it changed how I think about "done."

On motivation, honestly: the reliability problem moved. What I liked about distributed systems was turning unreliable components into a product people trust. That's precisely the AI engineering problem, one layer up.

I'm also careful about what I don't claim. I haven't pretrained anything. I've run LoRA on a small open model specifically to learn where fine-tuning does and doesn't beat prompting on a narrow task, and on mine it lost to a well-prompted frontier model on quality per dollar. That was the useful result. If this role needs someone who can debug a multi-node training run, I'm not that person yet, and you should hire the person who is.

The version of this answer that fails is "AI is the future and I'm excited to learn." Everyone says it. Bring the artifact instead.

**Follow-ups:** What's the first thing that surprised you when you moved from deterministic services to LLM-backed ones? Which parts of classical ML, if any, have you found you actually needed?

</details>

### 10. What questions do you have for us?

<details><summary><b>Answer</b></summary>

I ask things that are diagnostic for me and happen to reveal what I care about. The one I always lead with: "How do you know a prompt or model change is safe to ship? Walk me through the last one." The walkthrough matters far more than the policy. A real story with an eval set, a threshold and a named person who made the call means a functioning team. "We test it and eyeball the output" means I'd spend my first year firefighting vibes-driven regressions, and I want to know that before I sign, not after.

Then, in rough priority:

- Data access: "What data can the team actually use for evals and training, and how long does access take?" Months-long approval quietly kills AI teams and nobody advertises it in the JD.
- Compute and API budget: "Do experiments queue behind production? Who says no to a spend, and how often?"
- Path to production: "Who can change a prompt, and what gates it?" A team where prompts ship unreviewed and a team where they ride a release train are different jobs with the same title.
- On-call: "Are AI features paged? Who debugs a quality regression, and how would they get paged for one at all?" Most orgs have no answer, which is itself the answer.
- Model strategy: "What happened during your last model migration or deprecation?" Tells me how coupled you are to one vendor and what debt I'd inherit.
- For a startup: runway, who the design partners are, and what the last pivot was.

Two rules I hold myself to. Don't ask what a careful read of the JD and the engineering blog answers - that reads as lazy. And don't ask only about perks; both "no questions" and "only comp questions" get logged in the debrief as low ownership. If I'm close to an offer I'll also ask what would make you not hire me, and then actually listen instead of rebutting.

**Follow-ups:** Which of those answers would be a dealbreaker for you? What's the best question a candidate has ever asked you?

</details>

## Intermediate

### 11. You shipped an LLM feature - how did you evaluate it? Walk me through the actual eval setup.

<details><summary><b>Answer</b></summary>

**What they're probing:** eval maturity - the single strongest seniority signal in AI engineering interviews. They want mechanics: dataset origin, grading method, size, where it ran, and how it connected to ship decisions. Hand-waving here contradicts any impressive claims from question one.

**Strong answer structure:** how you defined "good" for the feature → dataset construction (source, size, how it grew) → grading taxonomy (code-graded checks where possible, LLM-as-judge where necessary, humans to calibrate the judge) → where it lived operationally (CI? pre-deploy gate?) → how production failures flowed back in → a decision the eval actually changed.

**Example sketch:** "For the support drafter, 'good' decomposed into faithfulness to retrieved docs, resolution-fit, and tone. Started with 60 cases hand-labelled from real tickets - deliberately overweighted past escalations. Faithfulness ran as an LLM judge with claim-level checks; we calibrated it against 100 human labels and found ~92% agreement, with a known blind spot on partial answers, so those routed to human review. Format and PII checks were pure code assertions - free and deterministic. The suite gated deploys: any prompt or model change ran all ~400 cases (it grew weekly from mined thumbs-down events) in CI, about $4 a run. It earned its keep the day it blocked a model upgrade everyone wanted - new model was better on tone, but faithfulness dropped 6 points. We fixed the prompt regression first, then upgraded."

**Pitfalls:** "we eyeballed outputs and they looked good"; quoting only public benchmarks (MMLU says nothing about your feature); an LLM judge with no human calibration story; an eval that existed but never gated anything - a dashboard, not a discipline; not knowing the eval's cost or run cadence.

**Follow-ups:** How did you know your judge was trustworthy? What did the eval miss that production found? How big before diffs were statistically meaningful?

</details>

### 12. Tell me about a time an AI feature failed in production. What happened and what did you change?

<details><summary><b>Answer</b></summary>

**What they're probing:** operational scar tissue and honesty. Everyone who has shipped LLM features has failures; a candidate without a failure story either hasn't shipped or won't own mistakes. They're listening for detection, diagnosis in a non-deterministic system, and whether the fix was systemic or a patch.

**Strong answer structure:** the failure, concretely and unflinchingly (what users saw, blast radius) → how you *detected* it (found it yourselves, or did users?) → the debugging path → root cause → immediate mitigation vs. systemic fix → what permanently changed in your process.

**Example sketch:** "Our RAG assistant started confidently answering questions about a product feature that didn't exist. Detection was the embarrassing part: a customer tweeted it - our monitoring tracked latency and errors, not truthfulness. Diagnosis: a marketing page describing an upcoming feature in present tense had entered the index; retrieval was working *perfectly*, faithfully grounding answers in wrong source material. Immediate fix: purged the page, added a content-freshness filter to ingestion. Systemic fixes: a faithfulness sampler on production traffic with alerting, an ingestion review gate for aspirational content, and - the real lesson - we started monitoring *quality* signals, not just infra signals. Also added the incident to the eval set; it's now a permanent regression test."

**Pitfalls:** "the model hallucinated" as the terminal explanation - blaming the model signals you stopped debugging at the API boundary; a story where users found every problem; no systemic change ("we fixed the prompt" - then what prevents recurrence?); choosing a fake-humble failure with no real stakes; throwing teammates under the bus.

**Follow-ups:** How long from failure to detection, and what would have shortened it? What monitoring do you now consider mandatory for LLM features?

</details>

### 13. How do you decide between building in-house, buying a vendor product, and calling a model API?

<details><summary><b>Answer</b></summary>

**What they're probing:** engineering judgment and business sense - whether you make this call with a framework or by resume-driven development. It's also a seniority test: juniors default to building; seniors ask what's differentiating.

**Strong answer structure:** state your framework, then immediately ground it in a real decision you made - including one where you decided *against* building. Framework dimensions worth naming: is this capability core to our differentiation; do we have the data advantage to beat the vendor; total cost of ownership including evals and maintenance, not just build time; switching costs and vendor risk; time-to-signal.

**Example sketch:** "My default: API for intelligence, build the layers that touch our data and users, buy only where a vendor's whole business is the problem. Concretely: for our doc-processing product, we called frontier APIs for the extraction itself - no data moat that justified training. We *built* the eval harness, retrieval, and orchestration, because those encode our domain and are the durable asset. We evaluated buying a RAG-in-a-box vendor and declined after a two-week bake-off: it demoed beautifully but we couldn't inspect retrieval failures, and being unable to debug your core loop is an unacceptable operational position. One reversal: we initially built our own observability, then migrated to a vendor once the market matured - maintaining it was costing a day a week and differentiated nothing."

**Pitfalls:** ideology in either direction ("never trust vendors" / "never build"); ignoring maintenance in build costs - the build estimate that omits evals, on-call, and upgrades is off by 3x; no story where you killed your own preference; forgetting switching costs and what happens when the vendor deprecates, pivots, or gets acquired.

**Follow-ups:** When would fine-tuning your own model beat a frontier API? Tell me about a build/buy call you got wrong.

</details>

### 14. How do you debug non-deterministic bugs in LLM systems?

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you've developed a real methodology for the defining operational annoyance of LLM systems - bugs that reproduce 7% of the time - or you just rerun things and hope. Strong answers convert non-determinism from mystery into statistics.

**Strong answer structure:** first, separate the determinism layers: true randomness (sampling temperature), infrastructure non-determinism (batching effects, provider-side model updates, floating-point non-associativity even at temperature 0), and *input* variance masquerading as randomness (retrieval returning different chunks, context assembled in different orders). Then your toolkit: capture-everything logging so any production request can be replayed exactly; pinning what's pinnable (seeds where supported, model snapshot versions, temperature 0 for diagnosis); and treating flaky behaviour statistically - run the failing case N times, measure a failure *rate*, and test whether candidate fixes move that rate significantly.

**Example sketch:** "A tool-calling agent intermittently skipped a required lookup step - roughly 1 in 15 runs. Step one was making it reproducible-ish: we logged full request payloads, so I replayed the exact context 50 times and got an 8% skip rate - now it's a measurable quantity, not a ghost. Diffing skip vs. success traces showed the failures correlated with a specific tool result landing near the context's end. Hypothesis: instruction dilution with long contexts. Fix candidates were each run 100 times against the replay: moving the instruction into the tool description cut skips to under 1%. Shipped that, added the scenario to evals with a 2%-failure-rate alarm threshold."

**Pitfalls:** "set temperature to 0" as the complete answer - it doesn't eliminate provider-side variance and isn't a fix, it's a diagnostic; no logging story, meaning nothing is replayable and every bug is unfalsifiable; single-run conclusions ("I changed the prompt and it worked once"); not knowing that providers update models behind stable API names.

**Follow-ups:** How do you write regression tests for behaviour that's correct 95% of the time? A bug appears in production but never replays locally - what's different?

</details>

### 15. Tell me about a time you significantly cut inference costs. What was the approach and the tradeoff?

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you treat cost as an engineering dimension with measurement and tradeoffs, or discovered it when finance escalated. LLM features are often margin-negative as first shipped; the ability to fix that without quality collapse is directly bankable, and they want proof you verified quality *didn't* collapse.

**Strong answer structure:** the baseline (cost per request/user/month - knowing these numbers cold is half the signal) → where the money actually went, from measurement not guessing → interventions in order of effort-to-impact → quality verification via evals → final numbers and what you traded away.

**Example sketch:** "Our assistant ran ~$0.11 per conversation; at growth projections that was untenable. Token accounting first: 70% of spend was input tokens, and most of that was re-sending a bloated system prompt plus full history every turn. Cheap wins first: prompt caching on the static prefix and trimming a 3k-token prompt to 1.1k - that alone cut ~40% with zero quality change on our 400-case eval. Then routing: a lightweight classifier sent the ~60% of queries that were simple lookups to a model roughly 10x cheaper, keeping the frontier model for multi-step reasoning. The router's misroutes cost us about 2 points on eval scores for complex queries initially; tightening the routing threshold traded some savings back for quality. Landed at ~$0.03 per conversation - a 70%+ reduction - with eval scores within a point of baseline. The eval suite is what made this safe; without it every optimisation is a gamble."

**Pitfalls:** no baseline numbers ("it was expensive... we made it cheaper"); optimising without a quality gate - "we switched to a cheaper model" without evals is the story of a silent regression; jumping to exotic fixes (fine-tuning, self-hosting) before free ones (caching, prompt hygiene); not knowing the input/output token cost asymmetry.

**Follow-ups:** At what scale does self-hosting beat API pricing? What would you try next for another 50%?

</details>

### 16. Tell me about a time a prompt change broke production.

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you've internalised that prompts are code - versioned, reviewed, tested, and rolled back like code - and they're checking for the war story that usually teaches this. Almost everyone learns it the hard way; the question is what process existed after.

**Strong answer structure:** the change and why it looked safe → what broke, including why it wasn't caught immediately (prompt regressions are often silent - no errors, no latency spike, just quality quietly cratering on some slice) → detection and rollback → the process that now exists: prompts in version control, eval suite as a merge gate, staged rollout, monitoring on quality signals.

**Example sketch:** "Someone added a well-intentioned instruction - 'be concise' - to fix verbose answers. It worked; answers got shorter. It also broke our downstream JSON parser about 4% of the time, because conciseness made the model occasionally drop optional fields, and it degraded multi-step answers where length *was* correctness. No exceptions, no alerts - we found it three days later via a support ticket spike. Rollback was instant because prompts lived in git behind a config flag; that part we'd done right. What we hadn't: the eval suite ran nightly, not on merge, and had thin coverage of structured-output cases. Afterward: evals became a required CI gate on any prompt diff, we added schema-validation assertions for every structured output, and prompt changes ship canary-first at 5% with a quality-metric comparison before full rollout. The cultural fix mattered most - prompt edits stopped being 'just copy changes' anyone could hotfix."

**Pitfalls:** revealing prompts live outside version control (or worse, edited live in a dashboard) with no embarrassment about it; "we test prompts manually before shipping" as the whole safety story; not grasping *why* prompt regressions evade normal monitoring; a story with no process change at the end.

**Follow-ups:** How do you handle a prompt that must change for a model upgrade and behaves differently on both? Who's allowed to change prompts on your team, and what gates it?

</details>

### 17. Tell me about a time your eval metrics and real user feedback disagreed. Which did you trust?

<details><summary><b>Answer</b></summary>

**What they're probing:** epistemic sophistication about measurement - do you understand that evals are a *proxy* for user value, and what you do when the proxy diverges? Weak candidates pick a side on principle; strong ones treat the disagreement itself as the most informative signal available.

**Strong answer structure:** the divergence, concretely (eval said X, users said not-X) → your investigative move: read the actual transcripts behind the user complaints and diff them against eval coverage → root cause, usually one of: eval distribution drifted from real usage, the rubric measures the wrong thing, or feedback is a biased sample → the reconciliation → what changed in how you build evals.

**Example sketch:** "Eval scores on our code-assistant were climbing for three straight releases; simultaneously, session abandonment rose and NPS verbatims turned negative. Reading 50 abandoned sessions answered it: users had shifted toward a new framework version our eval set barely covered - we were acing a test from six months ago. The evals weren't wrong, they were *stale*: right answers to yesterday's distribution. Also found a rubric gap - our judge rewarded thorough answers, users wanted fast minimal diffs; we were optimising for the judge's taste, not the user's. Fixes: monthly eval refresh sampled from current production traffic, a 'staleness' check comparing eval-set topic distribution to live traffic, and a rubric revision grounded in what accepted-vs-abandoned sessions actually looked like. The meta-lesson I carry: eval scores going up is not the same as the product getting better, and the divergence between them is a metric worth monitoring in itself."

**Pitfalls:** "users are noisy, we trusted the evals" (or the mirror image) without investigating - both dodge the actual work; not mentioning reading real transcripts, which is always the answer; treating thumbs-up/down rates as unbiased truth (response bias is severe); no durable process change.

**Follow-ups:** How do you keep an eval set aligned with drifting production traffic? What user signals do you weight most, given how biased explicit feedback is?

</details>

### 18. How do you decide when an AI prototype is ready for production?

<details><summary><b>Answer</b></summary>

**What they're probing:** judgment about the prototype-production gap, which is wider for LLM features than any other software - the demo works on five examples, production means the 99th percentile of adversarial, ambiguous, out-of-distribution traffic. They want criteria, not vibes, and evidence you've operationalised this decision before.

**Strong answer structure:** name your readiness checklist and be specific: (1) eval performance on a set that resembles *production* traffic, including adversarial and edge cases, with a threshold agreed before testing; (2) failure-mode inventory - you know the top ways it breaks and each has a mitigation or an accepted-risk signoff; (3) blast-radius bounding - human-in-the-loop, confidence routing, or constrained output space matching failure severity; (4) operational readiness - logging, quality monitoring, rollback path, cost model at projected scale; (5) a staged rollout plan. Then a story of applying it, ideally one where you said "not yet" to pressure.

**Example sketch:** "My rule: a prototype earns production when we can state its failure rate, name its failure modes, and afford both. Our contract-analysis demo wowed leadership on ten cherry-picked documents; pressure was immediate. I built a 200-document eval from a real workload sample - accuracy was 71%, versus the ~95% the workflow needed. Instead of shipping and hoping, we shipped *shaped*: high-confidence extractions flowed straight through, low-confidence routed to human review - production-ready at 71% because the architecture absorbed the error rate. Full automation waited two more months of iteration until evals cleared the bar. The reframe I push: 'ready for production' isn't a model-quality threshold, it's a systems property - quality times blast-radius design."

**Pitfalls:** "when the demo works well" - instant disqualification; a quality bar with no number attached; no mention of monitoring or rollback (readiness is operational, not just statistical); not knowing that acceptable failure rate depends on failure *cost* - 90% is production-ready for draft suggestions and disqualifying for financial actions.

**Follow-ups:** What's the minimum viable eval before any launch? How does the bar change between an internal tool and a customer-facing feature?

</details>

### 19. We're going to walk through your take-home. Start by telling me the biggest weakness in what you submitted.

<details><summary><b>Answer</b></summary>

The real one, not a humble-brag. For the RAG service I sent: the weakness is chunking. I used fixed ~800-token windows with overlap, and my own eval set shows it fails on the tables in the corpus - the boundary splits a row from its header, and the model then answers confidently from half a table. That's 6 of my 40 cases and every one fails the same way. It's in the README under known failures rather than quietly hoping you wouldn't run those rows.

Then what I'd do about it, ranked. Route table-shaped pages to a different extractor and keep prose chunking for everything else: about half a day, closes most of the gap. Second, a reranker over a wider candidate set. But I'd measure recall@k before spending on that, because it's entirely possible my retriever never returns the right chunk at all, in which case reranking is polish on a broken step.

I open here deliberately, because the defence round scores judgment, not code. You've already read the code. What the diff can't tell you is whether I know where the bodies are buried. A candidate who says "honestly, nothing major" has just told you they did no error analysis, which is worse than any specific flaw they could have named.

I'd also separate the deliberate cuts from the ignorance, so they don't get scored as the same thing: sync calls, no streaming, no cache, single process. All defensible at the stated scale, all wrong for production, all listed in the README with the reason.

And the part I'm actually pleased with: the eval harness. Forty hand-written cases, a pass/fail script that runs in under a minute, and a failure clustering that took me longer than the retrieval code did. That's where I chose to spend the budget, and given the same six hours I'd spend it the same way.

**Follow-ups:** If I gave you one more day, would you fix the chunking or widen the eval set? Why? Which of your 40 cases would you drop as not actually testing anything?

</details>

### 20. In this round you can use a coding agent, and we'll be watching how you use it. How do you approach that?

<details><summary><b>Answer</b></summary>

The way I'd use it at work: I direct it, I verify it, and I say out loud which parts I'm choosing not to delegate. The round isn't scoring typing speed, it's scoring whether I stay in command of code I didn't write.

In a two-hour build, I spend the first ten minutes without the agent, writing down the data model, the interfaces, and what working means, ideally as two or three concrete test cases. Those are the decisions, and they're mine. Then I hand the agent the work with one correct answer: the client wrapper, CLI parsing, the schema models, the Dockerfile. I read every line back. What I write myself is anything where a plausible-looking wrong answer is expensive - the retry and error path around the model call, parsing of untrusted output, anything touching concurrency.

The failure mode in a timed round is accepting a 200-line file you never read, then losing thirty minutes to a bug you can't locate because you have no model of the code. Agents are extremely good at code that looks right. So I keep the loop tight: small diffs, run after each one, never let it get more than one step ahead of my understanding. If I can't explain a file, I delete it and do it myself, which is faster than it sounds.

I narrate the moments I reject its output, because that's the actual signal. "It's pulling in a framework for a three-function problem, I'll write this by hand" tells you more about me than the finished demo does.

Two practical things. I ask the recruiter beforehand which rules apply, since companies differ sharply on this and some formats now explicitly encourage agent use. And I cut scope out loud rather than silently missing the deadline: "I'm skipping auth and the UI, they're not what this problem is about" is a scoping decision I want on the record. Running out of time on a half-built login page isn't.

**Follow-ups:** Tell me about a time an agent's output looked right and wasn't. How did you catch it? Where do you draw the line on what you'd never delegate to an agent in production code?

</details>

### 21. Tell me about an AI project that failed. Not one with a redemption arc - one that got killed.

<details><summary><b>Answer</b></summary>

I'll give you the real one, and I'd want you to judge the decision quality rather than the outcome. The structure that matters: what we believed, what turned out to be true, when we could have known, and what finding out cost.

We built an LLM feature to auto-triage inbound support tickets into ~30 categories and route them. It demoed beautifully and it was killed at about four months. The reason wasn't the model. It was that the taxonomy was fiction. Agents had been picking categories semi-randomly for years, so the historical labels we validated against were noise wearing a schema. Our eval reported high agreement with those historical labels, which felt like success. When we finally ran a small relabelling exercise, having two people independently label a couple of hundred tickets, they agreed with each other markedly less often than our model agreed with history. We had built a model that faithfully reproduced an inconsistent human process, and our metric was rewarding it for that.

What I own: I proposed the eval set, and I used the cheap labels because they existed and the deadline was real. The relabelling exercise was two days of work. It would have killed the project in week two instead of month four. "Where did these labels come from, and do humans agree with each other on them?" is now the first question I ask on any project with supervised-shaped ground truth, before any modelling at all.

What I'd avoid in the retelling: blaming the PM, blaming the data team, or claiming it secretly succeeded. Interviewers can hear a story that's been sanded smooth. I'd also avoid "we learned so much" as the punchline. The learning has to be one specific thing I now do differently, and ideally I can point at a later project where I did it.

The one thing I'd defend: killing it was correct and I argued for it. Sunk cost was roughly four engineer-months. A router that misroutes confidently would have cost far more, and it would have cost it forever.

**Follow-ups:** How would you have measured inter-annotator agreement before committing to the project? When is a noisy label set still good enough to build on?

</details>

### 22. You own an LLM feature in production. What does on-call actually look like for it, and tell me about a page you took.

<details><summary><b>Answer</b></summary>

The honest starting point: most AI features aren't properly on-call, and that's the interesting part of the question. Classic paging catches the feature being down. It does not catch the feature being wrong, which is the failure that actually matters. An LLM feature can degrade for hours with every SLO green: 200s, p95 fine, error rate flat, answers quietly worse.

So I run alerting in two tiers. Tier one is ordinary plumbing and it pages a human at 2am: availability, latency, error rate, provider 429s and 5xx, spend per hour against a budget ceiling. Tier two is proxy signals for quality, and it pages a business-hours rota rather than waking anyone, because the true-positive rate doesn't justify it: refusal rate, share of structured outputs failing schema validation, retrieval returning zero chunks, thumbs-down rate, fallback-to-human rate, output length distribution shifting. They're cheap to compute on live traffic and they lead the user complaints by hours or days.

The page I'd tell you about: our extraction path started failing schema validation on a rising share of calls overnight. Nothing was down. The retry loop absorbed it, so it showed up as rising latency and cost, not errors. The first thing I did was not open the prompt. I asked what changed, across three axes: provider-side model updates, our own deploys, and input mix. It was input mix. A new customer had started sending a document layout we'd never seen. The fix was a routing rule and two new eval cases, not a prompt tweak - and if I'd started at the prompt I'd have spent the night making it worse for everyone else.

The thing I want any AI on-call to have is enough logging to reproduce: a full version snapshot on every request, covering model version, prompt version, retrieval index build, and tool schema version. "It got worse" is unactionable unless you can diff what moved. Without that, you're guessing, and guessing at 2am is how prompt-tweak incidents get manufactured.

**Follow-ups:** Which quality proxy metric has given you the best signal-to-noise, and which one did you turn off? How would you page on a regression that only affects 2% of traffic?

</details>

### 23. Mid-round I tell you your answer is wrong: I think you should fine-tune here, not use retrieval. You disagree with me. What do you do?

<details><summary><b>Answer</b></summary>

I take the objection seriously first, because there's a real chance you know something about the problem I don't, and because this is often a deliberate test of whether I fold under mild authority. Both folding and digging in lose.

The sequence I run: restate your position in terms you'd accept, locate the actual point of disagreement, then ask what would settle it. "So the argument is that the knowledge is stable and the real failure is that the model doesn't know the output format, and fine-tuning teaches format more reliably than in-context examples. If that's the situation, I think you're right. My assumption was that the corpus changes weekly, which is why I reached for retrieval. Which is it?" Nine times out of ten the disagreement dissolves into an unstated assumption, and surfacing it is the skill actually being scored.

If it survives that, I say where I'd bend, where I wouldn't, and what experiment decides it. "I'd still start with retrieval, because I can ship it this week and I get citations for free. But I'd accept I'm wrong if a 200-case eval shows format errors dominate while retrieval quality is fine. That's a day of work to find out." Disagreements over AI tradeoffs are almost always empirical, and the senior move is converting an argument into a cheap measurement rather than winning it rhetorically. I'd rather be measured than persuasive.

If you're simply right, I say so immediately and specifically: "Yes, I missed that the corpus is static. That changes my answer, and here's what it changes it to." Updating on evidence is a positive signal, not a concession. Interviewers are looking for it.

What's fatal is agreeing while visibly not agreeing, then quietly continuing to design the thing I originally wanted. That reads as someone who will nod in design review and then do whatever they'd planned, which is a genuinely expensive person to hire.

**Follow-ups:** Tell me about a real disagreement where you were the one who turned out to be wrong. How do you handle it when the person disagreeing is your skip-level rather than a peer?

</details>

## Advanced

### 24. Tell me about a time you pushed back on shipping something you believed was unreliable.

<details><summary><b>Answer</b></summary>

**What they're probing:** backbone with evidence - will you hold a quality line under pressure, and can you do it *constructively*? This is also an integrity probe: they're imagining you on their team when leadership wants the AI feature out before the conference. The failure modes are caving silently and being the engineer who just says no.

**Strong answer structure:** stakes and pressure source → your specific reliability concern, *quantified* - pushback carried by data is persuasion, pushback carried by vibes is obstruction → how you made the risk legible to decision-makers (translate failure rates into business outcomes) → the alternative you offered, because pushback without a path is complaint → resolution and aftermath, including whether you were right.

**Example sketch:** "Sales wanted our AI onboarding flow live for a flagship customer's kickoff. Our evals showed 12% of a specific configuration class produced wrong setups - and that customer's use case sat squarely in the failure zone. I didn't argue 'it's not ready'; I brought the eval breakdown and translated it: 'roughly one in eight of their configs will fail silently, in their first week, and this account is a reference customer.' Then the alternative: ship on time with that config class routed to manual review - 80% of the wow, none of the silent failures. Leadership took it. The routed path caught 9 bad configs in week one, each one visible to the exec who'd wanted full automation. The follow-on effect mattered more than the launch: eval review became a standing item in ship decisions, because the pushback came with receipts."

**Pitfalls:** hero narratives where you blocked the release and everyone applauded - real resolutions involve negotiation; pushback with no data ("I had a bad feeling"); no alternative offered; a story where you were overruled and then sandbagged the launch; refusing to acknowledge the legitimate business pressure on the other side.

**Follow-ups:** What if you'd been overruled - then what? Have you ever pushed back and been wrong? How do you tell a real quality line from perfectionism?

</details>

### 25. You're asked to ship an AI feature you have safety or ethical concerns about. Walk me through what you'd do - or a time it happened.

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you have a functioning ethical process - not maximal virtue, *process*. Can you distinguish discomfort from harm, escalate through legitimate channels, propose mitigations, and know where your personal line is? Companies ask this both to filter for responsibility and because regulated deployments increasingly require exactly this muscle.

**Strong answer structure:** articulate the concern precisely - "this feature will present unverified medical-adjacent claims with high confidence to vulnerable users" is actionable; "AI ethics worries me" is not → make it concrete and measurable where possible (red-team it, produce failing examples, quantify the exposure) → raise it through the real channels: your lead, then whatever risk/safety/legal review exists, in writing → propose mitigations that preserve the business goal: guardrails, scope reduction, human review, staged rollout with monitoring → and be honest about the endgame: some resolutions are "my concern was addressed," some are "I was overruled on a judgment call I could live with," and some cross a line where escalation or leaving is the answer.

**Example sketch:** "We were building automated responses to customer disputes, and I realised the planned scope included financial-hardship cases - templated empathy plus policy citations, no human eyes. I spent a day producing concrete failures: transcripts where the model's response to someone describing genuine crisis was procedurally correct and humanly terrible. Brought those transcripts, not abstractions, to the PM and legal review. Concrete artifacts changed the conversation - we carved hardship-flagged cases out to human agents, added a distress classifier as the routing gate, and shipped the rest. I'd frame my line this way: I'll ship features that can fail, with mitigations; I won't ship features whose failure mode is harm to vulnerable people with no human backstop and no monitoring."

**Pitfalls:** performative maximalism ("I would refuse and resign") - signals you've never navigated a real one; the opposite ("not my call, I ship what's prioritised") - abdication; keeping concerns verbal and untraceable; framing everything as ethics to win product arguments, which burns the channel for real cases.

**Follow-ups:** Where exactly is your personal line? What if legal approves but you still think it's wrong? How do you distinguish a safety issue from a quality issue?

</details>

### 26. Tell me about a technical disagreement over model choice - how was it resolved?

<details><summary><b>Answer</b></summary>

**What they're probing:** how you fight - technically and interpersonally. Model selection is where AI-team disagreements concentrate (frontier vs. cheap, closed vs. open, one provider vs. another), and it's often contaminated by identity and hype. They want evidence you convert opinion-fights into measurement-fights while keeping the relationship intact.

**Strong answer structure:** the disagreement and both positions *steelmanned* - respecting the other side's case is half the evaluation → your move to shift the argument from priors to evidence: define decision criteria first (quality on your eval, latency, cost, ops burden, data-governance constraints), agree on them *before* running anything → the bake-off and its result, especially if it surprised you → resolution and relationship afterward.

**Example sketch:** "A teammate pushed hard to replace our API dependency with a self-hosted open-weights model - cost projections and data-control arguments, and they were good arguments. I believed the frontier API's quality gap on our task was worth the premium. Instead of relitigating priors weekly, we wrote down the decision criteria together first: quality within 3 points on our eval suite, p95 latency under 2s, all-in cost including engineering time, and vendor-risk exposure. One-week bake-off. Results were messier than either of us predicted: the open model matched on the high-volume simple tier and clearly lost on complex reasoning. So neither of us 'won' - we ended up routing: self-hosted for the simple 60%, API for the rest, which cut costs ~45% while holding quality. The pre-agreed criteria were the whole trick; they turned a values argument into an empirical one, and we've reused that template for every model decision since."

**Pitfalls:** stories where you were simply right and the other person came around - suspiciously frictionless and teaches nothing; disagreements resolved by seniority or exhaustion; unable to state the opposing case charitably; benchmark-brandishing (MMLU deltas) instead of task-specific evals; lingering resentment leaking through the retelling.

**Follow-ups:** How do you decide without time for a bake-off? What if the eval results were ambiguous? Tell me about a technical position you held strongly and later abandoned.

</details>

### 27. Deadline pressure: do you spend the next two weeks on eval infrastructure or the feature itself? How have you actually made this call?

<details><summary><b>Answer</b></summary>

**What they're probing:** whether your stated eval religion survives contact with a deadline. Everyone *says* evals matter; this question checks if you can articulate when they're load-bearing versus deferrable, and whether you've found the moves that make the tradeoff smaller than it looks.

**Strong answer structure:** reject the framing's severity first - the strongest candidates point out that minimal evals are cheap ("50 hand-graded cases is one afternoon, and it's the afternoon that makes the other thirteen days productive") - then give the real decision factors: failure cost of the feature, whether iteration is even possible without measurement (unmeasured prompt iteration is a random walk), reversibility of skipping, and what "minimum viable eval" means here. Then a concrete instance with the tradeoff you actually took and its consequences.

**Example sketch:** "The honest answer is that framing it as two weeks of either is usually a false binary - my floor is a day: 40-60 cases from real inputs, a pass/fail script, run on every change. I've never regretted that day; I've repeatedly regretted skipping it, because without it, week two of 'feature work' degenerates into changing prompts and squinting. Real instance: launch commitment for a summarization feature, four weeks out, zero eval infra. We spent day one building the minimal harness, then made an explicit cut: no LLM-judge calibration, no CI integration - just a script and a spreadsheet. Logged both as debt with names on it. The harness caught a regression in week three that manual spot-checking had already missed once - that alone repaid the day. Post-launch, the debt items got scheduled, and one of them (judge calibration) turned out to matter: our uncalibrated judge had been about 8 points optimistic. The principle: evals scale down gracefully - the choice is never 'infra vs. nothing,' it's picking the fidelity the decision requires."

**Pitfalls:** the pious answer ("evals always come first") - reads as never having shipped under pressure; the cowboy answer ("ship and iterate on feedback") - using customers as your eval set; not knowing that a useful eval can be built in hours; deferring evals with no record, so the debt silently becomes permanent.

**Follow-ups:** What's in your minimum-viable eval for a brand-new feature? How do you keep 'temporary' eval debt from becoming permanent?

</details>

### 28. A stakeholder wants to send sensitive customer data (PII) to a third-party model API. They say the business need justifies it. What do you do?

<details><summary><b>Answer</b></summary>

**What they're probing:** data-governance judgment under commercial pressure - increasingly a core AI-engineer competency, not a legal nicety. They want neither the engineer who YOLOs PII into an API nor the one who reflexively blocks and forces the business to route around them. The strong signal is knowing the actual technical option space.

**Strong answer structure:** first, clarify facts before positions - what data, which fields, what does the provider's data-processing agreement actually say (zero-retention options, no-training clauses, regional processing), what regulatory regime applies (GDPR, HIPAA, sector rules), what did customers consent to → then present the mitigation ladder, because this is rarely binary: field-level redaction/pseudonymisation before the API call with rehydration after, zero-retention enterprise agreements, regional endpoints, VPC or on-prem deployment of open models for the sensitive slice, or scoping the feature to non-sensitive fields → route the residual risk decision to the people authorised to accept it (legal/privacy), in writing → and a story showing you enabled the business rather than just gatekeeping.

**Example sketch:** "This exact scenario: product wanted support transcripts - names, account numbers, occasionally payment fragments - sent to an LLM API for summarization. Instead of yes or no, I mapped the options in a one-pager: (a) as-is under the provider's zero-retention enterprise terms, (b) PII-redaction layer before the call - we prototyped it in three days using a mix of regex and NER, with entity placeholders rehydrated after - or (c) self-hosted model, quality and cost penalty quantified from a quick eval. Legal reviewed; we shipped (b), and the summarization quality loss from redaction measured under 2 points on our eval because names rarely matter to summaries. Key part: privacy signed off on residual risk formally - engineers shouldn't be the ones silently accepting legal exposure, in either direction."

**Pitfalls:** "I'd just say no" (business routes around you, data flows anyway, unreviewed); "the DPA covers it" without having read what it actually covers; not knowing redaction/pseudonymisation is usually cheap and barely lossy; accepting or rejecting legal risk personally instead of escalating to the accountable function.

**Follow-ups:** How would you build the redaction layer and how do you *eval* it (what's its recall on PII, and what does a miss cost)? Does using the provider's 'no training on API data' policy fully address this? What changes if the data is health records?

</details>

### 29. Tell me about mentoring or upskilling teammates on AI. How did you approach it and what changed?

<details><summary><b>Answer</b></summary>

**What they're probing:** force multiplication - at senior levels they're hiring your effect on the team, not just your output. AI teams especially need this: most orgs are majority engineers-new-to-LLMs, and someone has to raise the floor. They also listen for whether you teach judgment (evals, failure thinking) or just tool usage.

**Strong answer structure:** the gap, specifically ("four strong backend engineers, none had shipped an LLM feature; PRs had no error handling on model calls and testing meant eyeballing three outputs") → your approach, and *why that format* - pairing on real tickets beats lectures; artifacts beat meetings → what you deliberately taught first (the strongest candidates say evals and failure modes, not prompting tricks) → measurable change in team output → what the mentee(s) now do without you, which is the true metric.

**Example sketch:** "When our platform team took over an LLM feature, I had four excellent engineers with zero AI-specific instincts - treating model calls like deterministic RPCs. Rather than a lecture series, three moves: first, a 'failure museum' - a doc of 20 real production transcripts showing hallucination, injection, format drift, each annotated with the mitigation; engineers internalise failure modes from specimens faster than from principles. Second, I paired with each engineer on one real ticket end to end, and the ticket always included writing eval cases - deliberately, because evals are the habit that generates all the other good habits. Third, a PR-review checklist for LLM-touching code: retries, timeout, token budget, output validation, eval diff. Six months later: eval coverage on every feature the team shipped, one of those engineers ran the next model migration solo, and - my favourite metric - they rejected one of *my* PRs for missing an eval case. That's the succession signal you want."

**Pitfalls:** "I gave some talks and shared links" - no evidence anything changed; teaching prompt tricks instead of engineering discipline; mentorship stories with no measurable outcome; positioning yourself as permanently indispensable, which is the opposite of the point; taking credit for a mentee's growth in a way that centres you.

**Follow-ups:** How do you mentor someone skeptical that AI work is "real engineering"? What did teaching reveal about gaps in your own understanding?

</details>

### 30. Your provider deprecates the model your product depends on, with 90 days' notice. Walk me through what you'd do - or a migration you actually ran.

<details><summary><b>Answer</b></summary>

**What they're probing:** operational maturity around a now-routine industry event. Model deprecations and forced upgrades happen on roughly annual cycles for every provider; how you handle one reveals your eval infrastructure, your coupling to vendor specifics, and whether you plan or panic. Candidates who've run one sound completely different from those who haven't.

**Strong answer structure:** immediate triage - inventory every dependency on the deprecated model (main prompts, judges inside your evals, fine-tunes, anything with hardcoded behavioural assumptions) → the migration is fundamentally an *eval problem*: your suite is the specification the replacement must meet, so its coverage gets audited first → candidate evaluation as a bake-off (successor model, competitors, open-weights) since forced migration is a free opportunity to renegotiate your model choice → expect behavioural drift even at "better" quality: format quirks, refusal-boundary changes, verbosity shifts - eval-driven prompt adaptation per candidate → staged rollout with side-by-side comparison, rollback plan until confidence, then the retrospective: what coupling made this hard, and how the next one gets cheaper.

**Example sketch:** "We got a deprecation notice mid-quarter. Day one: dependency inventory found a nasty surprise - the deprecated model wasn't just serving the product, it was the judge inside our eval pipeline, so our measuring stick was dying alongside the thing it measured. We migrated the judge first, re-calibrated it against our human-labelled set, *then* evaluated successors with it. The successor model scored higher overall but broke two things silently: it formatted lists differently (breaking a downstream parser) and refused a category of legitimate financial questions the old model answered. Both caught by evals, both fixed with prompt adjustments, one week. Canary at 10% for a week comparing quality metrics side by side, then full cutover with two weeks of overlap before the deadline. Retro output: an abstraction layer for model calls, quarterly 'migration readiness' eval runs against candidate models, and a rule that judges get versioned and calibrated like any other model dependency."

**Pitfalls:** treating it as a config change ("just bump the model string") - the answer of someone who's never done it; no eval-first framing, meaning quality verification is vibes; missing the judge/eval circularity; not seizing the bake-off opportunity; no retrospective step that reduces the cost of the next one.

**Follow-ups:** How do you keep prompts portable across providers without sinking to lowest-common-denominator capability? What would you do at 30 days' notice instead of 90?

</details>

### 31. Leadership saw a demo and now expects magic. Tell me about managing expectations for what an AI system can actually do.

<details><summary><b>Answer</b></summary>

**What they're probing:** whether you can manage the defining organisational hazard of AI work - the demo-to-production expectation gap - without becoming either the hype amplifier or the resident cynic. LLM demos are uniquely seductive: the technology's best 5% is visible in minutes while its failure distribution takes months to map. Seniors are expected to govern this gap proactively.

**Strong answer structure:** the expectation gap, concretely (what leadership believed vs. what the system reliably did) → why demos mislead - a good candidate can explain that a demo samples the happy path while production samples the full input distribution, adversarial cases included → your correction strategy: numbers and *live failure examples* beat verbal caveats; give leadership a calibrated mental model, not a wet blanket → converting deflation into a credible plan with staged milestones → the durable practice you installed so the next demo doesn't repeat the cycle.

**Example sketch:** "Our CEO saw a competitor's agent demo and asked why we couldn't automate our entire quote-generation workflow 'in a sprint.' Instead of debating feasibility in the abstract, I built a demo of my own - but rigged honestly: I ran our best prototype live on twenty *real* quote requests sampled from last month, in front of the exec team. Fourteen were excellent, four were subtly wrong in ways only a domain expert would catch, two were confidently absurd. That twenty-minute session recalibrated the room more than any slide deck could - the subtly-wrong ones did the heavy lifting, because they made the verification problem visceral. Then the pivot from no to how: here's the staged path - assistive drafts first, measured against these twenty cases grown to two hundred, autonomy expanding as eval numbers earn it. We shipped assistive mode in six weeks and hit full automation for the simple tier two quarters later, ahead of the recalibrated expectations. The practice that stuck: every AI demo to leadership now includes a 'failure reel' - it's cheap honesty insurance, and it's made leadership *better* customers of AI proposals, not more skeptical ones."

**Pitfalls:** mocking leadership's naivety - their excitement is an asset to steer, not a defect; pure deflation with no path forward (the "actually it's all hype" engineer loses the influence to steer anything); over-promising to preserve the excitement and detonating later; managing expectations once instead of installing a practice.

**Follow-ups:** How do you demo honestly without killing organisational momentum? What do you do when a competitor's (possibly staged) demo resets expectations you'd carefully calibrated?

</details>

### 32. Your assistant's answer quality regressed and nobody noticed for three weeks. You're writing the postmortem. Walk me through the document.

<details><summary><b>Answer</b></summary>

The document has to explain the three weeks, not just the regression. Detection latency is the headline finding. Any AI postmortem that leads with root cause and treats "we noticed late" as a footnote has missed the actual incident, because the cause is a one-off and the blindness is structural.

The structure I'd use:

**Timeline with versions, not just events.** What matters is what changed and when, across model version, prompt version, retrieval index build, tool schema, guardrail config, and input mix. Most quality regressions I've seen weren't a single deploy: they were slow drift, a provider-side model update, or an index rebuild that silently dropped a document type. If we don't log a version snapshot per request, the timeline is speculation, and that's finding number one before anything else.

**Impact in user and money terms.** Not "faithfulness dropped." Roughly how many users got a worse answer, how many escalated to a human, what the retries cost. If we can't quantify it, say so plainly and make quantifying it an action item rather than inventing a number.

**Root cause and, separately, why detection failed.** Two investigations, two sets of action items. The classic shape: the offline eval stayed green because it runs on a frozen curated set, and the regression lived in traffic that set doesn't represent. Real users send edge cases and adversarial phrasing; your golden set sends what you thought of six months ago.

**A reproducible test case.** Every AI incident should exit with a scripted input that fails on the bad version, passes on the good one, and joins the eval set permanently. An incident that produces no regression test will recur.

**Action items weighted toward detection.** One or two fixes for the cause, then the real work: a live proxy metric, a sampled scoring job on production traffic, a shadow canary comparing old and new. Fixing the specific cause without fixing the three weeks is theatre.

Blameless, but not mushy: the finding is that we shipped a system whose quality was unobservable. Someone chose that under deadline, and it was probably me.

**Follow-ups:** How would you sample production traffic for scoring without a labelling budget that scales with traffic? What would make you page on this rather than catch it in a weekly review?

</details>

### 33. Tell me about a time you argued to kill an AI feature that was already live.

<details><summary><b>Answer</b></summary>

A summarisation feature on a document product, live about a year. Roughly 3% of monthly actives ever touched it, well under 1% used it twice. I built the case to sunset it and shipped the removal.

How I built the argument, because "I don't like it" kills nothing:

**Usage, segmented honestly.** The headline number looked survivable until you split first use from repeat use. Something people try once and never return to is a demo, not a product, and aggregate MAU touches hide that completely.

**Total cost, not inference cost.** Inference was the small line. The real cost was the eval set we maintained, the on-call surface, the two engineers repeatedly pulled into "the AI made this up" complaints, and the fact that it was the last thing pinning us to a model we wanted to retire. That migration was worth more than the feature.

**Risk asymmetry.** It was our highest-variance surface, and the downside of a wrong summary on a contract is not symmetric with the upside of a right one.

**What we'd do instead.** Never propose a deletion without the alternative. We moved the effort into structured extraction, which had verifiable ground truth, a testable accuracy number, and users who came back.

The politics mattered more than the analysis. An exec had championed it, so I didn't open with "it's bad." I asked for a decision rule in advance: "If repeat usage is still under X at quarter end, do we agree to sunset?" Agreeing the threshold before the data lands is the whole trick. Afterwards, everyone relitigates the threshold instead of the decision.

The sunset itself: announce, keep it behind a flag for a cycle, and watch for the loud minority who genuinely depended on it. There were four accounts. We contacted them directly. Two didn't care; two got a better answer from the extraction path.

Killing your own work is a seniority signal. Most AI portfolios I've inherited needed pruning more than they needed features, and nobody gets promoted for the pruning, which is exactly why it doesn't happen.

**Follow-ups:** What if the usage had been low but the four accounts were your largest customers? How do you decide between sunsetting a feature and rebuilding it?

</details>

### 34. An AI feature you're shipping needs sign-off from legal, security, and data governance. How do you run that without it eating the quarter?

<details><summary><b>Answer</b></summary>

Go to them in week one with a specific proposal, not in week ten with a finished feature and a deadline. The failure mode is treating review as a terminal gate, which is when a two-week fix becomes a re-architecture, and it's why engineers believe legal blocks AI work. Legal doesn't block AI work. It blocks ambiguity, and it's fast on specifics.

I bring one page to the first meeting: exactly what data leaves our boundary, to whom, under what contract, retained how long, whether it trains their model, what happens if the answer is no, and what the feature does when the model is wrong. Every one of those gets asked in week ten regardless. Answering unprompted turns a six-week review into a conversation.

What each function actually cares about, in my experience:

**Legal:** data residency, the provider's processing terms and retention/training defaults, whether the output constitutes advice in a regulated domain, and IP and indemnity on generated content. The zero-retention or no-training-on-our-data posture is usually the crux, and it's usually a contract term rather than an engineering problem, which means starting it early costs nothing and starting it late costs the quarter.

**Security:** treat both the model's inputs and its outputs as untrusted. Prompt injection via retrieved documents on the way in; on the way out, whether model output ever reaches a shell, a query, or another user's context, and what the tool layer is permitted to do. Bring a threat model, not reassurance.

**Data governance:** lineage and access control. If retrieval can surface a document the requesting user can't open, you've built an exfiltration tool with a good UI. Per-user filtering enforced in the index, not requested in the prompt.

Then make one of them a named design partner rather than a reviewer. A security engineer who shaped the design in week one defends it in week ten instead of discovering it. I keep a written record of what was approved and why, because people change roles and the feature outlives the meeting.

Where I push back: if a control makes the feature useless, I say so plainly and let the business decide, rather than shipping a crippled version and blaming compliance for it.

**Follow-ups:** How would you enforce per-user access control at retrieval time without rebuilding the index per user? What's the strongest case for shipping without a control that legal asked for?

</details>

### 35. You join as a staff engineer. The team ships prompt changes on vibes, has no evals, and as far as they can tell is shipping fine. What do you do in your first 90 days?

<details><summary><b>Answer</b></summary>

I don't open by telling them evals matter. They've heard it, and a team shipping fine on vibes holds a rational prior that evals are ceremony. I'd change the prior with a demonstration, chosen to be cheap and hard to argue with.

**First ~2 weeks:** ship something small through their normal flow so I have standing, and read the logs. Not the code, the traffic. I sample a few hundred real requests and hand-label them myself against whatever quality means for this product. This is the highest-leverage thing a new senior person can do and almost nobody does it. It costs two days and produces the one artifact that moves people: a number, on their product, that they didn't have and can't dismiss.

**Weeks ~3 to 6:** turn that labelling into ~50 cases and a pass/fail script that runs in under five minutes. Not a platform, not a vendor evaluation, one file in the repo. Then wait for the next prompt change and run it. The moment that converts a team is when the script catches a regression that was about to ship, on a change everyone believed was safe. That has happened every time I've done this, because prompt edits reliably fix the case the author was staring at and break two they weren't.

**Weeks ~6 to 12:** make the right thing cheap rather than mandatory. Wire it into CI so it runs without anyone remembering. Make adding a case one line. Add a case for every incident and every customer complaint, so the eval set grows as a byproduct of work people already do. A set that requires a ritual dies within a quarter.

What I wouldn't do: propose an eval platform, demand a merge gate before there's trust, or frame any of it as process maturity. And I'd stay honest that 50 cases is not a real eval. It's the smallest thing that makes the argument. Where it goes next is the team's call, once they've felt it work.

**Follow-ups:** What if the demonstration fails and the script never catches anything? Do you conclude they were right? How do you handle the engineer who wrote the prompt the script just flagged?

</details>
