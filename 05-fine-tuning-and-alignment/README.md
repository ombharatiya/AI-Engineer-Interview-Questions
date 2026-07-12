# 🎛️ Fine-tuning, RLHF & Alignment

This topic shows up in nearly every AI Engineer loop because it separates people who call APIs from people who can change model behaviour. Expect it if you're interviewing for GenAI/LLM engineer roles at frontier labs, applied ML teams at big tech, or any startup that ships custom models - interviewers use it to probe whether you know *when* to fine-tune, what it costs, and how post-training actually works under the hood.

## Crash course

### The decision framework: prompt → RAG → fine-tune

**Fine-tuning changes form; RAG changes knowledge.** The default escalation path is: prompt engineering (hours, free) → RAG (days, adds fresh/private knowledge) → fine-tuning (weeks, changes behaviour). Fine-tune when you need consistent **style/format/tone**, reliable **structured output**, **latency/cost wins** (a tuned 8B replacing a frontier model, or cutting a 2,000-token system prompt), or **narrow-task skill** (classification, extraction, a house SQL dialect). Don't fine-tune to inject facts - knowledge injection via SFT is unreliable and goes stale; that's RAG's job (or continued pretraining if the *domain language itself* is foreign, e.g. legal or genomics corpora). The nuance: real systems combine them - RAG for facts, a fine-tuned model that's better at *using* retrieved context.

### SFT mechanics

**Supervised fine-tuning (SFT)** = next-token prediction on curated (prompt, response) pairs rendered through the model's **chat template** - the exact special-token markup (e.g. `<|im_start|>`, `[INST]`, header tokens) the model was post-trained with. Template mismatch between training and inference is the #1 silent killer of fine-tunes.

**Loss masking:** compute cross-entropy only on response tokens; set prompt-token labels to `-100` so the model learns to *answer*, not to *reproduce prompts*:

```python
labels = input_ids.clone()
labels[:prompt_len] = -100   # ignored by F.cross_entropy
```

**Quality >> quantity.** LIMA showed ~1,000 meticulously curated examples can align a 65B base model. A few hundred to a few thousand excellent, deduplicated, diverse examples beat 100k scraped ones. Dedup (exact + near-dup via MinHash/embeddings), decontaminate against your eval sets, and manually read a random sample - always.

### PEFT: LoRA and QLoRA

**LoRA** freezes base weights and learns a low-rank update per targeted matrix:

$$W' = W + \frac{\alpha}{r} BA,\quad B\in\mathbb{R}^{d\times r},\ A\in\mathbb{R}^{r\times k},\ r\ll d$$

`B` starts at zero so training begins at the base model. Typical `r` = 8-64, `alpha` ≈ r or 2r, targeting all attention projections (q/k/v/o) and often the MLP up/down/gate matrices. Trainable params drop to ~0.1-1% of the model, and - the real win - **no gradients or Adam states for frozen weights**, cutting training memory several-fold. Adapters can be merged into `W` for zero inference overhead, or kept separate for **multi-LoRA serving** (one base model, many hot-swappable adapters, as in vLLM/S-LoRA).

**QLoRA** = frozen base quantized to 4-bit **NF4** (an information-theoretically motivated data type for normally distributed weights) + **double quantization** (quantize the quantization constants) + **paged optimizers** (spill optimizer states to CPU RAM on spikes), with LoRA trained in bf16 on top. Fine-tunes a 65-70B model on a single 48 GB GPU with little measured quality loss on benchmarks - though you're training atop a slightly noisy base.

### Training memory math (why you can't full-fine-tune 7B on a 24 GB card)

Mixed-precision full fine-tuning with Adam costs roughly **16 bytes/param**: 2 (bf16 weights) + 2 (grads) + 4 (fp32 master weights) + 8 (fp32 Adam m and v). A 7B model ⇒ ~112 GB before activations. Levers: **gradient checkpointing** (recompute activations, ~30% slower, big memory win), **gradient accumulation** (simulate large batches), **ZeRO/FSDP** (shard optimizer states/grads/params across GPUs), and PEFT (optimizer states only for adapter params).

### Key hyperparameters

| Knob | Full FT | LoRA |
|---|---|---|
| LR | ~1e-5-5e-5 | ~1e-4-2e-4 |
| Epochs | 1-3 | 1-5 |
| Schedule | cosine + ~3% warmup | same |

Watch for **catastrophic forgetting** (general capability regressions): mitigate with a lower LR, fewer epochs, LoRA instead of full FT, and mixing ~5-25% general instruction data into your task data. **Overfitting signals:** eval loss rising while train loss falls, verbatim regurgitation, collapsing output diversity, benchmark regressions. Always eval **before and after** on (1) a held-out task set and (2) a general-capability suite (e.g. MMLU-style, instruction following) to catch regressions.

### Preference optimisation: RLHF → DPO → GRPO

**RLHF pipeline** (InstructGPT recipe): SFT → collect human preference pairs → train a **reward model** with a Bradley - Terry loss, $-\log\sigma(r(y_w) - r(y_l))$ → optimise the policy with **PPO** against that reward, with a per-token **KL penalty to the frozen reference model** so the policy can't drift into degenerate high-reward text. Remove the KL term and you get **reward hacking**: sycophancy, bloated confident-sounding answers, gibberish that spoofs the RM.

**DPO** collapses this: the KL-constrained RLHF objective has a closed form, so the policy itself defines an *implicit reward* $\beta\log\frac{\pi(y|x)}{\pi_{ref}(y|x)}$ and you can train directly on preference pairs with a classification loss - no reward model, no RL loop, no sampling during training. Cheaper and stabler; PPO-style online RL still wins when you can generate and score fresh samples (and is the norm at frontier labs). One-liners: **IPO** (bounded objective, less overfitting to preferences), **KTO** (works on binary good/bad labels, no pairs needed), **ORPO** (folds preference loss into SFT, no reference model).

**GRPO** (DeepSeekMath/R1): sample a *group* of responses per prompt, use each response's advantage relative to the group mean instead of a learned value network - cheap PPO. Paired with **verifiable rewards** (unit tests, math answer checkers), it drives RL for reasoning: math/code are RL-friendly because reward is programmatic, so no reward model to hack. **RLAIF/Constitutional AI** replaces human labels with AI feedback guided by an explicit set of principles.

### Distillation & synthetic data

**Black-box distillation** = generate synthetic training data from a stronger model (most common; check the teacher's ToS - many API providers restrict training competing models on outputs). **Logit distillation** = match the teacher's full token distributions (needs open weights, more signal per example). Synthetic-data pitfalls: **mode collapse** (teacher's stylistic tics amplified), **error amplification** (teacher mistakes become ground truth), and eval contamination. Filter with verifiers/judges and keep human data in the mix.

## Interview questions

All 36 questions with detailed answers: [questions.md](questions.md)

## Red flags interviewers watch for

- Reaching for fine-tuning to "teach the model facts" - not knowing that knowledge belongs in RAG/continued pretraining and fine-tuning is for behaviour/form.
- Can't write the LoRA equation or explain what `r` and `alpha` do; thinks LoRA speeds up inference of an unmerged adapter.
- No memory math: can't estimate why full fine-tuning a 7B model needs ~112 GB with Adam, or where QLoRA's savings come from.
- Describes RLHF as "training on thumbs up/down" - can't articulate the reward model, PPO, or why the KL penalty against the reference model exists.
- Thinks DPO is strictly better than PPO (or vice versa) rather than knowing the offline-vs-online tradeoff.
- Never mentions evaluation: no held-out set, no before/after regression checks, no contamination awareness.
- Ignores chat templates and loss masking - a candidate who's actually fine-tuned a model has been burned by both.
- Treats synthetic data as free lunch - no mention of mode collapse, error amplification, or ToS/licensing constraints.

## Further reading

- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) - Hu et al., 2021
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) - Dettmers et al., 2023
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) - the InstructGPT paper (canonical RLHF recipe)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) - Rafailov et al., 2023
- [LIMA: Less Is More for Alignment](https://arxiv.org/abs/2305.11206) - Zhou et al., 2023
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) - Anthropic, 2022
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) - GRPO + verifiable rewards at scale
- [Hugging Face TRL documentation](https://huggingface.co/docs/trl) and [PEFT documentation](https://huggingface.co/docs/peft) - the reference open-source post-training stack
