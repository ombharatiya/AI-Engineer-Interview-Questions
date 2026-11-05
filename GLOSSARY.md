# 📖 Glossary

Every term this repo uses, defined in one line, with a link to the page that treats it properly. It is a lookup table, not a study guide: use it to unblock yourself mid-question, then read the topic when you have time.

The acronym table below is for scanning when someone drops an initialism you half-recognise. The A to Z after it has the actual definitions.

**Related:** [The AI Engineer 75](AI-ENGINEER-75.md) · [Night-before cheat sheet](CHEATSHEET.md) · [Study plans](STUDY_PLAN.md) · [Company pages](14-company-interview-questions/README.md) · [Role guides](15-role-guides/README.md)

---

## 🔤 Acronyms at a glance

| Acronym | Expands to | Acronym | Expands to |
|---|---|---|---|
| A2A | Agent2Agent (protocol) | AAIF | Agentic AI Foundation |
| ACL | Access control list | ANN | Approximate nearest neighbour |
| AP2 | Agent Payments Protocol | ASR | Automatic speech recognition |
| BPE | Byte-pair encoding | CFG | Classifier-free guidance |
| CoT | Chain of thought | DPO | Direct preference optimization |
| ECE | Expected calibration error | EMA | Exponential moving average |
| EP | Expert parallelism | FLOP | Floating-point operation |
| FSDP | Fully sharded data parallel | GQA | Grouped-query attention |
| GRPO | Group relative policy optimization | HBM | High-bandwidth memory |
| HITL | Human in the loop | HNSW | Hierarchical navigable small world |
| ICL | In-context learning | ITL | Inter-token latency |
| IVF | Inverted file index | KV | Key and value |
| LLM | Large language model | LoRA | Low-rank adaptation |
| MCP | Model Context Protocol | MHA | Multi-head attention |
| MLA | Multi-head latent attention | MLE | Maximum likelihood estimation |
| MMR | Maximal marginal relevance | MoE | Mixture of experts |
| MQA | Multi-query attention | MRR | Mean reciprocal rank |
| MSE | Mean squared error | MTEB | Massive Text Embedding Benchmark |
| MTP | Multi-token prediction | nDCG | Normalized discounted cumulative gain |
| OCR | Optical character recognition | PEFT | Parameter-efficient fine-tuning |
| PII | Personally identifiable information | PP | Pipeline parallelism |
| PPO | Proximal policy optimization | PQ | Product quantization |
| PRM | Process reward model | PSI | Population stability index |
| QLoRA | Quantized LoRA | QPS | Queries per second |
| RAG | Retrieval-augmented generation | RLAIF | RL from AI feedback |
| RLHF | RL from human feedback | RLVR | RL from verifiable rewards |
| RMF | Risk Management Framework (NIST AI) | ROC | Receiver operating characteristic |
| RoPE | Rotary position embedding | RRF | Reciprocal rank fusion |
| SAE | Sparse autoencoder | SFT | Supervised fine-tuning |
| SGD | Stochastic gradient descent | SLO | Service level objective |
| SSE | Server-sent events | SSM | State space model |
| STT | Speech to text | TP | Tensor parallelism |
| TPOT | Time per output token | TTFT | Time to first token |
| TTS | Text to speech | VAD | Voice activity detection |
| VAE | Variational autoencoder | ViT | Vision transformer |
| VLA | Vision-language-action model | VLM | Vision-language model |
| WER | Word error rate | ZDR | Zero data retention |

---

## A

- **A2A** - Agent2Agent, the protocol for calling a peer agent across a team or company boundary, built on Agent Cards and long-running tasks, and hosted by the Agentic AI Foundation alongside MCP since August 2026. MCP connects an agent to tools, A2A connects it to other agents. [06 Agents](06-agents-and-tool-use/README.md)
- **A/B test** - an online experiment splitting users between variants to see which one moves the real product metric. [07 Evals](07-evaluation-and-observability/README.md)
- **Accuracy** - the share of predictions that are correct, and a liar on imbalanced data, where always predicting the majority class can score 99%. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **ACL filtering** - enforcing per-user permissions inside the retrieval query itself, never by asking the model to withhold results. [04 RAG](04-rag-and-retrieval/README.md)
- **Adam** - an optimizer with a per-parameter adaptive step size derived from moving averages of the gradient and its square. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **AdamW** - Adam with weight decay decoupled from the adaptive update, which is why it is the transformer default. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Agent** - a model plus tools plus context, running in a loop with stop conditions, deciding for itself what to do next. [06 Agents](06-agents-and-tool-use/questions.md)
- **Agent Card** - JSON metadata served at `/.well-known/agent-card.json` declaring an A2A agent's identity, skills, endpoint and auth requirements, so peers can discover it without a bespoke integration. [06 Agents](06-agents-and-tool-use/README.md)
- **Agent Skills** - an open format for packaging procedural knowledge: a folder holding a `SKILL.md` plus optional scripts, references and assets, loaded by progressive disclosure (name and description at startup, the body when the task matches, bundled files only when needed). Governed under the Agentic AI Foundation since October 2026. [06 Agents](06-agents-and-tool-use/README.md)
- **Agentic AI Foundation (AAIF)** - the Linux Foundation body that hosts open agent standards, set up in December 2025 with MCP, goose and AGENTS.md. As of October 2026 it hosts ten projects, including A2A (joined August 2026) and Agent Skills, Open Responses, OpenEnv and OpenSandbox (all joined October 2026). [06 Agents](06-agents-and-tool-use/questions.md)
- **Agentic RAG** - retrieval exposed as a tool the model calls in a loop, refining the query between calls instead of retrieving once. [04 RAG](04-rag-and-retrieval/README.md)
- **AGENTS.md** - a repository-level instruction file that coding agents load on every session: build and test commands, conventions and no-go areas, scoped to one repo, unlike a skill that loads on demand. [03 Prompting](03-prompt-engineering-and-context/questions.md)
- **ALiBi** - positional handling that adds a linear distance penalty to attention scores instead of using position embeddings. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Alignment** - post-training that shapes behaviour, both helpfulness and refusals, into the weights themselves. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **ANN** - approximate nearest neighbour search, trading exact recall for sublinear query time once brute force stops scaling. [04 RAG](04-rag-and-retrieval/README.md)
- **AP2** - the Agent Payments Protocol, which binds an agent-initiated purchase to signed user mandates so a merchant can verify what the user actually authorised. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **Arithmetic intensity** - FLOPs performed per byte moved, the ratio that decides whether an operation is compute-bound or memory-bound. [08 Inference](08-inference-and-production/README.md)
- **Attention** - each token emits a query, key and value, and mixes other positions' values weighted by scaled dot-product scores. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **AWQ** - activation-aware 4-bit post-training quantization that scales the channels that matter most before rounding. [08 Inference](08-inference-and-production/README.md)

## B

- **Barge-in** - letting a user interrupt a speaking voice agent, which means cancelling TTS and generation and truncating state to what was actually heard. [10 Multimodal](10-multimodal/README.md)
- **Batch API** - an asynchronous bulk endpoint priced at roughly half the synchronous rate, for work that tolerates delay. [08 Inference](08-inference-and-production/README.md)
- **BatchNorm** - normalization across the batch dimension, unusable in transformers because of variable-length sequences and batch-size-1 decoding. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Beam search** - decoding that keeps several partial sequences to maximise total likelihood, good for translation and ASR, bland and repetitive for open-ended text. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Best-of-N** - sampling N candidates and keeping the one a reward model, verifier or test suite scores highest, the simplest way to buy accuracy with test-time compute. [03 Prompting](03-prompt-engineering-and-context/questions.md)
- **Bias-variance decomposition** - expected test error as bias squared plus variance plus irreducible noise, diagnosed from the train and validation gap. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Bi-encoder** - embeds query and document independently, which is what makes precomputation and ANN search possible and what caps quality. [04 RAG](04-rag-and-retrieval/questions.md)
- **BM25** - the classic lexical ranking function, which nails IDs, SKUs, error codes and fresh jargon that dense retrieval misses. [04 RAG](04-rag-and-retrieval/README.md)
- **BPE** - byte-pair encoding, a tokenizer trained by repeatedly merging the most frequent adjacent pair until the vocab is full. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Bradley-Terry** - the pairwise preference model behind reward-model training and Arena-style Elo rankings. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)

## C

- **C2PA / Content Credentials** - a cryptographically signed provenance manifest attached to media, which strips on re-encode or screenshot. [10 Multimodal](10-multimodal/README.md)
- **Calibration** - whether a predicted 0.8 actually means 80%, a property separate from ranking quality. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **CaMeL** - a hardened plan-then-execute design where the planner writes code from the trusted request alone and an interpreter enforces data-flow policy. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Canary eval** - a scheduled eval run against the live production config so silent upstream changes page you instead of your users. [07 Evals](07-evaluation-and-observability/README.md)
- **Catastrophic forgetting** - general capability regressing after fine-tuning too hard on a narrow task, mitigated with lower LR, fewer epochs and mixed-in general data. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Causal mask** - the upper-triangular minus-infinity mask applied before softmax so a position cannot attend to later tokens. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **CFG** - classifier-free guidance, extrapolating between conditional and unconditional denoising to trade diversity for prompt adherence. [10 Multimodal](10-multimodal/README.md)
- **Chain of thought** - prompting the model to write intermediate reasoning before the answer, valuable on multi-step problems and wasted latency on lookups. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Chat template** - the exact special-token markup a model was post-trained with, and the single most common silent killer of fine-tunes. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Chinchilla** - the scaling result that compute-optimal training grows parameters and tokens together, roughly 20 tokens per parameter. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Chunked prefill** - splitting a long prefill into pieces mixed into decode batches so one huge prompt does not stall every other user's stream. [08 Inference](08-inference-and-production/README.md)
- **Chunking** - splitting documents into retrievable units, typically 256 to 1024 tokens with 10 to 20% overlap. [04 RAG](04-rag-and-retrieval/questions.md)
- **Circuit breaker** - a per-provider trip that stops sending traffic to a dependency that is already failing. [08 Inference](08-inference-and-production/README.md)
- **CLIP** - contrastive image-text pretraining that lands both modalities in one embedding space, which is why zero-shot classification and cross-modal retrieval work. [10 Multimodal](10-multimodal/README.md)
- **ColBERT / late interaction** - per-token embeddings scored by summed max similarity, sitting between bi-encoder speed and cross-encoder accuracy. [04 RAG](04-rag-and-retrieval/README.md)
- **ColPali** - screenshot-based document retrieval that embeds page images directly, so nothing is lost in parsing. [10 Multimodal](10-multimodal/README.md)
- **Compaction** - summarising old turns while keeping recent ones verbatim, so an agent's context stays usable over a long trajectory. [06 Agents](06-agents-and-tool-use/README.md)
- **Confused deputy** - a privileged component tricked by a less-privileged party into using its authority on that party's behalf, which is exactly what an injected agent with broad credentials does. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **Constitutional AI** - alignment in which the model critiques and revises its own output against a written set of principles. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Constrained decoding** - compiling a schema into a grammar and masking invalid tokens in the logits, which guarantees syntax but not semantics. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Contamination** - eval data present in the pretraining corpus, so the score measures memorisation rather than capability. [07 Evals](07-evaluation-and-observability/README.md)
- **Context engineering** - managing the whole token budget across turns (tools, retrieved docs, memory, history), not just optimising one string. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Context rot** - quality decay as stale errors, bloated tool output and irrelevant retrievals accumulate, well below the hard context limit. [06 Agents](06-agents-and-tool-use/README.md)
- **Contextual retrieval** - prepending a short LLM-written blurb situating each chunk in its document before embedding it. [04 RAG](04-rag-and-retrieval/README.md)
- **Continued pretraining** - more next-token training on domain data, the right move when the domain language itself is foreign rather than just the facts. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Continuous batching** - composing the serving batch per decode step so finished requests leave and queued ones join mid-flight. [08 Inference](08-inference-and-production/questions.md)
- **Cosine similarity** - direction-only similarity that ignores magnitude, the default for comparing text embeddings. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Covariate shift** - the input distribution moves while the input-to-label relationship holds, as opposed to concept drift where the relationship itself changes. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Cross-encoder** - scores query and document jointly through one transformer with full attention, accurate but one forward pass per candidate. [04 RAG](04-rag-and-retrieval/questions.md)
- **Cross-entropy** - the maximum-likelihood loss for categorical outputs, whose gradient through softmax is simply predicted minus actual. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Cross-validation** - rotating held-out folds to use a small dataset efficiently, replaced by temporal splits for anything time-dependent. [01 ML foundations](01-ml-and-dl-foundations/README.md)

## D

- **Data leakage** - training information reaching the evaluation, in forms as subtle as fitting a scaler before splitting or the same user in both sets. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Decode** - the sequential phase that emits one token at a time, memory-bandwidth-bound because every weight must be streamed per token. [08 Inference](08-inference-and-production/questions.md)
- **Decoder-only** - the causal next-token architecture behind every mainstream LLM, where every position yields a training signal. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Defence in depth** - stacking input, output and action controls because no single guardrail holds against an adaptive attacker. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Diffusion** - generation by learning to reverse a gradual noising process, predicting the noise added at each step. [10 Multimodal](10-multimodal/README.md)
- **Disaggregated serving** - running prefill and decode on separate GPU pools and shipping the KV cache between them, so the compute-bound and bandwidth-bound phases are sized and batched independently. [08 Inference](08-inference-and-production/questions.md)
- **Distillation** - training a small model on a large model's outputs or logits, the standard way to compress reasoning behaviour into a cheap model. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **DiT** - the diffusion transformer backbone that replaced the U-Net in recent image models. [10 Multimodal](10-multimodal/README.md)
- **Double descent** - the observation that heavily overparameterized networks generalise better past the interpolation threshold, breaking the classical U-curve. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **DPO** - direct preference optimization, training on preference pairs with a classification loss and no reward model or RL loop. [05 Fine-tuning](05-fine-tuning-and-alignment/questions.md)
- **Drift** - the family of production failures where model version, input distribution, or cost and latency move under you without a deploy. [07 Evals](07-evaluation-and-observability/README.md)
- **Dropout** - randomly zeroing activations at train time as an implicit ensemble, usually set to zero in large-scale pretraining. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Dual-LLM pattern** - a privileged model that plans and calls tools but never reads untrusted content, paired with a quarantined model that reads it and returns typed variables. [09 Safety](09-safety-security-and-responsible-ai/README.md)

## E

- **Early stopping** - halting training when validation loss stops improving, cheap and close to L2 in effect. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **ECE** - expected calibration error, the summary number from a reliability diagram, fixed post hoc with temperature scaling. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Elicitation** - the MCP feature that lets a server ask the host to collect structured input from the user mid-operation, instead of guessing or failing. [06 Agents](06-agents-and-tool-use/questions.md)
- **Elo / Arena** - pairwise human preference ranking, hard to contaminate but measuring preference and style rather than task correctness. [07 Evals](07-evaluation-and-observability/README.md)
- **Embedding** - a vector whose geometry encodes meaning, compared with whatever similarity the model was trained with. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Emergent abilities** - apparent sharp capability jumps with scale, partly a measurement artifact of discontinuous metrics. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Encoder-decoder** - a bidirectional encoder feeding a cross-attending decoder, still strong for fixed input-to-output transforms like translation and ASR. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Encoder-only** - bidirectional masked-LM models such as BERT, which cannot generate and now live on as embedding and reranker models. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Error analysis** - reading 50 to 100 failing traces, clustering the failure descriptions, and fixing the biggest cluster first. [07 Evals](07-evaluation-and-observability/README.md)
- **Eval set** - the versioned dataset that encodes what good means for your product, and the asset that survives every model swap. [07 Evals](07-evaluation-and-observability/questions.md)
- **Exfiltration channel** - any path by which data can leave the system, the third leg of the lethal trifecta. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Expert parallelism** - sharding an MoE model's experts across GPUs and routing tokens to them with all-to-all communication, which makes interconnect bandwidth and load balance the bottlenecks. [08 Inference](08-inference-and-production/questions.md)
- **Exponential backoff with jitter** - retry spacing that randomises the delay so clients do not synchronise into a retry storm. [08 Inference](08-inference-and-production/README.md)

## F

- **Faithfulness** - whether every claim in a generated answer is supported by the retrieved context, usually judged claim by claim. [07 Evals](07-evaluation-and-observability/README.md)
- **Few-shot** - putting worked examples in the prompt to anchor format and sharpen fuzzy decision boundaries. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **FID** - a distribution-level realism score for generated images, meaningless for judging any single image. [10 Multimodal](10-multimodal/README.md)
- **Fine-tuning** - further training that changes form, style and narrow skill, and the wrong tool for injecting facts. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **FlashAttention** - an IO-aware exact attention implementation that tiles into on-chip SRAM and never materialises the full score matrix. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Flow matching** - training a generator to predict the velocity that carries noise to data along a near-straight path, now the usual objective for image and video models because it needs fewer sampling steps. [10 Multimodal](10-multimodal/README.md)
- **FP4 (NVFP4 / MXFP4)** - four-bit floating-point formats with fine-grained block scales, natively accelerated on Blackwell-class GPUs, the next step down from FP8 for weights and, increasingly, for the KV cache. [08 Inference](08-inference-and-production/README.md)
- **FP8 / INT8** - eight-bit formats that shrink weights and, when activations are quantized too, accelerate the matmuls on tensor cores. [08 Inference](08-inference-and-production/README.md)
- **FSDP / ZeRO** - sharding optimizer states, gradients and parameters across GPUs so a model too large for one device can still train. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)

## G

- **GCG** - the gradient-searched adversarial suffix attack, notable because the strings transfer across models. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **GGUF** - the quantized model file format used by the llama.cpp and Ollama local-inference ecosystem. [08 Inference](08-inference-and-production/README.md)
- **Golden set** - a labelled set of real, hard cases you gate prompt and model changes on. [11 System design](11-ai-system-design/README.md)
- **Goodhart's law** - once a measure becomes a target it stops being a good measure, which is what happens to every headline benchmark. [07 Evals](07-evaluation-and-observability/README.md)
- **Goodput** - throughput that actually meets your latency SLO, the only throughput number worth reporting. [08 Inference](08-inference-and-production/README.md)
- **GPTQ** - Hessian-based 4-bit post-training weight quantization, one of the two standard methods alongside AWQ. [08 Inference](08-inference-and-production/README.md)
- **GQA** - grouped-query attention, where groups of query heads share one KV head, cutting cache size at near-MHA quality. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Gradient checkpointing** - recomputing activations in the backward pass instead of storing them, roughly 30% slower for a large memory win. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Gradient clipping** - capping the global gradient norm, conventionally at 1.0, so a loss spike does not destroy the run. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **GraphRAG** - building an entity and relationship graph at index time, worth the cost for relational or corpus-wide questions, not for factoid lookup. [04 RAG](04-rag-and-retrieval/README.md)
- **Grounding** - constraining the model to answer from supplied sources and cite them, the first line of defence against confident fabrication. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **GRPO** - group relative policy optimization, sampling a group of responses per prompt and using each one's reward relative to the group mean (scaled by the group's standard deviation) as the advantage, so no value network is trained. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Guardrail metric** - a must-never-regress number such as PII leakage or jailbreak rate, gated as a binary, never traded for quality. [07 Evals](07-evaluation-and-observability/README.md)
- **Guardrails** - the input, output and action checks around a model call: classifiers, moderation, schema validation and approval gates. [09 Safety](09-safety-security-and-responsible-ai/README.md)

## H

- **Hallucination** - confident fabrication, structural because the training objective rewards plausible next tokens rather than truth. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Handoff** - transferring conversation control to a specialist agent, the multi-agent pattern that suits distinct domains like support triage. [06 Agents](06-agents-and-tool-use/README.md)
- **HBM** - the GPU's high-bandwidth memory, whose bandwidth sets the hard ceiling on batch-1 decode speed. [08 Inference](08-inference-and-production/README.md)
- **Hidden Context Exposure** - the OWASP 2026 category (LLM08) that replaces system prompt leakage and widens it to developer instructions, tool and function schemas and retrieved policy text: anything in the context the user was never meant to see. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **HITL** - human in the loop, the review queue and approval gate for low-confidence outputs and high-risk actions. [11 System design](11-ai-system-design/README.md)
- **HNSW** - a multi-layer navigable small-world graph index, the standard high-recall ANN structure, tuned with M and ef_search. [04 RAG](04-rag-and-retrieval/README.md)
- **HumanEval** - a set of 164 Python problems scored with pass@k, now saturated and small. [07 Evals](07-evaluation-and-observability/README.md)
- **Hybrid search** - running lexical and dense retrieval together and fusing their rankings, the fix for queries containing IDs or jargon. [04 RAG](04-rag-and-retrieval/README.md)
- **HyDE** - having the model write a hypothetical answer and embedding that instead of the question, since answers sit closer to documents. [04 RAG](04-rag-and-retrieval/README.md)

## I

- **Idempotency key** - a client-supplied token that makes a retried side-effectful call safe to repeat. [08 Inference](08-inference-and-production/README.md)
- **In-context learning** - inferring the task from demonstrations in the prompt, with no weight update. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Indirect prompt injection** - instructions planted in content your app processes on someone else's behalf, dangerous because the victim never sees the attack. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **InfoNCE** - the contrastive loss behind CLIP and modern sentence embedders, where the positive pair must beat in-batch negatives. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Instruction hierarchy** - training-time privileging of system over user over tool content, which lowers attack success rates but is probabilistic, not enforced. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Interleaving** - mixing two rankers' results into one list to reach significance with far less traffic than an A/B test. [07 Evals](07-evaluation-and-observability/README.md)
- **IVF** - an inverted-file ANN index that clusters vectors into cells and probes only the nearest ones. [04 RAG](04-rag-and-retrieval/README.md)

## J

- **Jailbreak** - an attack on the model's safety training to elicit forbidden content, a different attacker and owner from prompt injection. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **JSON mode** - the model is instructed to emit JSON, so you still validate and retry, unlike constrained decoding. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Judge (LLM-as-judge)** - grading open-ended output with another model and a rubric, reliable only after you measure its agreement with humans. [07 Evals](07-evaluation-and-observability/questions.md)

## K

- **KL penalty** - the term keeping an RL-tuned policy near its frozen reference, and the thing whose removal invites reward hacking. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **KTO** - preference tuning that works on binary good and bad labels, so you do not need paired comparisons. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **KV cache** - stored keys and values for every past token, turning quadratic recompute into linear lookups at a large memory cost. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **KV cache quantization** - storing keys and values in FP8 or INT8, and on recent engines in 4-bit formats such as NVFP4 (roughly half the memory of FP8, dequantized before attention, so it saves memory and bandwidth rather than compute), a lever that directly buys batch size and therefore throughput. [08 Inference](08-inference-and-production/README.md)

## L

- **Late chunking** - embedding the whole document with a long-context embedder first, then pooling token embeddings per chunk. [04 RAG](04-rag-and-retrieval/README.md)
- **Latent diffusion** - running the diffusion process in a compressed VAE latent space rather than on pixels, which is what makes it tractable. [10 Multimodal](10-multimodal/README.md)
- **LayerNorm** - normalization across features within each token, batch-independent and therefore fine at batch size 1. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Lethal trifecta** - private data access plus untrusted content plus an exfiltration channel, the combination you design around by removing one leg. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **LIMA** - the result that roughly 1,000 meticulously curated examples can align a large base model, quality over quantity. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Llama Guard** - a safeguard model that classifies content against a hazard taxonomy, used as an input or output filter. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Logit masking** - the mechanism constrained decoding uses, setting invalid tokens to minus infinity before sampling. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Logprobs** - per-token log probabilities from the API, your tool for confidence scoring, classification and perplexity evals. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **LoRA** - a low-rank adapter update, W' = W + (alpha/r)BA, with base weights frozen and trainable parameters at roughly 0.1 to 1% of the model. [05 Fine-tuning](05-fine-tuning-and-alignment/questions.md)
- **Lost in the middle** - the U-shaped finding that models attend best to the start and end of a long context, so key material belongs at the edges. [03 Prompting](03-prompt-engineering-and-context/README.md)

## M

- **Mamba / SSM** - a selective state space layer that carries a fixed-size recurrent state instead of a growing KV cache, linear in sequence length and usually mixed with attention layers in hybrid models. [08 Inference](08-inference-and-production/questions.md)
- **Many-shot jailbreak** - hundreds of faux dialogue turns exploiting in-context learning in a long window to override safety training. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Matryoshka embeddings** - vectors trained so their prefixes are valid embeddings, letting you truncate for a cheap first pass and refine later. [04 RAG](04-rag-and-retrieval/README.md)
- **MCP** - the Model Context Protocol, an open standard (now governed under the Agentic AI Foundation) turning N times M bespoke integrations into N plus M, with tools, resources and prompts as server primitives. [06 Agents](06-agents-and-tool-use/questions.md)
- **MCP Apps** - an official MCP extension that lets a server ship interactive UI the host renders in a sandbox, which widens the server's attack surface from text to active content. [06 Agents](06-agents-and-tool-use/questions.md)
- **Memorisation** - models reproducing training data verbatim, which is why training and fine-tuning corpora need dedup and PII scrubbing. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Metadata filtering** - restricting an ANN search by tenant, date or ACL, which has to happen inside the index traversal rather than after top-k. [04 RAG](04-rag-and-retrieval/README.md)
- **MHA** - multi-head attention, splitting the model dimension into parallel heads so different relations can be attended to at once. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Mixed precision** - training with bf16 weights and gradients alongside fp32 master weights and optimizer states, roughly 16 bytes per parameter with Adam. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **MLA** - multi-head latent attention, DeepSeek's variant that caches one low-rank latent vector per token and reconstructs keys and values from it, going further than GQA on KV memory. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **MMLU** - a 57-subject multiple-choice knowledge benchmark, saturated at the frontier and widely contaminated. [07 Evals](07-evaluation-and-observability/README.md)
- **MMR** - maximal marginal relevance, picking results one at a time by trading relevance to the query against similarity to what is already selected, the standard fix for near-duplicate chunks. Not to be confused with MRR. [04 RAG](04-rag-and-retrieval/questions.md)
- **Modality gap** - the observation that image and text embeddings occupy separated cones inside CLIP's shared space. [10 Multimodal](10-multimodal/README.md)
- **Mode collapse** - synthetic training data amplifying the teacher model's stylistic tics until output diversity dies. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Model card / system card** - documentation of intended use, evals and limitations, for the model and for your deployed system respectively. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Model gateway** - the single choke point for every LLM call, handling auth, quotas, retries, provider failover and usage metering. [11 System design](11-ai-system-design/README.md)
- **MoE** - mixture of experts, routed expert MLPs giving large total parameters with a small active count per token, at the cost of holding every expert in memory. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Momentum** - keeping a moving average of gradients to damp oscillation across ravines and accelerate consistent directions. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **MQA** - multi-query attention, where all query heads share a single KV head, shrinking the cache at some quality cost. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **MRR** - mean reciprocal rank, scoring how high the first relevant result appeared. [04 RAG](04-rag-and-retrieval/README.md)
- **MTEB** - the standard embedding benchmark, useful for shortlisting and useless as final proof on your own domain. [04 RAG](04-rag-and-retrieval/README.md)
- **Multi-agent** - an orchestrator delegating to workers, which wins on parallel read-heavy work and hurts on write-heavy shared state. [06 Agents](06-agents-and-tool-use/README.md)
- **Multimodal RAG** - retrieval over visually rich documents, usually by captioning figures at ingestion or embedding page images directly. [10 Multimodal](10-multimodal/README.md)
- **Multi-token prediction (MTP)** - training extra heads to predict several future tokens, which densifies the training signal and leaves a built-in drafter for speculative decoding. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Muon** - an optimizer that orthogonalises the momentum update for 2D weight matrices, adopted by some frontier pretraining runs as an alternative to AdamW for hidden layers. [01 ML foundations](01-ml-and-dl-foundations/questions.md)

## N

- **nDCG** - a graded-relevance ranking metric that scores the whole result list, not just the first hit. [04 RAG](04-rag-and-retrieval/README.md)
- **NF4** - the 4-bit data type QLoRA quantizes the frozen base to, designed for normally distributed weights. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Nucleus sampling (top-p)** - keeping the smallest set of tokens whose cumulative probability reaches p, so the cutoff adapts to model confidence. [02 LLM fundamentals](02-llm-fundamentals/README.md)

## O

- **Observability** - tracing every model call, tool call and retrieval as spans with tokens, latency and cost attached, because you cannot debug what you did not record. [07 Evals](07-evaluation-and-observability/README.md)
- **OCR-free extraction** - sending the page image straight to a VLM instead of running a text-recognition pipeline first. [10 Multimodal](10-multimodal/README.md)
- **Online eval** - measuring on live traffic through A/B tests, interleaving and implicit signals, which confirms what offline evals only predict. [07 Evals](07-evaluation-and-observability/README.md)
- **OpenTelemetry GenAI conventions** - the standard attribute names for LLM spans, so traces stay portable across backends. [07 Evals](07-evaluation-and-observability/README.md)
- **Orchestrator-worker** - the subagent pattern whose real payoff is context isolation: a worker burns tokens and returns a short summary. [06 Agents](06-agents-and-tool-use/README.md)
- **ORPO** - preference optimisation folded into the SFT loss, with no separate reference model. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Over-refusal** - refusing benign requests, the failure mode that makes a model trivially safe and commercially useless. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **OWASP Top 10 for LLM Applications** - the shared vocabulary of AI security reviews, from prompt injection (LLM01) through improper output handling (LLM10) in the 2026 edition. Quote IDs with their year, because the numbering changed between editions. [09 Safety](09-safety-security-and-responsible-ai/questions.md)

## P

- **PagedAttention** - managing the KV cache in fixed-size blocks through a block table, virtual memory for the cache, which kills fragmentation. [08 Inference](08-inference-and-production/questions.md)
- **Parent-document retrieval** - matching on small precise chunks and returning the larger parent for context, also called small-to-big. [04 RAG](04-rag-and-retrieval/README.md)
- **pass@k** - the probability that at least one of k samples solves the problem, estimated without bias from n samples and c correct. [07 Evals](07-evaluation-and-observability/questions.md)
- **pass^k** - the probability that all k trials succeed, the consistency metric that matters for agents and that pass@k hides. [07 Evals](07-evaluation-and-observability/README.md)
- **PEFT** - parameter-efficient fine-tuning, training a small set of added parameters so no optimizer state is needed for frozen weights. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Pipeline parallelism** - sharding a model by layer ranges across devices, tolerant of slow interconnect but adding latency and bubbles. [08 Inference](08-inference-and-production/README.md)
- **Position bias** - a judge favouring whichever response it saw first, mitigated by running both orders and keeping consistent verdicts. [07 Evals](07-evaluation-and-observability/README.md)
- **Position interpolation** - rescaling positions back inside the trained range, plus a short fine-tune, to extend usable context. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **PPO** - the RL algorithm in the classic RLHF recipe, optimising the policy against a reward model under a KL penalty. [05 Fine-tuning](05-fine-tuning-and-alignment/questions.md)
- **PQ** - product quantization, compressing vectors into subspace codebook codes for large memory savings at some recall cost. [04 RAG](04-rag-and-retrieval/README.md)
- **PR-AUC** - the honest ranking metric when positives are rare, with the prevalence rather than 0.5 as its baseline. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Precision and recall** - the share of predicted positives that are correct, and the share of actual positives that were found. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Prefill** - processing the whole prompt in one parallel pass, compute-bound, and the phase that sets time to first token. [08 Inference](08-inference-and-production/questions.md)
- **Prefix caching** - the serving-engine mechanism behind prompt caching: KV blocks for an already-seen prefix are hashed and reused across requests instead of recomputed. [08 Inference](08-inference-and-production/questions.md)
- **Pre-norm** - placing the norm inside the residual branch before each sublayer, which keeps the residual stream a clean identity path. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Process reward model (PRM)** - a reward model that scores each intermediate reasoning step rather than only the final answer, giving a dense signal at a much higher labelling cost. [05 Fine-tuning](05-fine-tuning-and-alignment/questions.md)
- **Prompt caching** - reusing the KV cache of a shared prefix across requests, which is why prompts should run stable content first and volatile content last. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Prompt injection** - attacking the application through content the model reads, unsolved because the context window has no privilege separation. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **PSI** - population stability index, a drift measure comparing a current input window against a reference one. [01 ML foundations](01-ml-and-dl-foundations/README.md)

## Q

- **QLoRA** - a 4-bit NF4 frozen base with double quantization and paged optimizers, with LoRA trained on top in bf16. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Quantization** - lowering weight or activation precision to cut memory and bandwidth, roughly free at 8-bit and measurable at 4-bit. [08 Inference](08-inference-and-production/README.md)
- **Query rewriting** - turning a conversational follow-up into a standalone search query, non-negotiable for multi-turn RAG. [04 RAG](04-rag-and-retrieval/README.md)

## R

- **RadixAttention** - SGLang's prefix cache, held as a radix tree of token sequences so requests sharing any prefix reuse its KV, with a scheduler that routes for cache hits. [08 Inference](08-inference-and-production/questions.md)
- **RAG** - retrieval-augmented generation, supplying fresh or private knowledge at query time instead of baking it into weights. [04 RAG](04-rag-and-retrieval/questions.md)
- **RAGAS** - a framework packaging the standard RAG metrics, faithfulness and answer relevance among them. [07 Evals](07-evaluation-and-observability/README.md)
- **ReAct** - interleaving thought, action and observation, now largely absorbed into native tool-calling loops. [06 Agents](06-agents-and-tool-use/README.md)
- **Reasoning model** - a model RL-trained to spend test-time compute on long chains of thought, buying accuracy on hard problems at higher latency and cost. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Recall@k** - whether the gold chunk made the top k, the retrieval metric that gates everything downstream. [04 RAG](04-rag-and-retrieval/README.md)
- **Reflection** - generate, critique, revise, which works when verification is grounded in an external signal and stalls after one or two rounds. [06 Agents](06-agents-and-tool-use/README.md)
- **Regression test** - running the eval suite on every prompt, model or retrieval change and blocking the merge on a regression. [07 Evals](07-evaluation-and-observability/README.md)
- **Reliability diagram** - a plot of predicted confidence against observed accuracy, the visual form of calibration. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Reranking** - a second, more expensive pass that reorders a wide candidate list, typically retrieve 100 to 200 then keep 5 to 20. [04 RAG](04-rag-and-retrieval/questions.md)
- **Residual stream** - the running hidden state that attention and MLP blocks read from and write into, the model's workspace. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Retrieval miss vs generation miss** - the first triage question for any bad RAG answer: were the right chunks fetched, or were they fetched and ignored? [04 RAG](04-rag-and-retrieval/questions.md)
- **Reward hacking** - a policy exploiting the reward model rather than improving, showing up as sycophancy and confident bloat. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **Reward model** - a model trained on human preference pairs to score responses during RLHF. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **RLAIF** - reinforcement learning from AI feedback, replacing most human preference labels with model-generated ones guided by principles. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **RLHF** - the SFT, reward model and PPO pipeline that turned raw completion models into steerable assistants. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **RLVR** - reinforcement learning on verifiable rewards such as passing tests or correct answers, which is what trains reasoning models. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **RMSNorm** - LayerNorm without mean-centring, just a rescale by the root mean square, cheaper and equally effective. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **ROC-AUC** - the probability a random positive outranks a random negative, insensitive to class imbalance and therefore misleading on rare positives. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **RoPE** - rotary position embedding, rotating query and key pairs so their dot product depends only on relative position. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Router** - the component that sends each request to the right model tier, usually the single biggest cost lever in the system. [11 System design](11-ai-system-design/README.md)
- **RRF** - reciprocal rank fusion, combining rankings by rank because BM25 scores and cosine similarities live on incomparable scales. [04 RAG](04-rag-and-retrieval/README.md)
- **Rug pull** - a third-party tool server changing its descriptions after you approved them, one of the MCP supply-chain attack classes. [09 Safety](09-safety-security-and-responsible-ai/README.md)

## S

- **SAE** - sparse autoencoder, trained on one layer's activations with a sparsity penalty to recover features that are far more interpretable than individual neurons. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Safetensors** - the data-only weight format that cannot execute code on load, unlike pickle-based checkpoints. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Sandboxing** - running model-generated code in an isolated container with no network egress, resource limits and a throwaway filesystem. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Scaling laws** - power-law relationships between compute, data, parameters and loss, and the reason deployment-optimal differs from compute-optimal. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Self-consistency** - sampling k reasoning paths above temperature zero and majority-voting the final answer, at k times the cost. [03 Prompting](03-prompt-engineering-and-context/README.md)
- **Self-preference bias** - judges preferring output from their own model family, mitigated by judging with a different family. [07 Evals](07-evaluation-and-observability/README.md)
- **Semantic caching** - serving a stored answer for a semantically similar query, which needs a tight similarity threshold to avoid wrong-answer hits, plus care around ACLs and freshness. [08 Inference](08-inference-and-production/README.md)
- **SentencePiece** - a language-agnostic tokenizer library that treats raw text as a stream and needs no pre-tokenization. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **SFT** - supervised fine-tuning on prompt and response pairs rendered through the chat template, with loss masked to response tokens. [05 Fine-tuning](05-fine-tuning-and-alignment/questions.md)
- **SGLang** - an open-source LLM serving engine built around RadixAttention prefix reuse and fast structured output, the main alternative to vLLM. [08 Inference](08-inference-and-production/questions.md)
- **SigLIP** - the sigmoid-loss successor to CLIP, now a common vision backbone for VLMs. [10 Multimodal](10-multimodal/README.md)
- **SKILL.md** - the required file at the root of an Agent Skill: YAML frontmatter with at least a name and description, which is all the agent sees until the skill activates, followed by the instructions. [06 Agents](06-agents-and-tool-use/README.md)
- **SLO** - the latency or quality objective you size capacity against, for example P99 TTFT under 800 ms. [08 Inference](08-inference-and-production/README.md)
- **Spec-driven development** - agentic delivery where a written spec (intent, constraints, acceptance criteria) is agreed and reviewed before an agent writes code, then kept as the source of truth the plan and diff are checked against. [15 Role guides](15-role-guides/forward-deployed-engineer.md)
- **Speculative decoding** - a cheap drafter proposes tokens the target model verifies in parallel, speeding up decode without changing the output distribution. [08 Inference](08-inference-and-production/questions.md)
- **SPLADE** - learned sparse retrieval, where a transformer emits weighted term expansions so an inverted index captures some semantics while keeping exact-match strength. [04 RAG](04-rag-and-retrieval/questions.md)
- **Spotlighting** - marking untrusted content with delimiters, encoding or per-line prefixes so the model can tell data from instructions, which lowers injection success but enforces nothing. [03 Prompting](03-prompt-engineering-and-context/questions.md)
- **SSE** - server-sent events, the transport that streams token deltas so perceived latency is TTFT rather than full completion time. [08 Inference](08-inference-and-production/README.md)
- **Streamable HTTP** - MCP's remote transport, a single HTTP endpoint with optional SSE streaming, which replaced the older two-endpoint HTTP plus SSE transport. [06 Agents](06-agents-and-tool-use/questions.md)
- **Structured output** - a response constrained to a schema and validated deterministically, the highest-leverage guardrail available. [03 Prompting](03-prompt-engineering-and-context/questions.md)
- **Subagent** - a worker with its own clean context window that returns a distilled summary to the orchestrator. [06 Agents](06-agents-and-tool-use/README.md)
- **SWE-bench** - resolving real GitHub issues. The Verified subset has aged into saturation and contamination, so harder variants such as SWE-bench Pro now carry the signal, and every score depends heavily on the agent harness. [07 Evals](07-evaluation-and-observability/questions.md)
- **Sycophancy** - telling users what they want to hear, agreeing with stated positions or flattering instead of correcting, a predictable side effect of optimising for human preference. [07 Evals](07-evaluation-and-observability/questions.md)
- **SynthID** - Google's watermarking family, which biases token sampling for text or embeds a signal in pixels for images, so a detector holding the key can test for it statistically. [09 Safety](09-safety-security-and-responsible-ai/questions.md)
- **System prompt leakage** - assume it happens, so never put secrets or unenforced authorisation logic in it. OWASP's 2026 list folds it into Hidden Context Exposure. [09 Safety](09-safety-security-and-responsible-ai/README.md)

## T

- **Temperature** - the softmax rescaling knob, where zero is greedy argmax and above one flattens the distribution. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **Temperature scaling** - post-hoc calibration that divides logits by a single fitted scalar without changing the ranking. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Tensor parallelism** - sharding every layer's matrices across GPUs with an all-reduce per layer, which cuts latency but needs fast interconnect. [08 Inference](08-inference-and-production/README.md)
- **Test-time compute** - spending more inference tokens (longer reasoning, sampling and voting, search against a verifier) to raise accuracy instead of training a bigger model. [03 Prompting](03-prompt-engineering-and-context/questions.md)
- **Token** - the unit the model actually sees, a subword ID rather than a character or a word, which is why letter counting and arithmetic fail. [02 LLM fundamentals](02-llm-fundamentals/questions.md)
- **Tool call** - a structured message naming a tool and its JSON arguments, which your runtime executes, never the model. [06 Agents](06-agents-and-tool-use/questions.md)
- **Tool description** - the prose the model reads to decide when to call a tool, effectively a prompt and worth writing like one. [06 Agents](06-agents-and-tool-use/README.md)
- **Tool poisoning** - malicious instructions hidden in a tool description that lands in your model's context. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Tool search** - retrieving the few relevant tool definitions on demand instead of loading hundreds into every request, turning tool selection into a retrieval problem. [06 Agents](06-agents-and-tool-use/README.md)
- **Top-k sampling** - keeping only the k highest-probability tokens before renormalizing and sampling. [02 LLM fundamentals](02-llm-fundamentals/README.md)
- **TPOT / ITL** - time per output token after the first, driven by memory bandwidth and batch contention. [08 Inference](08-inference-and-production/README.md)
- **Trace and span** - one request as a tree, with a span per model call, tool invocation, retrieval and guardrail check. [07 Evals](07-evaluation-and-observability/README.md)
- **Trajectory eval** - grading the path an agent took (tool choice, argument correctness, step efficiency), which diagnoses why outcomes failed. [07 Evals](07-evaluation-and-observability/README.md)
- **TTFT** - time to first token, dominated by queueing and prefill, and the number streaming UX is built around. [08 Inference](08-inference-and-production/README.md)
- **TTS** - text to speech, classically an acoustic model plus vocoder, now often a language model over neural codec tokens or a flow-matching decoder. [10 Multimodal](10-multimodal/README.md)

## V

- **VAE** - the autoencoder that compresses images into the latent space diffusion operates in, and decodes the result back to pixels. [10 Multimodal](10-multimodal/README.md)
- **Verbosity bias** - longer answers scoring higher regardless of quality, mitigated by a rubric that penalises padding and by reporting length. [07 Evals](07-evaluation-and-observability/README.md)
- **Verifiable reward** - a programmatic correctness check such as a unit test or an answer checker, which is why RL for reasoning works on maths and code. [05 Fine-tuning](05-fine-tuning-and-alignment/README.md)
- **ViT** - vision transformer, an image cut into fixed-size patches and run through a standard transformer. [10 Multimodal](10-multimodal/README.md)
- **VLA** - vision-language-action model, a VLM fine-tuned to emit robot actions (as discrete action tokens or through an action head) from camera images and an instruction. [10 Multimodal](10-multimodal/questions.md)
- **vLLM** - the most widely deployed open-source serving engine, home of PagedAttention and continuous batching. [08 Inference](08-inference-and-production/README.md)
- **VLM** - vision-language model, a vision encoder plus a projector plus an LLM that treats patch embeddings as ordinary tokens. [10 Multimodal](10-multimodal/README.md)

## W

- **Warmup** - the short linear learning-rate ramp that stops deep transformers diverging while Adam's second-moment estimate is still unreliable. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **Weight decay** - shrinking weights toward zero, applied directly to the weights in AdamW rather than through the gradient. [01 ML foundations](01-ml-and-dl-foundations/README.md)
- **WER** - word error rate, the standard accuracy metric for speech recognition. [10 Multimodal](10-multimodal/README.md)
- **Workflow** - LLMs and tools orchestrated through predefined code paths, which is what you should build whenever you can draw the flowchart. [06 Agents](06-agents-and-tool-use/questions.md)

## Y

- **YaRN** - context extension that interpolates RoPE frequency bands unevenly, preserving local resolution with much less fine-tuning. [02 LLM fundamentals](02-llm-fundamentals/README.md)

## Z

- **ZDR** - zero data retention, a contract term removing even the vendor's short abuse-monitoring retention window. [09 Safety](09-safety-security-and-responsible-ai/README.md)
- **Zero-shot** - asking the model to do the task with instructions only, no examples, which works well on instruction-tuned models. [03 Prompting](03-prompt-engineering-and-context/README.md)

---

## Where to go next

| If you want | Go to |
|---|---|
| The 75 highest-signal items in checkbox form | [AI-ENGINEER-75.md](AI-ENGINEER-75.md) |
| One evening of revision before the interview | [CHEATSHEET.md](CHEATSHEET.md) |
| A structured 1, 4 or 8-week plan | [STUDY_PLAN.md](STUDY_PLAN.md) |
| Questions and loop maps for a specific company | [14-company-interview-questions](14-company-interview-questions/README.md) |
| A study map calibrated to your job title | [15-role-guides](15-role-guides/README.md) |
| Papers, courses and blogs worth the time | [resources](resources/README.md) |

Missing a term? Corrections and additions are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).
