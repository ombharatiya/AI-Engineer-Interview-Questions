# The night-before cheat sheet

Read this in one 60-90 minute pass the evening before an interview. It is not a substitute for the full topic material, it is what to have loaded in working memory. Each section links back to its deep dive.

---

## 🧠 ML & Deep Learning Foundations

- Bias-variance: high bias underfits (add capacity, features), high variance overfits (regularize, more data, simpler model).
- Cross-entropy is the right classification loss because it's the maximum-likelihood objective for a categorical distribution, and its gradient is `predicted - actual`, clean and well-scaled.
- AdamW, not Adam: decouples weight decay from the gradient update, which matters at transformer scale.
- LayerNorm normalizes across the feature dimension per token, so it works with variable sequence lengths and small batches, unlike BatchNorm.
- Precision/recall trade off; accuracy lies on imbalanced data. ROC-AUC can look fine while PR-AUC exposes a weak positive class.
- Cosine similarity, not Euclidean distance, is standard for embeddings, since it ignores magnitude and compares direction.
- Data leakage is the silent killer of eval numbers: check for it before trusting any surprising result.
→ Deep dive: [01-ml-and-dl-foundations](01-ml-and-dl-foundations/)

## 🧠 LLM & Transformer Fundamentals

- Attention: `softmax(QKᵀ/√d_k)V`. The `√d_k` scaling keeps logit variance near 1, preventing softmax saturation and vanishing gradients.
- GQA (grouped-query attention) is the modern default: multiple query heads share a KV head, cutting KV cache size roughly proportionally, near-MHA quality.
- KV cache size per token = `2 × n_layers × n_kv_heads × head_dim × bytes_per_elem`. Long-context serving is a memory problem, not a FLOPs problem.
- RoPE encodes relative position by rotating Q/K vectors; it generalizes to longer contexts better than learned absolute embeddings.
- Tokenization (BPE) explains the classic failures: character counting, arithmetic, multilingual token inefficiency.
- Chinchilla: compute-optimal training balances model size and data roughly 1:1 in scaling terms, but production models today train far past that point because inference cost, not training cost, dominates total cost of ownership.
- MoE: total params vs. active params per token. A large total parameter count with a small active count buys capacity without paying full inference cost, at the cost of training instability and full-weight memory footprint.
- Reasoning models spend extra test-time compute (longer chains of thought, often RL-trained) for higher accuracy on hard problems, at higher latency and cost. Use them selectively.
→ Deep dive: [02-llm-fundamentals](02-llm-fundamentals/)

## 🧭 Prompt Engineering & Context Engineering

- Chain-of-thought helps on multi-step reasoning; it's wasted latency on simple lookups, and reasoning models already do it internally.
- Structured output via constrained decoding enforces a grammar at the logit level, it masks invalid tokens rather than hoping the model complies.
- Prompt caching rewards a stable prefix: put fixed instructions first, volatile content (user input, retrieved docs) last.
- "Lost in the middle": put critical instructions at both the start and the end of a long context, not buried in the middle.
- Context engineering is the 2025+ reframing of prompting: you're managing the whole window, tools, retrieved docs, memory, history, not just a string.
→ Deep dive: [03-prompt-engineering-and-context](03-prompt-engineering-and-context/)

## 🔎 RAG & Retrieval

- Decision framework: RAG for fresh or private knowledge, fine-tuning for behavior/format/style, long-context when the corpus is small and static enough to just stuff in.
- Hybrid search (BM25 + dense, fused with reciprocal rank fusion) beats pure semantic search when queries include IDs, jargon, or exact terms.
- Rerank with a cross-encoder after a wide initial retrieval, a typical pattern is retrieve top-50, rerank down to top-5.
- Metadata filtering has to happen at the ANN layer, not after, a post-filter on top-k results can filter away everything relevant.
- Contextual retrieval (prepending chunk-level context before embedding) meaningfully improves retrieval on chunked documents.
- When debugging a bad RAG answer, triage first: is this a retrieval miss (wrong chunks returned) or a generation miss (right chunks, model didn't use them)? The fix is different for each.
- Authorization must be enforced at the retrieval layer with metadata filters, never left to the model to "decide" what a user shouldn't see.
→ Deep dive: [04-rag-and-retrieval](04-rag-and-retrieval/)

## 🎛️ Fine-tuning, RLHF & Alignment

- Escalation path: prompting → RAG → fine-tuning. Don't fine-tune to inject facts, that's RAG's job; fine-tune for consistent style, structured output, or latency/cost wins.
- LoRA: `W' = W + (α/r)BA`, rank `r` typically 8-64, trainable params drop to roughly 0.1-1% of the base model.
- QLoRA: 4-bit NF4 base quantization + double quantization + paged optimizers, fine-tunes a 65-70B model on a single 48 GB GPU with modest quality loss.
- Full fine-tuning with Adam in mixed precision costs roughly 16 bytes/param (2 bf16 weights + 2 grads + 4 fp32 master weights + 8 fp32 Adam states), a 7B model needs roughly 112 GB before activations.
- DPO's insight: skip the separate reward model and the RL loop, optimize directly on preference pairs using an implicit reward derived from the policy itself.
- GRPO and RL-for-reasoning work well on math and code specifically because those domains have cheap, verifiable rewards (does the test pass, is the answer correct).
- Catastrophic forgetting: mitigate with lower learning rate, fewer epochs, LoRA over full fine-tuning, and mixing general instruction data back into the task-specific set.
→ Deep dive: [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/)

## 🤖 Agents, Tool Use & MCP

- An agent is the LLM directing its own loop (deciding what to do next); a workflow is a fixed sequence with the LLM as one step. Don't build an agent when a workflow suffices.
- MCP solves N×M integration sprawl: one protocol between any host and any tool server, with tools, resources, and prompts as primitives.
- Design tools the way you'd design a good API: few, well-named, with error messages the model can actually act on. Token-expensive tool outputs are a real cost.
- The lethal trifecta: private data access + exposure to untrusted content + an exfiltration channel. Remove any one leg and the agent stops being exploitable by design, not by hoping the model refuses.
- Reliability compounds multiplicatively across steps: 0.95 per-step success over 20 steps is roughly 0.36 end to end. This is why long-horizon agents need checkpointing and self-correction, not just a good single-step model.
- Multi-agent architectures help for parallel, read-heavy work (research, search); they hurt for write-heavy, shared-state work where coordination overhead dominates.
- Irreversible actions need a human approval gate. Model confidence is not authorization.
→ Deep dive: [06-agents-and-tool-use](06-agents-and-tool-use/)

## 🧪 Evals & Observability

- Evals are the engineering artifact that makes iteration safe. Treat eval-set changes with the same rigor as code changes: version them, run them in CI, gate deploys on them.
- LLM-as-judge: pairwise comparison is more reliable than pointwise scoring. Known biases: position bias (swap order and average), verbosity bias, self-preference (use a different model family as judge when possible).
- pass@k unbiased estimator (Chen et al., Codex paper): generate `n ≥ k` samples, count `c` correct, `pass@k = 1 - C(n-c, k) / C(n, k)`. Naively sampling exactly k is high-variance.
- pass^k (all k trials succeed) punishes inconsistency that pass@k hides, closer to what matters for agent reliability.
- Public benchmarks saturate and leak into training data. Treat leaderboard position as a weak, contaminated signal, not ground truth for your use case.
- RAG evals split cleanly: retrieval metrics (recall@k, MRR, nDCG) vs. generation metrics (faithfulness, answer relevance). Measure both separately to triage failures.
- Start an eval set with 20-50 genuinely hard, real examples sourced from production failures, not hundreds of easy synthetic ones.
→ Deep dive: [07-evaluation-and-observability](07-evaluation-and-observability/)

## ⚡ Inference, Serving & Production LLM Systems

- Prefill is compute-bound (parallel over the prompt); decode is memory-bandwidth-bound (sequential, one token at a time). This asymmetry drives almost every serving decision.
- TTFT (time to first token) is dominated by queueing and prefill; TPOT/ITL (time per output token) is dominated by memory bandwidth and batch contention. Total latency ≈ TTFT + TPOT × output_tokens.
- PagedAttention (vLLM) manages the KV cache like virtual memory in fixed-size blocks, eliminating fragmentation and enabling much higher batch sizes.
- Continuous batching lets requests join and leave a batch per decode step instead of waiting for the whole batch to finish, the single biggest throughput win in modern serving.
- Speculative decoding uses a small draft model to propose tokens a large model verifies in parallel, it speeds up decode without changing the output distribution.
- Report goodput (throughput within your latency SLO), not raw throughput. 10K tokens/sec at 30-second TTFT is worthless for a chat product.
- Prompt caching and batch APIs are the two biggest cost levers available with zero quality tradeoff, use them before reaching for a smaller model.
→ Deep dive: [08-inference-and-production](08-inference-and-production/)

## 🛡️ Safety, Security & Responsible AI

- Prompt injection is unsolved because the context window has no privilege separation between instructions and data. Defend with defense-in-depth, not a single filter: input/output classifiers, least-privilege tools, human approval for irreversible actions, and treating every model output as untrusted.
- Indirect injection (via a retrieved document, email, or tool result) is more dangerous than direct injection because the victim never sees the attack.
- Jailbreaks attack the model's trained behavior; prompt injection attacks the application. Different attacker, different fix, different owner.
- Assume the system prompt leaks. Never put secrets or unenforced authorization logic in it.
- Safetensors over pickle for model weights, pickle deserialization can execute arbitrary code on load.
- OWASP Top 10 for LLM Applications is the shared vocabulary interviewers expect: prioritize the categories that matter for the system in front of you, don't just recite the list.
→ Deep dive: [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/)

## 🖼️ Multimodal Models

- Vision-language models tokenize images into patches via a vision encoder (ViT-style), project them into the LLM's embedding space, then process them as ordinary tokens, more tokens per image, more cost.
- CLIP's contrastive image-text pretraining is why zero-shot classification and cross-modal retrieval work at all: it aligns image and text embeddings in a shared space.
- Diffusion models generate by iterative denoising; latent diffusion does this in a compressed latent space rather than pixel space, which is why it's tractable.
- VLMs are weak at precise counting, fine spatial reasoning, and dense OCR relative to dedicated pipelines, know when to reach for traditional OCR instead.
- Native speech-to-speech models beat the STT→LLM→TTS pipeline on latency and naturalness, but the pipeline is easier to control, debug, and swap components in.
→ Deep dive: [10-multimodal](10-multimodal/)

## 🏗️ AI System Design

- The model is a component, not the whole system. Spend your time on data/context strategy, evaluation, and failure modes, not on redesigning the transformer.
- Always state success metrics and a rough cost-per-request estimate out loud, interviewers grade for cost and eval awareness as much as architecture.
- Have a fallback and a degradation path for every external model call: retries, timeouts, a cheaper model, or a static response, never a bare unhandled failure.
→ Deep dive: [11-ai-system-design](11-ai-system-design/)

## 🧑‍💻 Coding Challenges

- Implement attention, sampling, and the KV cache loop by hand at least once. The interview is a blank editor, not a multiple-choice quiz.
- Numerical stability matters: subtract the max before softmax, use log-space where you can, these are the details that separate a working solution from a correct-looking one that overflows on real inputs.
→ Deep dive: [12-coding-challenges](12-coding-challenges/)

---

## 🔢 Numbers and formulas to know cold

| Concept | Formula / value |
|---|---|
| Attention | `softmax(QKᵀ/√d_k)V`, scaling keeps logit variance ≈ 1 |
| KV cache size per token | `2 × n_layers × n_kv_heads × head_dim × bytes_per_elem` |
| LoRA update | `W' = W + (α/r)BA`, typical rank `r` = 8-64 |
| Full fine-tuning memory (Adam, mixed precision) | ≈ 16 bytes/param (2 weights + 2 grads + 4 fp32 master + 8 Adam states) |
| pass@k (unbiased estimator) | `1 - C(n-c, k) / C(n, k)` for `n` samples, `c` correct |
| TTFT | Time to first token: queueing + prefill |
| TPOT / ITL | Time per output token after the first: memory-bandwidth-bound |
| Total latency | `TTFT + TPOT × output_tokens` |
| Rerank pattern | Retrieve top-50 (cheap, wide) → rerank to top-5 (expensive, precise) |
| Agent reliability | `p^n` compounding: 0.95 per step over 20 steps ≈ 0.36 end to end |

## ❓ 25 questions you're most likely to be asked

1. Explain self-attention and why we divide by √d_k. → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
2. What's the difference between MQA, GQA, and MHA, and why does it matter for serving? → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
3. Walk me through how BPE tokenization works, and what problems it causes. → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
4. What is the KV cache, and how do you estimate its memory footprint? → [02-llm-fundamentals](02-llm-fundamentals/questions.md)
5. When would you use RAG versus fine-tuning versus a longer context window? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
6. How do you chunk documents for retrieval, and what determines chunk size? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
7. What's the difference between a bi-encoder and a cross-encoder, and where does reranking fit? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
8. How would you debug a RAG system that's giving wrong answers? → [04-rag-and-retrieval](04-rag-and-retrieval/questions.md)
9. Explain LoRA, and why it reduces memory during fine-tuning. → [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/questions.md)
10. What's the core idea behind DPO, and how does it differ from PPO-based RLHF? → [05-fine-tuning-and-alignment](05-fine-tuning-and-alignment/questions.md)
11. What's the difference between a workflow and an agent, and when should you not build an agent? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
12. How does MCP work, and what problem does it actually solve? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
13. How would you design the tool permission model for an agent with write access? → [06-agents-and-tool-use](06-agents-and-tool-use/questions.md)
14. What's the lethal trifecta, and how do you design around it? → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
15. How do you build and maintain an eval set for an LLM feature? → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
16. What are the known biases in LLM-as-judge evaluation, and how do you mitigate them? → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
17. Derive or explain the unbiased pass@k estimator. → [07-evaluation-and-observability](07-evaluation-and-observability/questions.md)
18. Why is decode memory-bandwidth-bound while prefill is compute-bound? → [08-inference-and-production](08-inference-and-production/questions.md)
19. Explain continuous batching and why it beats static batching. → [08-inference-and-production](08-inference-and-production/questions.md)
20. How does speculative decoding speed up generation without changing output quality? → [08-inference-and-production](08-inference-and-production/questions.md)
21. Is prompt injection solved? How do you defend against it? → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
22. Walk through the OWASP Top 10 for LLM applications for a system of your choice. → [09-safety-security-and-responsible-ai](09-safety-security-and-responsible-ai/questions.md)
23. Design a RAG assistant over a company's internal wikis and tickets, with access control. → [11-ai-system-design](11-ai-system-design/case-studies/01-enterprise-rag-assistant.md)
24. Design a customer support agent that can take real actions like issuing refunds. → [11-ai-system-design](11-ai-system-design/case-studies/03-customer-support-agent.md)
25. Walk me through an LLM feature you shipped end to end, and how you evaluated it. → [13-interview-process-and-behavioral](13-interview-process-and-behavioral/questions.md)

## 🗣 Phrases that make you sound senior

- "Evals are the moat here, not the prompt." Framing evaluation as the durable engineering artifact, not an afterthought.
- "Is this a retrieval miss or a generation miss?" The first question in any RAG debugging session.
- "What's the failure mode if the provider is down for ten minutes?" Thinking about degradation before being asked.
- "That's a cost decision as much as a technical one." Naming the token-cost tradeoff explicitly instead of treating quality as free.
- "The context window has no privilege separation." The one sentence that explains why prompt injection is architecturally hard, not a prompting bug.
- "Let's remove a leg of the trifecta." Turning an agent security concern into a concrete design change.
- "Prefill is compute-bound, decode is memory-bandwidth-bound." The sentence that tells an interviewer you've actually operated a serving stack.
- "We'd want a golden set before touching the prompt again." Refusing to iterate blind.
- "What's the reversibility of this action?" The question that separates auto-execute from human-approval-gated agent actions.
- "Pass@k versus pass^k, depending on whether best-case or reliability is what we're optimizing for." Precision about what a metric actually measures.
