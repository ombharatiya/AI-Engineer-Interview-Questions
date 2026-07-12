# 🧠 Zhipu AI - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, technical reports, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- **Public detail on the interview loop is thin.** Zhipu AI does not publish a process skeleton, and there are few English-language candidate write-ups. The loop below is the typical shape for a research-driven Chinese LLM lab, clearly labelled as inference, anchored to their real job requirements (PhD or MS plus publications, strong Python/C++). Treat it as a map, not a contract.
- Expect a research-heavy bar: their public postings ask for a track record at KDD, ICML, NeurIPS, ICLR, or ACL, and name pre-training, alignment, instruction tuning, RLHF, and evaluation as the actual work.
- The technical centre of gravity is the **GLM lineage**: the autoregressive blank-infilling objective, the GLM-4.5 / GLM-5 MoE architecture, hybrid thinking / non-thinking reasoning, and their **ARC focus** (agentic, reasoning, coding). Know how their models actually work, not just the API surface.
- **Agents are a first-class product line**, not a side project: AutoGLM (phone GUI agent) and CogAgent (vision-language GUI agent) mean long-horizon tool use, GUI grounding, and agentic RL are fair game.
- Chinese big-tech and startup loops commonly include a written/online assessment (笔试) and several technical rounds; be ready to reason bilingually about tokenization, data, and evaluation for Chinese and English.

## Company context

Zhipu AI (智谱, internationally branded **Z.ai**) is a Beijing LLM company spun out of the Knowledge Engineering Group at Tsinghua University in 2019, founded by professors Tang Jie and Li Juanzi with Zhang Peng as CEO. It is one of China's leading foundation-model labs, known publicly for the **GLM family**: the original General Language Model objective, the open bilingual GLM-130B, ChatGLM, and the GLM-4 / GLM-4.5 / GLM-5 series, plus agent products (AutoGLM, CogAgent) and multimodal models (GLM-4V, CogVLM, CogVideoX). Several flagship models ship as open weights, so an "AI engineer" here sits close to real training and post-training runs: pre-training data and objectives, RLHF and reinforcement learning with verifiable rewards, agentic RL infrastructure, inference efficiency, and evaluation. Teams are academically minded (heavy Tsinghua ties) but ship product at scale. Note the geopolitical context: Zhipu was added to the US Entity List in January 2025, and its recent models are reported to train on domestic (Huawei Ascend) hardware.

## Roles & titles they hire

From publicly posted Zhipu AI job descriptions and category norms (labelled where inferred):

- **NLP Researcher** - pre-training, alignment, instruction tuning, RLHF, and evaluation of large language models. Public posting asks for a PhD, or an MS with 2+ years of research experience, strong Python/C++/Git, PyTorch or TensorFlow, and a publication record at KDD/ICML/NeurIPS/ICLR/ACL.
- **Multi-Modality Researcher** - vision-language and generation work (the CogVLM / CogAgent / CogVideoX lineage); at least one CV or NLP paper expected.
- **Data Engineer / Data Scientist** - pre-training and post-training data pipelines, curation, and quality; strong engineering, bachelor's-level entry.
- **Research / ML Engineer, Systems (inferred)** - distributed training, RL infrastructure (their slime framework), serving and inference optimization; typical for a lab shipping 100B+ MoE models.
- **Applied / Product and Agent Engineering (inferred)** - building on GLM APIs and the AutoGLM agent stack, plus overseas growth roles (they have reportedly been hiring to boost overseas sales out of Hong Kong and Malaysia).

Apply routes are usually the official site and email (public postings list ai.hr@zhipuai.cn). Titles and Chinese-language equivalents (算法, 大模型, 多模态) vary by team.

## The interview loop

**Public information on Zhipu's specific loop is thin, so treat this section as inference, not fact.** There is no official process page and few English candidate reports. What follows is the typical shape for a research-driven Chinese LLM lab, combined with the concrete requirements Zhipu's own postings state. Verify every stage with your recruiter.

| Stage | Format | What's evaluated |
|---|---|---|
| Resume / referral screen | Recruiter or hiring manager | Publications, open-source, model/training experience; fit to team (research vs systems vs multimodal vs agent) (inferred) |
| Online / written assessment (笔试) | Timed coding + ML questions | Algorithms in Python/C++, plus ML/DL fundamentals; common in Chinese tech loops (reported category norm, varies) |
| Technical round 1 | Live, often with a researcher | Transformer and LLM internals, your past projects deep-dive, coding (inferred) |
| Technical round 2-3 | Live | Training / post-training depth (pre-training, RLHF, RL), or systems (distributed training, inference), or multimodal / agents depending on team (inferred) |
| Research presentation | Present your own work | Depth, rigour, and whether you can defend method choices - expected for research hires given the publication bar (inferred) |
| Director / cross / values round | Senior leader + HR | Motivation, "why Zhipu", collaboration, long-horizon thinking (inferred) |

Timeline and the exact number of rounds are not publicly documented; assume it varies by team and seniority.

## What they emphasise

- **GLM-lineage fluency.** From the autoregressive blank-infilling objective through the GLM-4.5 MoE and hybrid reasoning design, they build their own architecture family. Being able to explain *why* GLM is shaped the way it is signals you have read past the model card.
- **Agentic, Reasoning, Coding (ARC).** GLM-4.5 is explicitly framed around ARC, and GLM-5 pushes agentic engineering. Expect questions on long-horizon agents, tool use, and coding-model evaluation (SWE-bench, TAU-bench style).
- **Reinforcement learning at scale.** Their post-training stack (expert training then unified training, plus the open-source slime RL framework with colocated and disaggregated modes) means RLHF, RLVR, and agentic RL are core, not trivia.
- **Bilingual by design.** GLM has been Chinese/English from GLM-130B onward. Tokenization, data balance, and evaluation across both languages are real concerns here.
- **Multimodal and GUI grounding.** CogVLM, CogAgent, and AutoGLM mean vision-language grounding and screen-operating agents are a genuine product line, not a research curiosity.
- **Efficiency and open weights.** Shipping open MoE models makes inference economics (active vs total parameters, MTP, quantization, serving) a shared obsession across the org.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. GLM's original pre-training objective is autoregressive blank infilling. How does it differ from BERT and GPT, and why did the team argue it unifies understanding and generation?

<details><summary><b>Answer</b></summary>

GLM sits deliberately between the two dominant paradigms. **BERT** is a bidirectional encoder trained with masked language modelling: it sees the whole context but predicts masked tokens independently, which is strong for understanding (NLU) but awkward for generation. **GPT** is a left-to-right autoregressive decoder: great for generation, but each token only sees the past, so it lacks BERT-style bidirectional context.

GLM's trick is to **mask out spans** (not single tokens) from the input, then **autoregressively predict each span** conditioned on the corrupted text plus previously generated tokens of that span. The unmasked context is attended to bidirectionally (like an encoder), while the tokens inside a blank are generated left-to-right (like a decoder), inside a single transformer. Two design details make it work: spans are predicted in a shuffled order (so the model learns dependencies between blanks), and **2D positional encoding** tracks both the position of a span in the original text and the position of a token within the span.

The pitch is that one objective covers the spectrum: short blanks behave like an NLU/cloze task, long blanks that stretch to the end behave like generation. By varying the span-length distribution during pre-training you can bias toward understanding or generation, so a single model handles classification, conditional generation, and unconditional generation. That "one architecture for both" argument is the historical root of the GLM name and why later chat models kept the GLM branding even as the architecture evolved toward standard decoder-style MoE.

**Follow-ups:** Why does span prediction order matter for the objective? How would you adapt the span-length distribution if you cared mostly about long-form generation?

</details>

### 2. GLM-4.5 is a Mixture-of-Experts model with 355B total but 32B active parameters. Explain the economics: what does that split buy you and what does it cost?

<details><summary><b>Answer</b></summary>

The split decouples **capacity** from **per-token compute**. GLM-4.5 stores 355B parameters across many expert FFNs, but a router selects only a small subset per token, so roughly 32B parameters actually fire on each forward pass. FLOPs and decode latency track the *active* count, so you get quality closer to a very large model at the compute cost of a mid-size dense one. GLM-4.5-Air applies the same idea at 106B total / 12B active for cheaper serving.

The catch is that the economics are asymmetric. FLOPs scale with active parameters, but **memory scales with total parameters**: you must hold all 355B weights in VRAM (or across a sharded cluster with expert parallelism), even though most sit idle per token. So MoE buys quality-per-FLOP, not quality-per-GB. That is fine for a lab serving on multi-GPU nodes and painful on a single card, which is why the Air variant and quantized/FP8 releases exist.

Two training-time costs come with it. **Load balancing:** left alone, routers collapse onto a few favourite experts, wasting capacity and unbalancing hardware; you counter this with an auxiliary balancing loss or a loss-free bias-adjustment scheme. **Systems overhead:** expert-parallel training needs all-to-all communication to ship each token to whichever device holds its expert, plus careful handling of routing instability. The interview signal is that you can separate "how big is the model" (marketing) from "how much compute per token" (what you pay) and reason about where the memory actually goes.

**Follow-ups:** Why is batched MoE inference trickier than dense (expert imbalance within a batch)? When would you recommend GLM-4.5-Air over the full model to a self-hosting customer?

</details>

### 3. Implement a top-k MoE router in PyTorch. Then contrast auxiliary-loss load balancing with a loss-free approach.

<details><summary><b>Answer</b></summary>

Core routing plus the balancing loss, isolated:

```python
import torch, torch.nn.functional as F

def moe_route(x, gate_w, experts, k=2):
    # x: (T, D); gate_w: (D, E); experts: list of callables
    logits = x @ gate_w                     # (T, E)
    topv, topi = logits.topk(k, dim=-1)     # (T, k)
    w = F.softmax(topv, dim=-1)             # normalise over the chosen k

    out = torch.zeros_like(x)
    for slot in range(k):
        for e in range(len(experts)):
            mask = topi[:, slot] == e
            if mask.any():
                out[mask] += w[mask, slot, None] * experts[e](x[mask])

    # auxiliary load-balancing loss (Switch/GShard style)
    probs = logits.softmax(-1)                       # (T, E)
    importance = probs.mean(0)                       # fraction of prob per expert
    onehot = F.one_hot(topi[:, 0], probs.size(-1)).float()
    load = onehot.mean(0)                            # fraction of tokens per expert
    aux = (importance * load).sum() * probs.size(-1)
    return out, aux
```

Points that get probed: softmax over the selected top-k (not all experts), the causal detail that routing is per token per layer, and that production code dispatches with grouped gather/scatter rather than a Python loop.

**Auxiliary-loss balancing** adds `aux` (weighted) to the training loss to push token assignment toward uniform. It works but injects gradients that are not about the language objective, so too high a weight hurts quality and too low lets experts collapse - a tuning headache. **Loss-free balancing** (the direction more recent MoEs, including the GLM/DeepSeek lineage, favour) instead keeps a per-expert **bias term added to the routing logits** and nudges that bias up for under-used experts and down for over-used ones between steps, based on observed load. Balancing then happens through a controller on the bias, not through an extra loss term, so the main objective's gradients stay clean while utilisation still evens out.

**Follow-ups:** What breaks if an expert receives zero tokens for many steps? How does capacity factor / token dropping interact with balancing?

</details>

### 4. GLM-4.5 is a "hybrid reasoning" model with a thinking mode and a direct-response mode. How do you build one model that does both, and what are the training and serving implications?

<details><summary><b>Answer</b></summary>

The goal is a single set of weights that can either emit a long chain-of-thought before answering (thinking mode, for hard reasoning, maths, and multi-step tool use) or answer immediately (non-thinking mode, for latency-sensitive chat). You do not train two models; you train one to condition its behaviour on a control signal.

**Training:** post-train on a mixture where some examples contain explicit reasoning traces wrapped in a delimiter (a think block) followed by the final answer, and others contain only the answer, each tagged so the model learns to associate the mode with a switch (a system flag or template token). Reinforcement learning then sharpens the thinking mode on verifiable tasks (maths, code, agentic trajectories) where you can reward correct final answers, while keeping the fast mode aligned for everyday chat. The hard parts are making the model actually *stop* thinking when told to, preventing reasoning traces from leaking into the final answer, and stopping the model from padding trivial questions with unnecessary thought.

**Serving:** thinking mode spends large numbers of output tokens before the user sees anything, so you expose the mode as an API parameter and budget accordingly - token cost, time-to-first-token, and max-length limits differ sharply between modes. You often cap reasoning length, and you may run the two modes behind different routing / batching policies because their token-length distributions differ. Evaluation must be mode-aware too: a benchmark that allows thinking measures a different capability than one that forbids it.

**Follow-ups:** How would you stop the model from over-thinking simple prompts? How do you evaluate whether the thinking actually helps versus inflating token spend?

</details>

### 5. Zhipu open-sourced slime, an RL framework that supports both colocated-synchronous and disaggregated-asynchronous modes. Why does long-horizon agentic RL need the disaggregated, asynchronous design?

<details><summary><b>Answer</b></summary>

RL post-training has two workloads that compete for the same GPUs: **rollout/generation** (the policy acts, producing trajectories) and **training** (gradients update the policy from those trajectories). How you place them matters.

For **reasoning RL** (single-turn maths/code with verifiable rewards), rollouts are relatively short and uniform, so a **colocated, synchronous** design is efficient: generate a batch, score it, update, repeat, with generation and training sharing the same devices in lockstep. Utilisation is high because everyone finishes at roughly the same time.

**Agentic RL** breaks that assumption. A trajectory might be dozens of tool-calling steps, with wildly variable length (one task finishes in 3 steps, another in 50), plus latency from real or simulated environments and tool execution. If training waits synchronously for the slowest rollout in the batch, GPUs sit idle behind long-tail trajectories - the classic straggler problem. A **disaggregated, asynchronous** design separates rollout workers from trainer workers: rollout engines continuously generate trajectories into a buffer, the trainer consumes them without blocking on any single episode, and the updated policy is periodically shipped back to the rollout engines. This keeps both pools busy and is what makes long-horizon agentic RL throughput tractable.

The cost is **off-policy drift**: trajectories in the buffer were generated by a slightly older policy than the one being updated, so you need staleness bounds, importance-weighting or clipping, and careful sync frequency to stay stable. The interview point is recognising that the environment's latency and length variance, not the model, dictate the training-system architecture.

**Follow-ups:** How stale can rollouts get before training destabilises, and how would you bound it? Why is reward design harder for multi-step agentic tasks than for single-answer maths?

</details>

### 6. GLM-4.5's post-training uses expert models per domain and then a unified training stage with self-distillation. Walk through why you would train specialists and then merge them.

<details><summary><b>Answer</b></summary>

The problem this solves is that reasoning, agentic tool use, and general chat pull post-training in different directions. Optimising all three jointly from the start tends to produce a model that is mediocre at each, because the data mixtures, reward signals, and RL recipes that make a great agent are not the same ones that make a great chat model, and they interfere.

**Expert training** sidesteps the interference: you take the base model and post-train separate specialist variants, each pushed hard on one domain - a reasoning specialist trained with verifiable-reward RL on maths and code, an agent specialist trained on long-horizon tool-use trajectories, a general specialist tuned for helpful, safe chat. Each can use its own best recipe without compromise.

**Unified training with self-distillation** then folds those capabilities back into one deployable model. Rather than trying to re-run all the specialist RL simultaneously (expensive and unstable), you use the specialists as *teachers*: generate high-quality outputs from each expert on its domain, then train the single unified model to match them (distillation on the model's own family, hence "self"-distillation). The unified model inherits each specialist's strengths in one set of weights, which is what you actually ship and serve.

The tradeoffs: distillation can lose a little of each specialist's peak, so you balance the data mixture to avoid one domain dominating, and you still do a final alignment/RL polish on the unified model. The signal an interviewer wants is that you understand capability interference and see distillation as a practical merge operator, not just a compression trick.

**Follow-ups:** How do you decide the mixing ratio across the three domains? What goes wrong if the agent specialist's traces dominate the distillation set?

</details>

### 7. AutoGLM and CogAgent operate real GUIs - a phone or a browser - from screenshots, over tens of steps. Design the agent: perception, action space, and error recovery for a 50-step task.

<details><summary><b>Answer</b></summary>

The core loop is perceive, decide, act, observe, repeat, and the design lives in each piece.

**Perception / grounding.** The input is a screenshot (plus optionally the accessibility tree / view hierarchy). A vision-language model like CogAgent (built on GLM-4V) has to *ground* language to pixels: given "tap the Add to cart button", output the coordinates or element id to act on. Robust grounding is the make-or-break capability - training needs GUI-specific data pairing instructions with element locations, and high enough input resolution to read small UI text, which is why these models use higher-resolution vision paths than generic VLMs.

**Action space.** Keep it small and executable: `tap(x,y)`, `swipe(dir)`, `type(text)`, `back`, `home`, `wait`, `done`. Emit as structured calls so a runtime executes them deterministically. Constrain outputs (schema/JSON) so the model cannot emit unexecutable actions.

**Planning and memory.** For a 50-step task you cannot re-plan from scratch each step. Maintain a task goal, a running history of past actions and their observed effects, and a short plan the agent updates. History matters because screens repeat (you must know you already added the item) and because recovery needs context.

**Error recovery.** The hard part. Screens are non-deterministic: pop-ups, loading spinners, ads, wrong-page landings. Design for it: after each action, verify the screen changed as expected; if not, detect the failure (unexpected screen, no state change) and try a recovery action (dismiss dialog, go back, retry) rather than blindly continuing. Add hard caps on total steps and on repeated identical actions to break loops, and a "give up and ask the user" terminal state. Gate irreversible actions (purchases, sending) behind confirmation.

**Evaluation.** Task success rate end-to-end, plus per-step grounding accuracy, on a suite of real apps - not just a single happy path.

**Follow-ups:** Why is verifying state after each action more important than a perfect plan up front? How would you collect training data for GUI grounding at scale?

</details>

### 8. GLM has been bilingual Chinese/English since GLM-130B. What changes in tokenization, data, and evaluation when a model must serve both languages well?

<details><summary><b>Answer</b></summary>

**Tokenization** is the first place monolingual assumptions break. Chinese has no whitespace word boundaries and a huge character inventory; a BPE tokenizer trained mostly on English will over-fragment Chinese (many tokens per character-dense sentence), inflating sequence length and cost and hurting quality. You train the tokenizer on a *balanced* bilingual corpus so both languages get reasonable **fertility** (tokens per word/character), and you size the vocabulary large enough to cover common Chinese characters and multi-character words without exploding the embedding table. Measure fertility per language and check that neither is badly penalised.

**Data.** You need a deliberate mixture ratio between Chinese and English (and code), because scraped web data skews heavily English. Too little Chinese and the model is weak on it; too much and you lose the strong English/coding transfer that English-heavy data provides. Chinese data also has its own quality, dedup, and safety/filtering pipeline (different sources, different noise). Cross-lingual transfer is a feature to exploit: reasoning and coding ability learned in one language partly transfers, so you do not need perfectly symmetric data for every capability.

**Evaluation.** You cannot just translate English benchmarks - that measures translation artefacts. Use native benchmarks in each language (Chinese exam-style and knowledge benchmarks alongside English ones), plus code and reasoning suites, and watch for capability gaps that appear in one language only. Safety and alignment must be evaluated per language too, since refusals and jailbreak behaviour do not transfer cleanly.

**Follow-ups:** How would you detect that your tokenizer is unfairly penalising Chinese? Why can safety alignment in English fail to hold in Chinese?

</details>

### 9. What is Multi-Token Prediction (MTP), why do models like GLM-4.5 add an MTP layer, and how does it help at inference time?

<details><summary><b>Answer</b></summary>

Standard language-model training predicts one next token per position. **Multi-Token Prediction** adds auxiliary heads (or a small extra module) that also predict the *next few* tokens from the same hidden state, so the training signal is richer: the model is pushed to plan a little further ahead than one step, which can improve representation quality and sample efficiency.

The bigger practical payoff is at **inference**, where MTP feeds naturally into **speculative decoding**. Autoregressive decode is memory-bandwidth-bound: each token requires a full forward pass reading all the weights, so latency is dominated by that per-step cost, not by the arithmetic. Speculative decoding breaks the one-token-per-pass barrier by cheaply *proposing* several future tokens and then verifying them in a single forward pass of the main model; any prefix the main model agrees with is accepted at once. An MTP head is a built-in, well-aligned proposer - it was trained jointly with the model to predict those next tokens, so its guesses are accepted more often than a generic tiny draft model, giving a speed-up with no change to the output distribution (verification guarantees the same tokens the base model would have produced).

The tradeoffs: MTP adds parameters and training complexity, the acceptance rate (and thus the speed-up) depends on how predictable the continuation is, and you carry the extra head's compute per step. Some deployments train with MTP for the quality benefit and can drop the extra heads at serving time if they do not use speculative decoding. The interview signal is connecting a training-time objective to a concrete decode-latency win, and knowing that speculative decoding is lossless.

**Follow-ups:** Why does speculative decoding not change the output distribution? When does MTP give little speed-up (low acceptance)?

</details>

### 10. For a reasoning model, describe reinforcement learning with verifiable rewards (RLVR) and how you would design the reward. How does it differ from classic RLHF?

<details><summary><b>Answer</b></summary>

**Classic RLHF** optimises a *learned* reward model trained on human preference comparisons, then uses RL (PPO-style) to push the policy toward higher predicted reward, with a KL penalty to the reference model so it does not drift or reward-hack. It is the right tool for fuzzy, subjective qualities - helpfulness, tone, safety - where there is no programmatic notion of "correct".

**RLVR** replaces the learned reward with a **verifiable, programmatic signal** for domains where correctness is checkable: maths answers matched against ground truth, code run against unit tests, agentic tasks scored by whether the environment reached the goal state. The reward is (largely) a checker, not a neural network, which removes the biggest failure mode of RLHF - reward-model hacking - because you cannot fool a unit test the way you can fool a preference model. This is a major driver behind the strong maths/code numbers in the GLM-4.5 lineage and models like it.

**Reward design** is where it gets subtle: (1) outcome reward (final answer correct) is clean but sparse for long solutions; (2) you often add light format/consistency rewards (answer in the required box, valid code that compiles) but must keep them small so the model does not game format over substance; (3) for agentic/multi-step tasks the goal-reached signal is delayed and credit assignment across steps is hard, which is why you sometimes add process-level checks. Guard against reward hacking even here - models will exploit weak test suites or degenerate solutions - so tests must be robust and you monitor for pathological strategies. You still keep a KL/reference anchor and usually keep some preference-based RL for the non-verifiable qualities.

**Follow-ups:** How do you handle sparse reward on long reasoning chains? What reward-hacking behaviours have you seen against unit-test rewards, and how do you defend?

</details>

### 11. How would you evaluate an agentic coding model on SWE-bench and TAU-bench style benchmarks without fooling yourself?

<details><summary><b>Answer</b></summary>

Start with what each measures. **SWE-bench Verified** gives the model a real GitHub issue and repository and asks it to produce a patch that makes the hidden tests pass - end-to-end software engineering, not a coding puzzle. **TAU-bench** measures tool-use agents in simulated domains (retail, airline) where the agent must follow policy and complete multi-turn tasks correctly. Both are *task-success* benchmarks, which is the right altitude for an agentic model, but both are easy to misread.

The traps to defend against: (1) **Contamination.** These repos and issues may be in pre-training data; a high score can reflect memorisation. Check dates, hold out fresh issues, and inspect whether the model reproduces the exact human patch versus solving it independently. (2) **Harness leakage.** Agentic scores depend heavily on scaffolding - retries, tools, context management, number of allowed steps. A "model" comparison that changes the harness is not a fair comparison; fix the harness or report it. (3) **Flaky tests and partial credit.** Some tests are non-deterministic; a pass can be luck. Run multiple seeds and report variance, not a single number. (4) **Reward/measure mismatch.** Passing hidden tests is not the same as a good patch (it may break unrelated behaviour); for a stronger read, review a sample of accepted patches. (5) **Pass@k inflation.** pass@1 and pass@8 tell different stories; state which and why.

Beyond the public sets, build an internal eval on your own tasks and languages, track per-step tool-call accuracy alongside end-to-end success, and version the eval so a model upgrade can be compared apples-to-apples. The signal is scepticism: you treat a leaderboard number as a hypothesis, not a result.

**Follow-ups:** How would you detect contamination concretely? Why can two labs report very different SWE-bench numbers for the same open weights?

</details>

### 12. Design the AutoGLM product end to end: a cloud service that lets users delegate multi-step phone tasks ("order my usual coffee") to an autonomous agent. Walk through the architecture and the failure modes.

<details><summary><b>Answer</b></summary>

Treat it as a real system, not a demo. **Requirements first:** latency tolerance (async, minutes is fine), task breadth (which apps), safety (never spend money without confirmation), and privacy (screenshots contain personal data).

**Architecture.** (1) An **agent runtime** that runs the perceive-decide-act loop against a device or emulator: capture screen, send to the model, receive a structured action, execute it, capture the new screen. (2) The **VLM policy** (CogAgent/GLM-4V lineage) for grounding instructions to on-screen elements and emitting actions; served with the inference stack (continuous batching, KV cache) since a 50-step task is 50+ forward passes. (3) A **planner/memory** component holding the goal, action history, and observed state so the agent knows progress and can recover. (4) A **tool/skill layer** for deterministic shortcuts where an API exists (use the real API instead of tapping through a UI when you can - faster and more reliable). (5) An **orchestration/queue** layer because tasks are long-running and async, with per-user isolation of the device session.

**Safety and control.** Gate irreversible actions (payment, send, delete) behind explicit user confirmation. Hard caps on steps and on repeated actions to prevent runaway loops and cost. A kill switch and full trajectory logging (screens + actions) for audit and debugging - and that log is also your future training/eval data.

**Failure modes to name.** Grounding errors on unfamiliar UIs; non-deterministic screens (pop-ups, ads, A/B layouts) derailing the plan; app updates breaking learned flows; getting stuck in a loop; privacy exposure in screenshots; and the sharp end - taking a wrong irreversible action. Mitigations: verify state after each step, recovery behaviours, confirmation gates, and continuous evaluation on a suite of real apps with success-rate tracking and regression tests before shipping a model update.

**Evaluation and ops.** Task success rate as the north star, per-step grounding accuracy as the leading indicator, and a canary/rollback path for model swaps because agent behaviour shifts more than chat quality across versions.

**Follow-ups:** Where do you draw the line for "requires user confirmation"? How do you keep the agent working when a target app redesigns its UI?

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - the highest-leverage dir. GLM internals live here: the blank-infilling objective, MoE routing and load balancing, attention variants, RoPE and long-context, tokenization, and Multi-Token Prediction. Be able to implement, not just describe.
2. **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - RLHF, RLVR, expert-then-unified post-training, self-distillation. Their public work is dense here; know reward design cold.
3. **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - long-horizon agents, GUI grounding, tool-call reliability. AutoGLM/CogAgent make this a first-class topic, not a bonus.
4. **[08-inference-and-production](../08-inference-and-production/)** - MoE serving (active vs total params), speculative decoding via MTP, quantization, KV-cache economics. Open weights make inference a shared concern.
5. **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - SWE-bench / TAU-bench style agentic and coding evaluation, contamination, per-step vs end-to-end metrics.
6. **[11-ai-system-design](../11-ai-system-design/)** - use the framework on agent-product prompts. Closest case study: **[AI code assistant](../11-ai-system-design/case-studies/02-ai-code-assistant.md)** for the coding-agent angle, with **[customer support agent](../11-ai-system-design/case-studies/03-customer-support-agent.md)** for the tool-using agent loop.

Company-specific moves:

- **Read the GLM technical reports.** Start with the original GLM paper (autoregressive blank infilling) and the GLM-130B report for the bilingual roots, then the GLM-4.5 (ARC) technical report for the current MoE, hybrid-reasoning, and RL recipe. Being fluent in expert-then-unified training and slime's colocated/disaggregated modes covers a lot of ground.
- **Run an open GLM model.** GLM-4.5 / GLM-4.5-Air weights are public; serve one, try thinking vs non-thinking mode, and speak about active-vs-total-parameter serving from experience.
- **Use the agent products.** Try AutoGLM and read the CogAgent write-up so you can talk about GUI grounding, action spaces, and long-horizon recovery concretely.
- **Prepare bilingually.** Be ready to reason about Chinese/English tokenization, data mixing, and per-language evaluation - it is a genuine differentiator here.
- **Have a "why Zhipu" answer** grounded in their open-weights strategy, ARC focus, and Tsinghua research culture, plus a crisp deep-dive on your own strongest project.

## Sources

- [GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models (arXiv 2508.06471)](https://arxiv.org/abs/2508.06471) - MoE sizes (355B/32B, Air 106B), 23T-token multi-stage training, expert-then-unified post-training, slime RL, benchmark figures
- [GLM: General Language Model Pretraining with Autoregressive Blank Infilling (arXiv 2103.10360)](https://arxiv.org/abs/2103.10360) - the foundational objective and 2D positional encoding
- [GLM-130B: An Open Bilingual Pre-Trained Model (Tsinghua KEG)](https://keg.cs.tsinghua.edu.cn/glm-130b/posts/glm-130b/) - bilingual pre-training roots, scale, and training setup
- [GLM-4.5 GitHub (zai-org)](https://github.com/zai-org/GLM-4.5) - open-weight release, thinking/non-thinking modes, MTP, license
- [CogAgent: A Visual Language Model for GUI Agents (CVPR 2024)](https://openaccess.thecvf.com/content/CVPR2024/papers/Hong_CogAgent_A_Visual_Language_Model_for_GUI_Agents_CVPR_2024_paper.pdf) - GUI grounding and agent design
- [CogAgent GitHub (zai-org)](https://github.com/zai-org/CogAgent) - open GUI-agent model based on GLM-4V-9B
- [Zhipu AI NLP Researcher posting (ISWC 2023)](https://iswc2023.semanticweb.org/job-posting/zhipu-ai-nlp-researcher/) - real role requirements (pre-training, alignment, RLHF, evaluation; publication and coding bar)
- [What is Zhipu AI? (The Wire China)](https://www.thewirechina.com/2025/02/16/what-is-zhipu-ai/) - founding, Tsinghua ties, founders, funding, government links, Entity List
- [Z.ai official site](https://www.zhipuai.cn/en) - product lineup and international branding
- [InfoQ: GLM-4.5 launch coverage](https://www.infoq.com/news/2025/08/glm-4-5/) - third-party summary of architecture and capabilities

*Note: no official interview-process page or substantial English candidate reports were found; the loop section is inferred from category norms and Zhipu's stated role requirements, and is labelled as such.*
