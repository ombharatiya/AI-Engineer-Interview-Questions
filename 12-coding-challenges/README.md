# 🧑‍💻 Coding Challenges

Almost every AI engineer loop now includes an "implement it from scratch" round. Interviewers use these to separate people who have *used* transformers, RAG, and agents from people who *understand* them - you can't fake your way through a causal mask or a numerically stable softmax with API knowledge. Frontier labs and serious AI startups routinely ask for attention, tokenizers, sampling, and KV caches in plain numpy; product-focused teams lean on the RAG, agent-loop, and streaming-parser variants.

## Rules of the game

- **Dependencies:** `numpy` + Python stdlib only. No PyTorch, no transformers, no framework crutches. That's the point.
- **Self-contained:** every file runs standalone with `python3 <file>.py` and finishes with `All tests passed.`
- **Structure:** each file has a `PROBLEM` statement (what you'd be asked, with exact signatures), `INTERVIEW NOTES` (what strong solutions demonstrate, common mistakes, follow-up variations), a clean reference solution, and assert-based tests.

**How to practise:** read only the docstring, close the file, implement it yourself under time pressure (30-45 min is typical), then run the tests and diff against the reference. Being able to *talk while coding* - naming the stability trick, the complexity, the failure mode - is what actually gets scored.

## The challenges

| # | File | Difficulty | Concepts tested | What interviewers look for |
|---|------|------------|-----------------|----------------------------|
| 01 | [01_attention.py](01_attention.py) | Medium | Scaled dot-product attention, multi-head, causal masking | Stable softmax, mask as −inf *before* softmax, √d_k scaling, head split via reshape/transpose not loops |
| 02 | [02_bpe_tokenizer.py](02_bpe_tokenizer.py) | Medium | Byte-level BPE: train, encode, decode | Merge-rank order at encode time, byte-level round-trip on any unicode, deterministic tie-breaking |
| 03 | [03_sampling.py](03_sampling.py) | Easy | Temperature, top-k, top-p, min-p, repetition penalty | Correct order of operations, filtering with −inf then renormalizing, edge cases (T→0, p=1, k=1) |
| 04 | [04_positional_encodings.py](04_positional_encodings.py) | Medium | Sinusoidal PE, RoPE | Why RoPE encodes *relative* position, rotation preserving norms, frequency spectrum intuition |
| 05 | [05_layernorm_and_softmax.py](05_layernorm_and_softmax.py) | Easy | Stable softmax/log-softmax, LayerNorm, RMSNorm | Max-subtraction trick, eps placement, what RMSNorm drops and why it's cheaper |
| 06 | [06_kv_cache.py](06_kv_cache.py) | Medium | Autoregressive decode loop with vs. without KV cache | O(T²)→O(T) per-step attention cost, exact output equivalence, cache memory accounting |
| 07 | [07_mini_gpt_forward.py](07_mini_gpt_forward.py) | Hard | Full GPT block forward pass: embeddings → attention → MLP → logits | Pre-norm residual wiring, correct shapes end-to-end, weight tying, where the FLOPs live |
| 08 | [08_semantic_search_rag.py](08_semantic_search_rag.py) | Medium | Embed, index, cosine retrieval, context assembly (mini-RAG) | Vector normalization, top-k retrieval correctness, token-budgeted context packing |
| 09 | [09_text_chunking.py](09_text_chunking.py) | Easy | Fixed, sliding-window, recursive, sentence chunkers | Overlap handling, boundary preservation, no dropped/duplicated text at edges |
| 10 | [10_agent_loop.py](10_agent_loop.py) | Medium | Tool-calling agent loop with a mock LLM | Clean state machine, tool-result feedback into context, max-iteration and error handling |
| 11 | [11_rate_limiter_and_retry.py](11_rate_limiter_and_retry.py) | Medium | Token bucket, exponential backoff with jitter | Burst vs. sustained rate reasoning, why jitter prevents thundering herd, retry budget caps |
| 12 | [12_eval_metrics.py](12_eval_metrics.py) | Medium | pass@k unbiased estimator, QA F1/EM, judge harness skeleton | Why the naive pass@k estimator is biased, token-level F1 details, judge calibration hooks |
| 13 | [13_streaming_parser.py](13_streaming_parser.py) | Hard | SSE parser, incremental tool-call argument assembly | Handling chunks split mid-event/mid-JSON, buffering discipline, partial-parse recovery |

## Running

```bash
python3 12-coding-challenges/01_attention.py
# ...
# All tests passed.
```

The only dependency is numpy (`pip install numpy`).
