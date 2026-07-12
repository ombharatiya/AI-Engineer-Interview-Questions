# LLM & Transformer Fundamentals - Interview Questions

41 questions: 13 basic, 16 intermediate, 12 advanced.

## Basic

### 1. Why did transformers replace RNNs and LSTMs for language modeling?

<details><summary><b>Answer</b></summary>

Two reasons: parallelism and gradient paths. RNNs process tokens sequentially - hidden state t depends on t−1 - so training can't parallelize across the sequence dimension, and information from early tokens must survive hundreds of recurrent steps, where it degrades even with LSTM gating. Transformers compute attention over all positions simultaneously: one matrix multiply processes the whole sequence, so training saturates GPUs/TPUs, and any token can attend to any other token through a path of length one, so long-range dependencies don't decay through recurrence.

The parallelism point is the economically decisive one. Next-token prediction with a causal mask gives you a training signal at *every* position of a sequence from a single forward pass - an n-token document yields n loss terms computed in parallel. That efficiency is what made training on trillions of tokens feasible, which is what made scaling laws discoverable, which is what produced modern LLMs.

Worth noting the honest tradeoffs: RNNs have O(1) state per step at inference, while transformers pay O(n²) attention compute and an O(n) KV cache that grows with context. That's why there's active work on state-space models (Mamba-style architectures) and hybrid designs - they revisit the recurrent idea with parallelizable training. But for training-time throughput and quality at scale, attention won, and everything at the frontier today is transformer-based or transformer-hybrid.

A good answer also mentions that self-attention is permutation-invariant, so transformers need explicit positional information (RoPE etc.) - the sequential order RNNs got for free has to be injected.

**Follow-ups:** What's the inference-time cost transformers pay that RNNs don't? Why does causal masking make training so sample-efficient per forward pass? What are state-space models trying to recover?

</details>

### 2. Walk me through what happens inside a single transformer decoder block.

<details><summary><b>Answer</b></summary>

A decoder block takes hidden states of shape (n_tokens × d_model) and applies two sublayers, each wrapped in a residual connection with a normalization:

1. **Norm → masked self-attention → add.** The input is normalized (RMSNorm in modern models), then projected into queries, keys, and values. Scaled dot-product attention with a causal mask mixes information *across positions* - each token gathers a weighted summary of earlier tokens. The result goes through an output projection and is *added* to the original input (residual).
2. **Norm → MLP → add.** The updated stream is normalized again and passed through a position-wise feed-forward network - typically up-project to ~3-4× d_model, nonlinearity (SwiGLU in Llama-family models), down-project - applied identically and independently at every position. Added back to the residual stream.

So the division of labour is: **attention moves information between tokens; the MLP transforms information at each token** (it's where most parameters and, plausibly, most stored "knowledge" live). The residual stream acts as a shared workspace that each sublayer reads from and writes small updates into - a framing that explains why you can stack 100+ blocks: the identity path means each block only needs to make an incremental refinement.

Placement of the norm matters: modern models are **pre-norm** (norm inside the residual branch), which keeps the residual path clean and training stable at depth; the 2017 original was post-norm. In a real model each attention sublayer also applies RoPE to Q and K, and the block repeats N times (e.g. 32 blocks for a 7-8B model, 80 for a 70B), followed by a final norm and the LM head projecting to vocabulary logits.

**Follow-ups:** Roughly what fraction of a block's parameters are in the MLP vs attention? Why do residual connections matter more as depth grows? What changes in this picture for an MoE model?

</details>

### 3. Explain self-attention step by step. What exactly are Q, K, and V?

<details><summary><b>Answer</b></summary>

Every token's vector is linearly projected three ways: a **query** ("what am I looking for?"), a **key** ("what do I contain, for others to match against?"), and a **value** ("what content do I contribute if attended to?"). Attention is a soft, differentiable key-value lookup: token i's query is compared to every token's key; the resulting weights mix the values.

Steps, for X of shape (n, d_model):

1. Q = XW_q, K = XW_k, V = XW_v - three learned projections.
2. Scores = QKᵀ / √d_k - an (n, n) matrix; entry (i, j) is how relevant token j is to token i.
3. Apply the causal mask: set scores where j > i to −∞.
4. Row-wise softmax → each row becomes a probability distribution over previous positions.
5. Output = weights · V - each token's output is a convex combination of value vectors, then a final output projection W_o maps back to d_model.

```python
import numpy as np
def attention(Q, K, V, causal=True):
    s = Q @ K.T / np.sqrt(K.shape[-1])
    if causal:
        s[np.triu(np.ones_like(s, dtype=bool), k=1)] = -np.inf
    w = np.exp(s - s.max(-1, keepdims=True))
    w /= w.sum(-1, keepdims=True)
    return w @ V
```

The crucial conceptual point: the weights are **computed from the data at runtime**, not fixed like convolution kernels. The same layer can route "pronoun → antecedent" in one sentence and "verb → subject" in another. Why separate K and V? Because what makes a token *findable* (key) and what it should *deliver* once found (value) are different roles - collapsing them forces one vector to serve both, which is measurably worse.

**Follow-ups:** Why divide by √d_k? What is the computational complexity of step 2 and what does that imply for long contexts? In a decoder generating token-by-token, which of Q, K, V get cached and why?

</details>

### 4. Why does scaled dot-product attention divide by √d_k?

<details><summary><b>Answer</b></summary>

To keep the softmax from saturating. If the components of q and k are roughly independent with zero mean and unit variance, their dot product q·k is a sum of d_k terms and has variance ≈ d_k - so the standard deviation of the logits grows like √d_k. With d_k = 128, unscaled logits routinely reach magnitudes of ±20 or more.

Softmax of large-magnitude logits collapses to nearly one-hot: one attention weight ≈ 1, the rest ≈ 0. In that regime the softmax's Jacobian is nearly zero (the gradient of softmax involves p·(1−p) terms, which vanish as p → 0 or 1), so almost no gradient flows back through the attention scores. Early in training that means the attention layers barely learn; it can also cause loss spikes and instability. Dividing by √d_k renormalizes the logit variance back to ~1 regardless of head dimension, keeping the softmax in a regime with usable gradients and appropriately soft attention distributions.

Two points that distinguish a strong answer:

- It's a **variance argument about initialization/training dynamics**, not a mathematical requirement - the model could in principle learn scaled-down projections, but starting saturated makes optimisation much harder.
- The same idea shows up elsewhere: logit **soft-capping** in some models (bounding attention or final logits with tanh) and **QK-norm** (applying LayerNorm/RMSNorm to queries and keys before the dot product, used in several modern architectures) attack the same failure mode - attention logits growing without bound during training - more aggressively than the static √d_k scale.

A concrete way to phrase the intuition: √d_k scaling makes the temperature of the attention softmax independent of head size, so architecture choices about head_dim don't silently change how peaked attention is.

**Follow-ups:** What is QK-norm and why did some recent models adopt it? What happens to gradients when softmax saturates - walk me through the Jacobian? Would you expect scaling issues to be worse with larger or smaller head dimensions?

</details>

### 5. What is causal masking, why is it needed, and how is it implemented?

<details><summary><b>Answer</b></summary>

Causal masking prevents position i from attending to positions j > i, enforcing that predictions depend only on the past. It's needed for two linked reasons. First, at inference time future tokens don't exist - the model must generate left to right, so training must match that conditional structure. Second, and more subtly, it's what makes causal LM training efficient and non-degenerate: with a causal mask, one forward pass over an n-token sequence produces n valid next-token predictions trained in parallel. Without the mask, predicting token t+1 while attending to token t+1 is trivial copying - the model would learn nothing.

Implementation: before the softmax, add a mask matrix that is 0 on and below the diagonal and −∞ (in practice a large negative number like −1e9, or dtype min) strictly above it. After softmax, those positions get exactly zero weight, and the renormalization happens automatically because softmax normalizes over the remaining finite entries.

```python
mask = np.triu(np.ones((n, n), dtype=bool), k=1)   # True above diagonal
scores = np.where(mask, -1e9, scores)               # before softmax
```

In production kernels (FlashAttention), the mask is never materialised as an n×n tensor - the kernel simply skips computing blocks that are entirely masked, which also halves the work since roughly half the score matrix is masked out.

Details worth volunteering: encoder models (BERT) deliberately omit the mask - they trade generation ability for bidirectional context. Prefix-LM setups mask causally only over the generated portion while allowing bidirectional attention over the prompt. And during batched inference you additionally need *padding* masks so tokens don't attend to padding - a distinct mask that beginners often conflate with the causal one.

**Follow-ups:** Why does the mask go before the softmax rather than after? What's a prefix LM and when is bidirectional prompt attention useful? How does FlashAttention exploit the causal structure for speed?

</details>

### 6. Why does the transformer use multiple attention heads instead of one large one?

<details><summary><b>Answer</b></summary>

Because a single softmax produces a single weighting over positions per token - one "view" of the context. A token often needs several different relations resolved simultaneously: which noun does this pronoun refer to, what's the syntactic head of this phrase, what came just before me, which delimiter opened this bracket. Averaging those into one attention distribution destroys information. Multi-head attention runs h independent attention operations in parallel subspaces so each can specialise.

Mechanically: instead of one attention over d_model-dimensional Q/K/V, split into h heads of dimension d_model/h (e.g. 4096 → 32 heads × 128). Each head gets its own learned Q/K/V projections into its subspace, computes attention independently, and the h outputs are concatenated and mixed by the output projection W_o. Total parameter count and FLOPs are approximately the same as one full-width head - you're partitioning the computation, not adding to it. What you gain is h independent softmaxes; what each head loses is representational width (a 128-dim dot product is a lower-rank similarity measure than a 4096-dim one).

Empirically, interpretability work has found heads with recognisable roles - previous-token heads, positional heads, and famously **induction heads** (pairs of heads implementing "find the previous occurrence of this token and copy what followed it"), which are central to in-context learning. It's also empirically true that many heads are redundant after training - head-pruning studies showed you can remove a substantial fraction with modest quality loss - which is part of the intuition for why sharing K/V across query heads (MQA/GQA) works.

Head count is a tuned hyperparameter: too few heads underfits the diversity of relations; too many makes each head's subspace too narrow. head_dim between 64 and 128 has been a stable sweet spot across model generations.

**Follow-ups:** What is an induction head and why does it matter for in-context learning? If many heads are redundant, what architectural optimisations does that motivate? Does multi-head attention cost more FLOPs than single-head at equal d_model?

</details>

### 7. Compare encoder-only, decoder-only, and encoder-decoder architectures. What is each used for?

<details><summary><b>Answer</b></summary>

**Encoder-only** (BERT lineage): bidirectional self-attention - every token sees the whole sequence - trained with masked-LM. Produces rich contextual representations but has no natural generation mechanism. Today it survives where representation quality per FLOP matters: embedding models for retrieval, rerankers, classifiers, PII/toxicity filters. Small, fast, cheap to serve.

**Decoder-only** (GPT, Llama, Claude, Gemini): causal self-attention, trained on next-token prediction. This is the architecture of essentially every modern general-purpose LLM. Why it won: (1) generation is native; (2) every token position provides training signal in each pass, so it's data-efficient at scale; (3) one architecture and one objective handle every task via prompting - no task-specific heads; (4) it scales cleanly, and the entire tooling ecosystem (KV caching, serving stacks, RLHF pipelines) is built around it.

**Encoder-decoder** (original transformer, T5, Whisper, many translation models): the encoder reads the input with bidirectional attention; the decoder generates autoregressively while cross-attending to encoder outputs. Strongest fit when there's a clear input→output transform with a fixed input: translation, speech-to-text, structured summarisation. The bidirectional encode of the source is a genuine advantage there. Drawbacks for general chat: the input/output split is awkward for multi-turn conversation, and you can't incrementally extend "the input" the way a decoder-only model just appends to context.

A nuance worth adding: decoder-only models can emulate the encoder-decoder pattern - the prompt plays the role of the encoded input - and prefix-LM variants allow bidirectional attention over the prompt while generating causally. In practice the industry consolidated on decoder-only for generative workloads and encoder-only for embeddings/reranking, with encoder-decoder holding niches like ASR (Whisper) and translation.

**Follow-ups:** Why do embedding models still use bidirectional attention? What's a prefix LM? If you were building a translation system today, would you pick encoder-decoder or a decoder-only LLM, and on what criteria?

</details>

### 8. What's the difference between causal language modeling and masked language modeling as pretraining objectives?

<details><summary><b>Answer</b></summary>

**Causal LM (CLM)**: predict token t+1 given tokens 1..t, at every position, with attention causally masked. The loss is cross-entropy summed over all positions - an n-token sequence yields n prediction problems per forward pass, and 100% of tokens contribute signal.

**Masked LM (MLM)**: corrupt the input by masking a subset of tokens (BERT masked ~15%) and predict the originals using *bidirectional* context. Only the masked positions produce loss, so per forward pass you get signal from ~15% of tokens.

Implications:

- **Generation**: CLM models generate natively - sampling from the model *is* the objective's inference mode. MLM models can't generate coherently; there's no left-to-right factorization of the joint distribution.
- **Representation quality**: MLM sees both sides of every position, which historically gave better representations per parameter for understanding tasks - why BERT dominated classification benchmarks in 2019-2020 and why embedding models still favour bidirectional attention.
- **Scaling and universality**: CLM turned out to be the objective that scales into general-purpose capability. Next-token prediction over diverse data implicitly requires syntax, world knowledge, reasoning, and style - and in-context learning falls out of it. The 15%-signal inefficiency of MLM plus its lack of a generative mode made it a dead end for frontier-scale general models.
- **Train/inference mismatch**: MLM's [MASK] token never appears at inference - a distribution shift BERT-era papers worked around; CLM has no such mismatch (though it has *exposure bias*: training always conditions on ground-truth prefixes, inference conditions on its own possibly-erroneous outputs).

Also worth knowing: T5-style **span corruption** is an encoder-decoder middle ground (mask contiguous spans, generate them), and some diffusion-style text models revisit non-autoregressive objectives, but CLM remains the backbone of every frontier model.

**Follow-ups:** What is exposure bias and how much does it matter in practice? Why does in-context learning emerge from next-token prediction? When would you still pretrain or fine-tune with MLM today?

</details>

### 9. Why do LLMs use subword tokenization instead of whole words or raw characters?

<details><summary><b>Answer</b></summary>

It's a compression/coverage tradeoff, and subwords are the sweet spot between two bad extremes.

**Word-level** fails on coverage: natural language has an unbounded vocabulary (names, typos, morphology, code identifiers, other languages). You either carry a vocabulary of millions - an enormous embedding matrix and softmax - or you map everything unseen to an `<UNK>` token and lose information. Morphologically rich languages make this catastrophic.

**Character-level** (or raw bytes) has perfect coverage but terrible compression: sequences get ~4-5× longer than subword tokenization in English, and attention cost is quadratic in sequence length - so you pay a large constant factor in compute and effective context. Each character also carries almost no meaning by itself, so the model burns capacity reassembling words before it can do anything else.

**Subword tokenization** (BPE and relatives) learns a vocabulary of frequent chunks: common words become single tokens, rare words decompose into meaningful pieces ("tokenization" → "token" + "ization"), and with a byte-level base alphabet *any* string is representable - no OOV ever. You get sequences ~4× shorter than character-level with a vocabulary of manageable size (32k - 200k), and frequent tokens get well-trained embeddings.

The interview-worthy caveat: this efficiency is bought by hiding the character level from the model - which causes the classic failures (letter counting, spelling games, some arithmetic) - and compression quality varies wildly by language, so non-English text is often 2-4× more tokens for the same content, meaning higher cost and less usable context. Tokenization is one of the few remaining hand-engineered, non-learned stages of the pipeline, and there's ongoing research on byte-level models with learned patching (e.g. the Byte Latent Transformer line) aimed at removing it.

**Follow-ups:** How does byte-level BPE guarantee no out-of-vocabulary strings? What's the effect of tokenizer choice on multilingual pricing and quality? Why hasn't character/byte-level modeling replaced BPE yet?

</details>

### 10. Why do LLMs famously miscount the number of r's in "strawberry"?

<details><summary><b>Answer</b></summary>

Because the model never sees letters. The tokenizer maps "strawberry" to one or two token IDs (e.g. "str" + "awberry", or a single token), and the model receives only those IDs' embedding vectors. There is no character-level view anywhere in the forward pass - asking it to count r's is like asking someone to count the letters in a word they've only ever heard spoken. To answer correctly, the model must have *memorised* the spelling of that specific token from training data (e.g. from spelling lists or character-separated text), then perform counting - a two-step process where both steps are unreliable.

Counting itself is the second failure: transformers perform a fixed number of layers of parallel computation per token, and counting is an inherently sequential operation. Without externalising intermediate steps into generated tokens (chain of thought like "s-t-r-a-w-b-e-r-r-y: r appears at positions 3, 8, 9 → 3"), the model attempts the count "in its head" in one shot, where it's guessing from memorised associations. This is why the same model that fails the direct question usually succeeds if you ask it to spell the word letter-by-letter first - and why reasoning models, which are trained to externalise steps, largely fixed this class of error.

The general lesson interviewers want: **this is a tokenization artifact, not evidence about intelligence**. The same root cause explains poor performance on rhyming and wordplay, string reversal, base64-ish character manipulation, and off-by-one behaviours in character-precise editing. Practical implication for engineers: don't build character-level string operations on raw LLM output - do them in code, and use the LLM for the parts it's actually good at.

**Follow-ups:** Why does asking the model to spell the word first fix the count? What other task categories fail for the same root cause? How would a byte-level model differ here?

</details>

### 11. What does the temperature parameter actually do? Give the formula.

<details><summary><b>Answer</b></summary>

Temperature rescales the logits before the softmax that converts them into a probability distribution over the vocabulary:

p_i = exp(z_i / T) / Σ_j exp(z_j / T)

- **T = 1**: the model's raw distribution.
- **T → 0**: differences between logits are amplified; the distribution collapses toward the argmax - deterministic, greedy-like decoding. (T = 0 in APIs is implemented as argmax; true division by zero is undefined.)
- **T > 1**: differences are compressed; the distribution flattens, low-probability tokens become likelier - more diverse, more error-prone output.

Key properties worth stating: temperature is a *monotonic* transform - it never reorders tokens, only sharpens or flattens the distribution, so greedy decoding is unaffected by it. It operates per generation step on the conditional distribution, and its effects compound over a long generation: small increases in per-token entropy produce noticeably more divergent completions.

Practical guidance a strong candidate gives: use T = 0 (or near it) for extraction, classification, structured output, and code where there's a correct answer - you want the mode. Use T ≈ 0.7-1.0 for creative writing and brainstorming where diversity is the point. Note that T = 0 does not guarantee bit-identical outputs across API calls in practice (batching non-determinism, floating-point non-associativity across kernels, infrastructure changes), a common misconception worth flagging. Also note temperature interacts with truncation samplers: it's applied with top-p/top-k/min-p, and the order of operations (typically temperature first, then truncation, though implementations vary) changes behaviour at high T - min-p in particular was designed to stay robust at T > 1.

One more useful framing: temperature trades off exploitation of the model's confidence against exploration of its uncertainty - the same knob as in softmax exploration in RL.

**Follow-ups:** Why can T=0 still produce different outputs across identical API calls? If you increase temperature, why do you usually also want min-p or top-p? What temperature would you use for an LLM-as-judge evaluation and why?

</details>

### 12. Compare greedy decoding, top-k sampling, and top-p (nucleus) sampling.

<details><summary><b>Answer</b></summary>

**Greedy** takes the argmax token every step. Deterministic and cheap, fine for short factual answers and structured extraction. Failure mode: repetition loops ("the the the", or paragraph-level cycles) and blandness - locally optimal tokens don't compose into globally good text, and the model can enter self-reinforcing repetition where prior repeats make the next repeat *more* likely.

**Top-k** restricts sampling to the k highest-probability tokens (renormalized), typically k = 20-50. Problem: k is static while the distribution's shape varies enormously per step. When the model is confident (one token at 0.95), k = 40 admits 39 junk tokens; when it's genuinely uncertain across 200 plausible continuations (start of a story sentence), k = 40 truncates valid diversity.

**Top-p / nucleus** (from Holtzman et al., "The Curious Case of Neural Text Degeneration") adapts: keep the smallest set of tokens whose cumulative probability ≥ p (e.g. 0.9), renormalize, sample. Confident step → nucleus is 1-2 tokens; uncertain step → nucleus is large. This adaptivity is why top-p became the default. Its residual weakness: at high temperature the flattened distribution lets the nucleus swell to include genuinely bad tokens - which is what **min-p** (keep tokens with p ≥ min_p × p_max) addresses by anchoring the cutoff to the top token's confidence.

The key insight behind all truncation sampling: the model's probability mass is well-calibrated at the head of the distribution and unreliable at the tail - a long generation will eventually sample a tail token, and one bad token can derail everything after it (errors compound autoregressively). Truncation cuts the tail; temperature shapes what remains. In practice these compose: temperature + top-p (+ optionally top-k as a hard cap) is the standard stack, with greedy/T≈0 for anything with a right answer.

**Follow-ups:** Why does greedy decoding loop, mechanistically? When does top-p fail and how does min-p fix it? Why is sampled text at T=1 often *worse* than the model's "true" distribution would suggest?

</details>

### 13. What is the KV cache and why does it make generation fast?

<details><summary><b>Answer</b></summary>

During autoregressive generation, each new token's attention needs the keys and values of *all previous tokens* at every layer. Those K and V vectors depend only on the tokens that produced them (and their positions) - they don't change as generation proceeds. The KV cache stores them so each step computes Q/K/V only for the single new token, attends against cached K/V, and appends its own K/V to the cache.

Without the cache you'd re-run the full forward pass over the whole prefix for every generated token: generating token n costs O(n) recomputation, so a full generation costs O(n²) forward-pass work (with the attention inside making it effectively cubic-ish in total FLOPs). With the cache, each step does one token's worth of projections plus attention reads over n cached entries - generation becomes linear in tokens generated, which is the difference between usable and unusable latency.

This creates the two-phase structure every serving stack is built around: **prefill** (process the whole prompt in parallel - compute-bound, populates the cache) and **decode** (one token at a time - memory-bandwidth-bound, because each step must read the entire cache from GPU memory while doing relatively few FLOPs). Time-to-first-token is prefill; inter-token latency is decode.

The cost is memory: per token you store 2 (K and V) × n_layers × n_kv_heads × head_dim elements. For a 70B-class model with GQA (80 layers, 8 KV heads, head_dim 128, fp16) that's ~320 KB per token - ~40 GB for one 128k-token sequence. That memory pressure is why GQA/MQA exist (fewer KV heads), why vLLM's PagedAttention manages cache in non-contiguous blocks, why prefix/prompt caching shares cache across requests, and why cache quantization (fp8/int8 KV) is common.

**Follow-ups:** Why is decode memory-bandwidth-bound rather than compute-bound? What is prefix caching and when does it save money? Why can't you cache the queries too?

</details>

## Intermediate

### 14. Pre-norm vs post-norm - what's the difference and why did everyone move to pre-norm? And why RMSNorm?

<details><summary><b>Answer</b></summary>

**Post-norm** (original 2017 transformer): `x = Norm(x + Sublayer(x))` - normalization sits *on* the residual path, after the add. **Pre-norm** (GPT-2 onward, essentially all modern LLMs): `x = x + Sublayer(Norm(x))` - normalization is inside the branch, and the residual path is a pure identity.

Why it matters: with post-norm, the gradient from the loss to early layers must pass through every LayerNorm on the trunk, and each norm rescales gradients in ways that compound with depth - deep post-norm transformers are notoriously hard to train, requiring careful learning-rate warmup and still prone to divergence. With pre-norm, there is an unobstructed identity path from the loss to every layer - gradients reach early layers unattenuated, warmup requirements shrink, and training is stable at 80-100+ layers. Since frontier training runs cost tens of millions of dollars, stability wins over everything: pre-norm became universal.

The honest nuance: post-norm, *when you can train it*, sometimes achieves slightly better final quality - pre-norm's identity path means later layers can behave more like an ensemble of shallow paths, arguably wasting some depth. This motivated hybrids (e.g. "peri-norm"/double-norm arrangements, or Gemma-style normalizing both the branch input and output), but plain pre-norm remains the default.

**RMSNorm** vs LayerNorm: LayerNorm subtracts the mean, divides by standard deviation, then applies learned gain and bias. RMSNorm drops mean-centring and the bias - just divide by the root-mean-square of the vector and apply a learned gain: x / RMS(x) · g. Ablations (from the RMSNorm paper onward, confirmed at scale by Llama-family models) show the mean-centring isn't needed; RMSNorm is cheaper (fewer reductions, fewer params, one fewer memory-bound op) and equally stable. At thousands of norm invocations per forward pass, the savings are real.

**Follow-ups:** Why does warmup interact with post-norm? What does normalizing do to the loss landscape geometry? Where else in modern architectures do norms appear besides the two block positions (QK-norm, final norm)?

</details>

### 15. Walk me through the BPE training algorithm step by step.

<details><summary><b>Answer</b></summary>

Byte-Pair Encoding learns a vocabulary of subword merges from a corpus:

1. **Initialize** the vocabulary with the base alphabet - in byte-level BPE (GPT-2 onward), all 256 byte values, which guarantees any string is representable. Represent the corpus as sequences of these base symbols.
2. **Count** all adjacent symbol pairs across the corpus.
3. **Merge** the most frequent pair into a new single symbol, add it to the vocabulary, and record the merge rule (e.g. `t` + `h` → `th`).
4. **Repeat** steps 2-3 until the target vocabulary size is reached (e.g. ~50k merges for GPT-2's 50,257 vocab; ~128k for Llama 3's).

The output is an ordered list of merge rules. **Encoding** at inference time replays them: split the text into base symbols, then apply merges in the order they were learned wherever they occur, greedily, until no more apply. Encoding is deterministic; the learned merge order is the tokenizer.

```python
from collections import Counter
def bpe_step(corpus):                     # corpus: list of (symbol_tuple, freq)
    pairs = Counter()
    for word, freq in corpus:
        for a, b in zip(word, word[1:]):
            pairs[(a, b)] += freq
    return max(pairs, key=pairs.get)      # pair to merge next
```

Practical details that signal real understanding: real tokenizers apply a **pre-tokenization** regex first (splitting on whitespace/category boundaries, so merges don't cross word boundaries - GPT-2's regex famously special-cases contractions like `'s`), and they handle leading spaces as part of tokens (`" the"` and `"the"` are different tokens). Frequency-based merging means the vocabulary mirrors the training corpus distribution - which is exactly why tokenizers trained on English-heavy data fragment other languages. Note also the contrast: **WordPiece** picks the merge maximising corpus likelihood rather than raw frequency, and **unigram-LM** (SentencePiece's other algorithm) works top-down - start with a large candidate vocab and prune tokens whose removal least hurts likelihood.

**Follow-ups:** Why does pre-tokenization matter - what would go wrong without word-boundary constraints? Why do `"the"` and `" the"` need to be separate tokens? How does unigram-LM tokenization differ conceptually from BPE?

</details>

### 16. Compare BPE, WordPiece, SentencePiece, and byte-level BPE.

<details><summary><b>Answer</b></summary>

These are two algorithms, a library, and a base-alphabet choice - a distinction that itself scores points, because people wrongly treat them as four parallel algorithms.

**BPE** (algorithm): bottom-up, greedy - repeatedly merge the most *frequent* adjacent pair. Used (in byte-level form) by GPT-2/3/4-family tokenizers (tiktoken) and Llama 3.

**WordPiece** (algorithm, BERT): same bottom-up scheme but merges the pair that maximises training-corpus *likelihood* - score ≈ freq(ab) / (freq(a)·freq(b)) - favouring pairs that co-occur more than chance rather than just often. Recognisable by its `##` continuation-piece convention. Encoding uses longest-match-first rather than merge replay.

**Unigram-LM** (algorithm, often used via SentencePiece): top-down - start with a large candidate vocabulary, iteratively prune tokens whose removal least damages the corpus likelihood under a unigram model; encoding picks the most probable segmentation (Viterbi). Supports sampling alternative segmentations for regularization during training.

**SentencePiece** (library, not an algorithm): implements both BPE and unigram-LM. Its distinctive property: it operates on raw text as a character stream with **no external pre-tokenization** - whitespace is encoded as a meta-symbol (▁, U+2581) - making it language-agnostic (works for Chinese/Japanese/Thai where there are no spaces) and exactly reversible. Standard for multilingual and many open models (Llama 1/2, T5, Gemma).

**Byte-level BPE** (base-alphabet choice): run BPE over the 256 byte values instead of Unicode characters. Guarantee: *no string is ever out-of-vocabulary* - anything, any language, emoji, binary-ish garbage, decomposes to bytes at worst. Cost: rare non-Latin characters can fragment into multiple byte tokens. SentencePiece offers an equivalent escape hatch called byte-fallback.

Practical engineering relevance: tokenizer choice determines token counts (cost, latency, effective context) per language, and mismatched tokenizers are a classic source of bugs when swapping models - never assume token counts transfer across model families.

**Follow-ups:** Why does SentencePiece encode whitespace explicitly - what property does that buy? What is byte-fallback? Given the same vocab size, why might unigram-LM produce more linguistically natural segmentations than BPE?

</details>

### 17. What are the tradeoffs in choosing vocabulary size?

<details><summary><b>Answer</b></summary>

Vocab size trades sequence-length compression against parameter cost and tail-token quality. The industry trend tells the story: GPT-2 used 50,257; Llama 2 used 32k; Llama 3 moved to ~128k; GPT-4o's tokenizer is ~200k.

**Larger vocabulary - benefits:**
- **Fewer tokens per text**: more strings become single tokens, so the same document costs fewer tokens - directly cheaper inference, lower latency, and more content fits in the context window. Gains are largest for non-English languages and code, which small English-centric vocabs fragment badly. This is a major reason Llama 3 quadrupled Llama 2's vocab.
- Fewer autoregressive steps for the same output → faster generation.

**Larger vocabulary - costs:**
- **Embedding + LM-head parameters** scale as 2 × vocab × d_model (unless weight-tied). At d_model = 4096, a 128k vocab means ~525M embedding params and the same again for the output head - for small models this is a huge fraction of the budget (a 1B model can spend >30% of params on vocab), while for a 70B model it's noise. This is why small models almost always tie the embedding and LM head and are far more sensitive to vocab size, while large models can afford huge vocabularies.
- **Softmax compute** over the vocab at every position (mostly matters for small models, and for training throughput).
- **Under-trained tail tokens**: with more tokens, each rare token gets fewer training occurrences. Pathological case: "glitch tokens" (the SolidGoldMagikarp story - tokens present in the vocab but nearly absent from training data, whose embeddings are essentially uninitialized, producing bizarre behaviour when triggered).
- Larger multilingual vocabs make each token cover *more* text, which slightly reduces per-token granularity the model can exploit.

Rule of thumb: vocab size should scale with model size and with the breadth of languages/domains served. There's published work on compute-optimal vocab scaling showing frontier models had been under-sizing vocabularies.

**Follow-ups:** What are glitch tokens and what causes them? Why does weight-tying the embedding and LM head matter more for small models? How would you evaluate whether a tokenizer serves your target languages well?

</details>

### 18. Beyond letter counting, what failure modes does tokenization cause? Think arithmetic, multilingual text, and code.

<details><summary><b>Answer</b></summary>

**Arithmetic.** Numbers tokenize inconsistently: "1234" might be one token while "1235" splits as "12"+"35", and the same quantity chunks differently depending on surrounding text. Place-value alignment - the core of digit-wise algorithms - is destroyed when operands have inconsistent boundaries. This is why several model families force single-digit tokenization for numbers (each digit its own token), which measurably improves arithmetic: consistent structure lets the model learn positional algorithms. Comma formatting ("1,234,567") adds another layer of chunking chaos.

**Multilingual inefficiency.** Tokenizers are trained on a corpus; the merges reflect its language mix. English-heavy vocabs fragment other scripts - Hindi, Thai, Khmer, and others can cost 2-5× more tokens than English for equivalent content (byte-level fallback can reduce rare script characters to multiple byte tokens each). Consequences are concrete: users of those languages pay more per request, exhaust context windows sooner, hit output-token limits earlier, and get worse quality because the model reasons over fragmented units. It's an equity issue baked in before any learning happens - and a reason Llama 3 and newer tokenizers expanded vocab with explicitly multilingual data.

**Code.** Whitespace is syntax in Python, and tokenizers handle indentation via whitespace-run tokens (e.g. a token for 4 spaces, 8 spaces...). Models can confuse indentation levels - an off-by-one-level bug is a tokenization-adjacent failure. Tabs vs spaces tokenize entirely differently. Identifier splitting (`getUserById` → `get`+`User`+`By`+`Id`) is usually semantically reasonable, but rare identifiers fragment unpredictably. Modern code-aware tokenizers added dedicated whitespace and indentation handling, which was a real contributor to code-generation quality gains.

**General diagnostic habit** interviewers want: when an LLM fails at something character- or format-precise - spelling, string manipulation, character offsets in structured output, off-by-one edits - check the tokenization first. Pasting the failing input into a tokenizer visualiser resolves a surprising fraction of "model is dumb" bug reports.

**Follow-ups:** Why does single-digit number tokenization improve arithmetic? If your product targets Southeast Asian languages, what would you check before choosing a model? How would tokenization affect a code-diff-generation feature?

</details>

### 19. Attention is O(n²) in sequence length. Where does that actually bite in practice - prefill vs decode?

<details><summary><b>Answer</b></summary>

The n×n score matrix means attention FLOPs scale quadratically with sequence length, but *where* that hurts differs by phase, and strong candidates separate them.

**Prefill** (processing the prompt): genuinely quadratic compute. All n tokens attend to all prior tokens in parallel - total attention FLOPs ~O(n²·d) per layer. Doubling prompt length roughly quadruples attention prefill work (the MLP part scales linearly, so the blended exponent depends on length - at short contexts MLPs dominate; at 100k+ attention dominates). This is why time-to-first-token grows superlinearly for long prompts, and why serving stacks use chunked prefill to avoid stalling decode traffic behind a 100k-token prompt.

**Decode** (generating token-by-token, with KV cache): each step is O(n·d) - the new token attends over n cached entries. Quadratic total across a full generation, but the per-step cost is linear in context. The real constraint here isn't FLOPs at all - it's **memory bandwidth and capacity**: every step must stream the entire KV cache from HBM, and the cache itself grows linearly with n (that ~320 KB/token for a 70B-class GQA model → ~40 GB at 128k). Long context at decode time is a memory problem.

Consequences that follow: (1) long-context pricing - some providers price long-context requests higher because prefill compute and cache memory both balloon; (2) architectural responses - GQA/MQA/MLA shrink the cache, sliding-window attention (Mistral-style) bounds it, hybrid SSM-attention models attack both; (3) FlashAttention fixes attention's *memory* footprint (no materialised n² matrix) and IO but not the FLOP count - prefill is still quadratic; (4) product implications - "just stuff everything in context" has a real quadratic cost floor, which keeps RAG and context curation economically relevant even as windows grow.

**Follow-ups:** Why is decode memory-bandwidth-bound - walk me through the arithmetic intensity? What does sliding-window attention give up? Why doesn't FlashAttention change the asymptotic FLOP complexity?

</details>

### 20. Explain FlashAttention's core idea. What does it optimise, and what doesn't it change?

<details><summary><b>Answer</b></summary>

FlashAttention's insight is that standard attention is bottlenecked not by FLOPs but by **memory traffic**: the naive implementation materialises the n×n score matrix in GPU HBM, writes it, reads it back for softmax, writes the probabilities, reads them again to multiply by V. GPU compute vastly outpaces HBM bandwidth, so the kernel spends its time waiting on memory. FlashAttention is an **IO-aware, exact** reimplementation - same math, radically less memory movement.

Three mechanisms:

1. **Tiling**: split Q, K, V into blocks sized to fit in on-chip SRAM (orders of magnitude faster than HBM). Compute attention block-by-block, keeping intermediate products on-chip, fusing score computation, softmax, and the V-multiply into one kernel.
2. **Online softmax**: softmax normally needs the full row (for the max and the normalizer) before any output. The streaming trick maintains a running maximum and running sum as blocks arrive, rescaling previous partial results when the max updates - mathematically exact, no full row ever needed. This is the piece that makes tiling possible.
3. **Recomputation in backward**: instead of storing the n×n probability matrix for the backward pass, store only the row statistics (max, normalizer) and recompute attention blocks on the fly. Extra FLOPs, far less IO - a favourable trade on modern hardware.

Results: memory footprint for attention drops from O(n²) to O(n), wall-clock speedups of ~2-4× on typical shapes, and long-context training/inference becomes practical. FlashAttention-2/3 refine parallelization and exploit newer hardware (Hopper async execution, fp8).

What it does **not** change: the FLOP count is still O(n²) - prefill remains quadratic in compute; it's not sparse, linear, or approximate attention. And it doesn't shrink the KV cache - those are orthogonal problems solved by GQA/MLA/quantization. Common interview trap: calling FlashAttention an approximation. It's bit-for-bit the same attention (up to floating-point reordering), which is exactly why adoption was universal - no quality tradeoff to litigate.

**Follow-ups:** Walk me through the online softmax rescaling. Why is recomputation faster than storing the matrix? How does FlashAttention interact with causal masking?

</details>

### 21. How do sinusoidal positional encodings work, and how do they compare to learned positional embeddings?

<details><summary><b>Answer</b></summary>

Self-attention is permutation-invariant, so position must be injected explicitly. The original transformer added **sinusoidal encodings** to token embeddings: for position pos and dimension pair i, PE(pos, 2i) = sin(pos / 10000^(2i/d)) and PE(pos, 2i+1) = cos(pos / 10000^(2i/d)). Each dimension pair oscillates at a different frequency, geometrically spaced from wavelength 2π up to ~10000·2π - like a binary counter in continuous form, or clock hands ticking at different speeds. Low-frequency dims distinguish coarse position; high-frequency dims distinguish adjacent tokens.

Two elegant properties: no learned parameters (works for any position, including ones never seen in training - in theory), and for any fixed offset k, PE(pos+k) is a *linear function* of PE(pos) - a rotation in each frequency pair - so relative offsets are, in principle, easy for attention to compute. In practice extrapolation beyond trained lengths still degrades, because the model never learned to *use* the unseen combinations.

**Learned absolute embeddings** (GPT-2, BERT): just an embedding table indexed by position, added to token embeddings. Simpler, lets the model learn whatever positional structure helps, and empirically matched sinusoidal at trained lengths. Hard limitations: the table has a fixed size - position 1025 simply has no embedding in a 1024-trained model - and each position index is trained only as often as it appears, so late positions are under-trained.

Both share a deeper weakness: they encode **absolute** position, while language mostly cares about **relative** position ("the adjective before this noun"), and adding position to the *embedding* entangles content with position throughout the residual stream. That motivated the modern generation of methods that inject *relative* position directly into the attention computation - RoPE (rotate Q/K per position, so scores depend on offset) and ALiBi (distance-penalty bias on scores) - which is what current models actually use. Sinusoidal/learned absolute embeddings are now mostly of historical and conceptual importance.

**Follow-ups:** Why is relative position more useful than absolute for language? Show why a fixed offset is a linear transform of a sinusoidal encoding. Why does adding position to embeddings entangle content and position, and why does that matter?

</details>

### 22. Explain RoPE. What's the rotation intuition and why did it become the default?

<details><summary><b>Answer</b></summary>

Rotary Position Embedding injects position by **rotating** the query and key vectors rather than adding anything to embeddings. Pair up the dimensions of each head (dim 0-1, 2-3, ...) and treat each pair as a 2D vector; for a token at position m, rotate pair i by angle m·θ_i, where θ_i = 10000^(−2i/d) gives geometrically spaced frequencies - fast-spinning pairs encode fine/local position, slow-spinning pairs encode coarse/long-range position.

The payoff is what happens in the dot product. Rotations preserve norms, and the angle between a query rotated by m·θ and a key rotated by n·θ changes by exactly (m−n)·θ. So the attention score between positions m and n depends only on their **relative offset m − n** (and the content vectors) - relative position encoding, achieved multiplicatively, with zero learned parameters, applied only to Q and K (V is left alone; the output carries no positional contamination). The clock-hands intuition: each dimension pair is a clock hand spinning at its own rate as position advances; attention compares the *difference* in clock readings between two tokens.

Why it won (Llama, Qwen, Mistral, most modern open models - and it's the assumption behind most long-context tooling):

- Relative position matches what language needs, without the extra attention terms older relative-position schemes (T5 bias, Shaw et al.) required.
- No parameters, no position-table length cap; compatible with KV caching (each token's K is rotated once by its absolute position, then cached - relative behaviour emerges in the dot product).
- Decaying inter-token dependency with distance falls out naturally at standard frequency settings.
- Crucially, it turned out to be **extensible**: because position lives in rotation angles, context extension becomes frequency surgery - position interpolation, NTK-aware scaling, and YaRN all work by rescaling θ or positions, which is far cleaner than retrofitting an embedding table.

Limitation: vanilla RoPE still degrades sharply past trained length - unseen angle ranges are out-of-distribution - which is exactly what the extension methods address.

**Follow-ups:** Prove that the score depends only on m−n for a single 2D pair. Why is RoPE applied to Q and K but not V? How do position interpolation and YaRN manipulate RoPE's frequencies?

</details>

### 23. How does ALiBi encode position, and what's its claim to fame?

<details><summary><b>Answer</b></summary>

ALiBi (Attention with Linear Biases) uses **no positional embeddings at all**. Instead, it adds a static penalty directly to attention scores proportional to the distance between query and key: score(i, j) += −slope · (i − j) for j ≤ i. Each head gets a different fixed (not learned) slope, drawn from a geometric sequence (e.g. 1/2, 1/4, ..., 1/2⁸ for 8 heads) - so some heads are strongly recency-biased, effectively local, while shallow-slope heads can still attend far back. Position is expressed purely as "farther = softly down-weighted," and the model learns everything else from content.

Its claim to fame is **length extrapolation**: train at 1k - 2k context and run inference at much longer lengths with far less degradation than sinusoidal, learned, or vanilla-RoPE models, whose behaviour collapses on out-of-distribution position values. ALiBi has no out-of-distribution positions - the bias formula is the same linear function at any distance - so nothing structurally breaks at unseen lengths. It's also simple (a few lines in the attention kernel), parameter-free, and adds negligible compute. MPT and BLOOM shipped with it.

Honest limitations, which explain why RoPE still dominates: the built-in recency bias is a strong inductive prior - helpful for perplexity, but it means genuinely long-range retrieval must fight the penalty, and empirically ALiBi models are weaker at long-range recall tasks than extended-RoPE models; "doesn't blow up at length" is not the same as "uses length well." It's also awkward to combine with some attention optimisations, and the ecosystem's tooling consolidated around RoPE - once position interpolation and YaRN made RoPE extensible cheaply, ALiBi's headline advantage mattered less.

Conceptually it remains an important data point: relative position can be expressed as a *score-space bias* rather than embedding-space content, and the sliding-window-like behaviour of steep-slope heads prefigured explicit local-attention designs.

**Follow-ups:** Why does ALiBi extrapolate where RoPE doesn't? What's the cost of a recency prior for retrieval-heavy tasks? Compare ALiBi's bias to T5's learned relative-position buckets.

</details>

### 24. A model was pretrained at 8k context. You need 128k. What are your options? Explain position interpolation and YaRN.

<details><summary><b>Answer</b></summary>

The failure you're fixing: RoPE encodes position as rotation angles, and positions past 8k produce angle combinations the model has never seen - attention behaviour degrades catastrophically out-of-distribution. Naive fine-tuning at 128k from scratch positions is expensive and slow to converge, so the practical methods rescale RoPE so long contexts land inside (or near) the distribution the model already understands.

**Position interpolation (PI)**: compress positions linearly - to run at 32k on an 8k-trained model, multiply every position by 1/4 (equivalently, scale RoPE frequencies down) so the full range maps into [0, 8k]. All angles are now in-distribution; the cost is resolution - adjacent tokens are only a quarter of a "position unit" apart, blurring the fine-grained local distinctions the high-frequency dimensions were providing. A short fine-tune (order of ~1B tokens) recovers most quality. Simple and effective; local precision suffers most at large scale factors.

**NTK-aware scaling** (the intermediate idea): instead of compressing all frequencies equally, rescale the RoPE base so **low-frequency (long-wavelength) dims get interpolated a lot** while **high-frequency dims stay nearly intact** - preserving local resolution while stretching long-range coverage. Popular because it works surprisingly well even *without* fine-tuning.

**YaRN** combines and refines these: divide RoPE dimensions into bands by how many full wavelengths fit in the trained context - high-frequency bands are left untouched (they've seen all phases; they encode local structure), low-frequency bands are fully interpolated (their absolute angles matter), and a middle band is smoothly ramped between the two - plus a small attention-temperature adjustment (scaling attention logits) that compensates for the entropy shift longer contexts induce. YaRN reaches strong long-context quality with roughly an order of magnitude less fine-tuning data than plain PI, and it's the basis of many open-model long-context variants.

Also mention: production long-context models typically combine such scaling with dedicated **long-context mid-training** (continued pretraining on genuinely long documents) - frequency surgery makes long positions representable; training on long-range dependencies makes them *usable*. And verify with retrieval evals (needle-in-a-haystack and, better, multi-fact reasoning benchmarks like RULER-style suites) - advertised length ≠ usable length.

**Follow-ups:** Why do high-frequency RoPE dims need no interpolation? Why does long-context extension usually still require some fine-tuning on long documents? How would you verify usable context length before shipping?

</details>

### 25. What are MQA and GQA, and why do they exist?

<details><summary><b>Answer</b></summary>

They exist because of KV cache memory. In standard multi-head attention (MHA), every one of h heads has its own K and V projections, so the cache stores h keys and h values per token per layer. Cache size - not FLOPs - is the binding constraint on serving throughput: it determines how many concurrent sequences fit on a GPU (batch size), and decode speed is bounded by streaming the cache from HBM every step. Cutting KV heads attacks both.

**MQA (multi-query attention)**, from Shazeer's "Fast Transformer Decoding: One Write-Head is All You Need": keep h query heads but share a **single** K/V head across all of them. Cache shrinks by h× (e.g. 32×), decode bandwidth drops proportionally. Cost: measurable quality regression on some tasks, and training can be less stable - one K/V representation has to serve every query head's needs.

**GQA (grouped-query attention)**, Ainslie et al.: the interpolation. Partition the h query heads into g groups, each group sharing one K/V head - e.g. Llama-style 70B models use 64 query heads with 8 KV heads (groups of 8). Cache shrinks 8×, and quality is empirically near-indistinguishable from MHA. The GQA paper also showed you can **uptrain** an existing MHA checkpoint into GQA by mean-pooling its K/V heads and continuing training briefly - you don't need to pretrain from scratch. GQA is the default in essentially every serious model since 2023 (Llama 2/3 large variants, Mistral, Qwen...).

Concrete impact: a 70B-class model at fp16 with 80 layers and head_dim 128 stores ~2.6 MB/token with 64 KV heads versus ~320 KB/token with 8 - the difference between fitting ~4 and ~30+ long sequences in the same memory.

The natural follow-on is **MLA** (multi-head latent attention, DeepSeek): compress K/V into a shared low-rank latent vector per token and reconstruct per-head K/V from it - cutting cache further while *increasing* effective head diversity versus GQA. Worth mentioning to show you know where this design line went.

**Follow-ups:** Why is decode throughput bounded by memory bandwidth, and how does GQA change the arithmetic? How does the GQA uptraining recipe work? What does MLA do differently?

</details>

### 26. Derive the KV cache memory formula and compute it for a concrete model.

<details><summary><b>Answer</b></summary>

Derivation from what's stored: for each token, at each layer, the cache holds that token's key and value vectors for every KV head. A key (or value) vector per head has head_dim elements. So:

**bytes per token = 2 × n_layers × n_kv_heads × head_dim × bytes_per_element**

(2 for K and V; multiply by seq_len for a sequence, and by batch size for a serving node.) Note it's **kv** heads - with GQA the query head count is irrelevant to the cache.

Concrete: a Llama-3-70B-shaped model - 80 layers, 8 KV heads (GQA), head_dim 128, fp16 (2 bytes):

```python
bytes_per_token = 2 * 80 * 8 * 128 * 2      # = 327,680 ≈ 320 KB/token
seq_128k = bytes_per_token * 131_072        # ≈ 42 GB for one sequence
seq_8k   = bytes_per_token * 8_192          # ≈ 2.7 GB
```

So a single 128k-context conversation consumes ~40+ GB of GPU memory *beyond* the ~140 GB of fp16 weights. With full MHA (64 KV heads) it would be 8× worse: ~2.6 MB/token, ~340 GB at 128k - completely unservable. That one comparison is the entire justification for GQA.

Engineering consequences to draw out: (1) batch capacity - cache memory, not weights, caps concurrent users, so cache size directly sets cost per request; (2) **PagedAttention** (vLLM) exists because naively pre-allocating max-length contiguous cache wastes most of it - paging allocates on demand in blocks, like virtual memory; (3) **KV quantization** to fp8/int8 halves or quarters this again with modest quality cost; (4) **prefix caching** shares the cache of common prompt prefixes (system prompts, few-shot examples) across requests - huge savings for agentic workloads that repeatedly re-send growing conversations; (5) speculative decoding, beam search, and parallel sampling all multiply cache pressure.

Sanity-check habit: memorise the formula, not model numbers - interviewers vary the architecture and want to watch you compute.

**Follow-ups:** How does PagedAttention reduce waste, and what problem does fragmentation cause? On an 8×80 GB node serving this model, how many concurrent 32k-token sequences fit after the weights? How does sliding-window attention change the formula?

</details>

### 27. Explain min-p sampling and repetition/frequency penalties. When do standard sampling settings fail?

<details><summary><b>Answer</b></summary>

**Min-p** keeps only tokens whose probability is at least min_p × p_max (the top token's probability), then renormalizes and samples. The threshold *scales with model confidence*: if the top token has p = 0.9, min_p = 0.1 keeps only tokens above 0.09 - essentially just the head; if the top token has p = 0.1 (genuine uncertainty), tokens above 0.01 survive - wide, appropriate diversity. Contrast with top-p, whose cumulative-mass criterion degrades at high temperature: flattened distributions push the nucleus deep into the junk tail. Min-p stays anchored to the best token, which is why it enables stable sampling at temperatures like 1.5-3 where top-p output falls apart - popular in creative-writing and open-model communities, supported in vLLM and llama.cpp.

**Repetition-family penalties** exist because autoregressive models have a self-reinforcing loop: repeated text raises the probability of repeating further, and greedy/low-temperature decoding can lock into cycles. Three standard variants: **repetition penalty** (divide/multiply logits of previously seen tokens by a factor like 1.1-1.3), **frequency penalty** (subtract an amount proportional to the token's count so far - punishes heavy reuse progressively), and **presence penalty** (flat subtraction for any token that has appeared at all - pushes topic novelty). OpenAI-style APIs expose the latter two.

**When standard settings fail** - the part that shows production experience:

- **Structured output/code with penalties on**: JSON needs to repeat `"`, `{`, `,`, field names; code needs repeated identifiers and indentation tokens. Repetition penalties corrupt exactly these - a classic cause of malformed JSON. Turn them off (or near-off) for structured generation; use constrained decoding instead.
- **High temperature + top-p**: incoherence via tail sampling - switch to min-p or lower T.
- **T = 0 for long free-form generation**: repetition loops - the thing penalties were invented for.
- **Aggressive presence penalty in long conversations**: the model starts avoiding necessary domain terms it already used.
- Also: penalties apply to *token IDs*, not words - they can't see that "dog" and " dog" are the same word, another tokenization leak.

**Follow-ups:** Why does top-p specifically break down at high temperature? How would you generate guaranteed-valid JSON - sampling settings or constrained decoding? Why do repetition penalties operate on tokens rather than words, and what artifacts does that cause?

</details>

### 28. What are logprobs, and what are they useful for in production systems?

<details><summary><b>Answer</b></summary>

A logprob is the log of the probability the model assigned to a token - log softmax(z) - at a given step. APIs (e.g. OpenAI's `logprobs`/`top_logprobs`) can return, per output token, its logprob plus the top-k alternative tokens and theirs. They're the closest thing you get to the model's internal confidence, and they're free - no extra forward pass.

Production uses:

- **Classification with confidence.** Frame the task so the answer is a single token ("yes"/"no", "A" - "D"); the logprob is a confidence score. Route low-confidence cases to a bigger model, a human, or an abstention path. This is the cleanest way to get calibrated-ish scores out of an LLM classifier, and to set precision/recall thresholds like a normal ML system.
- **Hallucination/uncertainty heuristics.** Low or entropy-spread logprobs on content-bearing spans (names, numbers, dates) flag likely fabrications. Not a guarantee - models can be confidently wrong - but a usable signal for triggering verification or citation checks.
- **Reranking and scoring.** Score candidate completions, retrieval passages, or MCQ options by total/average logprob; perplexity of a document under the model is a fluency/anomaly signal (also used heavily in pretraining data filtering).
- **Evals.** Perplexity-based evaluation; MCQ benchmarks (score each option, pick the max - the standard trick behind many benchmark harnesses) - cheaper and lower-variance than parsing generated answers.
- **Debugging.** When output goes weird at a specific point, per-token logprobs show exactly where the model got uncertain, and top-k alternatives show what it almost did - invaluable for prompt debugging and for spotting tokenizer artifacts.
- **Distillation/data work.** Soft targets for training smaller models; confidence-based filtering of synthetic data.

Caveats a strong candidate raises: RLHF-tuned models are notoriously **miscalibrated** relative to base models (alignment sharpens distributions), so treat logprobs as relative signals, tune thresholds on your own data; sequence-level probability ≠ answer correctness (many phrasings share the same answer - its true probability is spread across paraphrases); and closed APIs may not expose logprobs on all endpoints/models, sometimes for distillation-prevention reasons.

**Follow-ups:** Why does RLHF hurt calibration? Design a confidence-thresholded router using logprobs - what would you validate? Why is the probability of an *answer* not the same as the probability of a *sequence*?

</details>

### 29. Describe the modern LLM training pipeline: pretraining → mid-training → SFT → RL.

<details><summary><b>Answer</b></summary>

**Pretraining** - next-token prediction over trillions of tokens (web crawl, code, books, papers; heavily filtered, deduplicated, and mixture-weighted). This is where nearly all compute goes (months on thousands of accelerators) and where capabilities - language, knowledge, code, latent reasoning - actually come from. Output: a *base model* that completes text but doesn't follow instructions or converse; it might answer your question or continue it with three more questions.

**Mid-training** (continued pretraining) - the messy-but-crucial middle stage labs now name explicitly: still next-token prediction, but on deliberately curated data for targeted goals: injecting high-quality domain data (math, code, synthetic textbooks), **context-length extension** (long documents + RoPE rescaling - long context is a mid-training deliverable, not a pretraining default), and **annealing** - decaying the learning rate over the highest-quality data, upweighting instruction-formatted and exam-style material so the base model lands closer to its post-trained destination.

**SFT (supervised fine-tuning)** - cross-entropy on curated (prompt, response) pairs, loss usually masked to response tokens. Teaches format and behaviour: chat structure, instruction following, tool-call syntax, refusal style, persona. Relatively tiny (order of 10⁴ - 10⁶ examples) and cheap versus pretraining. Key mental model: SFT *elicits and shapes* what pretraining built; it adds behaviour, not (much) knowledge - pushing new facts via SFT tends toward memorisation and can even encourage hallucination-shaped behaviour.

**RL / preference optimisation** - align outputs with human or verifiable preferences beyond what demonstrations capture. Classic **RLHF**: train a reward model on human preference pairs, optimise the policy with PPO under a KL leash to the SFT model. **DPO** and successors skip the explicit reward model, optimising preferences directly - simpler, cheaper, widely used. **RLVR** (RL from verifiable rewards, e.g. **GRPO**): reward comes from checkable outcomes (unit tests pass, math answer matches) - this is what trains o1/R1-style reasoning models and represents the current frontier, because it can *extend* capabilities rather than just steer style.

Framing that lands well: pretraining ≈ building the engine; mid-training ≈ upgrading components; SFT ≈ teaching it to drive on roads; RL ≈ coaching it against outcomes. Each stage is orders of magnitude cheaper than the previous, but the later stages disproportionately determine perceived quality.

**Follow-ups:** Why does SFT on new facts encourage hallucination? What does the KL constraint in RLHF prevent? Why did verifiable rewards unlock reasoning gains that preference-based RLHF didn't?

</details>

## Advanced

### 30. What is "lost in the middle," and why doesn't a long context window equal reliable retrieval?

<details><summary><b>Answer</b></summary>

"Lost in the middle" (Liu et al., 2023) is the empirical finding that models retrieve and use information best when it sits at the **beginning or end** of the context, with a pronounced accuracy dip for content in the middle - a U-shaped curve, demonstrated on multi-document QA and key-value retrieval tasks. Strikingly, this held even for models explicitly built for long contexts - extended-context variants were no better at using mid-context information than their short-context siblings at equal positions.

Why it happens (plausible mechanisms, worth presenting as such): training data has positional structure - important content clusters at document starts (headlines, abstracts) and recency matters for next-token prediction, so attention learns primacy and recency priors; attention mass also concentrates on early tokens ("attention sinks") and recent tokens by construction. Add causal masking's asymmetry and there's no pressure during pretraining to weight the middle of a 100k-token window uniformly.

Why long context ≠ retrieval - the engineering takeaways:

- **Advertised ≠ usable.** A model accepting 1M tokens is not a promise of uniform recall over 1M tokens. Needle-in-a-haystack tests are the *easy* case (verbatim retrieval of a distinctive string); realistic tasks - aggregating several mid-context facts, reasoning across them, resisting distractors - degrade much earlier, which is what harder suites (RULER-style, multi-needle, long-form reasoning benchmarks) show.
- **RAG survives long context.** Retrieval + curation puts the relevant 2k tokens where the model performs best, at a fraction of the prefill cost and latency of stuffing 500k tokens per query - quadratic prefill and per-token pricing make brute-force context economically dominated even when quality holds.
- **Position-aware prompting matters**: put instructions and the most critical material at the start and end; re-state key constraints near the end for long agentic transcripts; summarise/compact long histories rather than letting them grow.

Nuance for 2026: frontier models have substantially improved mid-context recall - the effect has shrunk, not vanished - and it remains worst on aggregation-style tasks. Verify against your own workload; don't assume either the 2023 pathology or vendor claims.

**Follow-ups:** How would you design an eval for *usable* context length on your workload? Why do needle-in-a-haystack results overstate long-context ability? What are attention sinks and how do they connect?

</details>

### 31. Compare Kaplan and Chinchilla scaling laws. What did Chinchilla change?

<details><summary><b>Answer</b></summary>

Both fit power laws relating loss to model size (N), data (D), and compute (C ≈ 6ND for training) - the shared, load-bearing conclusion being that loss improves predictably and smoothly as a power law across many orders of magnitude, which is what makes betting hundreds of millions on a training run rational.

**Kaplan et al. (2020, "Scaling Laws for Neural Language Models")** concluded that for a fixed compute budget, you should scale **parameters much faster than data** - most incremental compute goes into a bigger model. The field followed: GPT-3 (175B on ~300B tokens) and Gopher (280B on 300B tokens) are Kaplan-shaped - enormous models, comparatively little data.

**Chinchilla (Hoffmann et al., 2022)** re-ran the analysis with a crucial fix: Kaplan's experiments had used a roughly fixed (and too-short, non-optimised) learning-rate schedule across runs, undertraining the smaller models and biasing the fit toward "parameters matter more." With schedules tuned per compute budget (plus IsoFLOP analyses and a parametric loss fit), the corrected answer: **scale N and D roughly equally** - compute-optimal is approximately **~20 tokens per parameter**. The demonstration: Chinchilla, 70B params on 1.4T tokens, same compute as Gopher (280B/300B), outperformed it across the board. The field's flagship models were 3-4× oversized and correspondingly data-starved.

Consequences: an immediate industry pivot toward smaller-N/bigger-D training; data collection, cleaning, and deduplication became first-class engineering concerns (and "are we running out of high-quality tokens?" became a serious question, pushing synthetic data); and inference costs dropped since equal-quality models got smaller.

Sharp caveats that distinguish a strong answer: Chinchilla-optimal minimises loss *for a fixed training budget only* - it ignores inference entirely, which is why nobody follows it anymore (see the overtraining question); the laws predict *pretraining loss*, not downstream capabilities, and the loss→capability mapping can be nonlinear; and the fitted constants are data- and architecture-dependent - 20 tokens/param is a rule of thumb from one setup, not a physical constant.

**Follow-ups:** Why did Kaplan's learning-rate schedule choice bias the conclusion? What does C ≈ 6ND assume? If high-quality data becomes the binding constraint, how does the optimal allocation shift?

</details>

### 32. Why do modern models train far past Chinchilla-optimal?

<details><summary><b>Answer</b></summary>

Because Chinchilla answers the wrong question for a product company. It minimises loss subject to a fixed **training** compute budget - treating training as the only cost. But training is paid **once**, while inference is paid on **every** request for the model's entire deployed life. For any model with real traffic, lifetime inference compute dwarfs training compute, and inference cost scales with parameter count. So the economically relevant optimisation is: minimise *training + lifetime-inference* cost subject to a quality target - and its solution is a **smaller model trained on far more data** than Chinchilla prescribes.

Mechanics: past the ~20 tokens/param point, additional data still improves a fixed-size model - with smoothly diminishing returns, but no wall. You spend "inefficient" extra training FLOPs to push a small model to a quality level Chinchilla would achieve with a larger model - then harvest the savings on every single inference call, forever. The exchange rate is favourable whenever expected serving volume is high.

Concrete evidence of the regime shift: Chinchilla-optimal for an 8B model is ~160B tokens; Llama 3 8B trained on ~15T tokens - roughly **~1,900 tokens per parameter**, about 100× past "optimal" - precisely because Meta optimised for deployment (including edge/on-device viability), not training-loss-per-FLOP. Essentially every serious open-weights release since (Llama, Qwen, Gemma, Mistral small models) is heavily overtrained in this sense, and the same logic governs closed models' small/fast tiers (the -mini/-flash/-haiku class), typically combined with distillation from larger internal models.

Additional forces pushing the same direction: small models unlock latency-sensitive and on-device products regardless of FLOP accounting; memory footprint (weights + KV cache) constrains serving concurrency, favouring fewer params; distillation makes overtraining even more effective by improving the training signal per token; and MoE complicates the arithmetic further by partially decoupling capacity (total params) from inference cost (active params).

Crisp summary line: Chinchilla tells you the cheapest way to *reach* a loss; inference economics tells you the cheapest model to *serve* at that loss. Modern labs optimise the second.

**Follow-ups:** Sketch the total-cost-of-ownership optimisation that replaces Chinchilla's. How does distillation change the overtraining calculus? Why is MoE another answer to the same economic pressure?

</details>

### 33. What are "emergent abilities," and what is the mirage critique? Where does that debate land practically?

<details><summary><b>Answer</b></summary>

**The claim** (Wei et al., 2022, "Emergent Abilities of Large Language Models"): some capabilities - multi-step arithmetic, certain BIG-Bench tasks, instruction following - show near-random performance across small scales, then jump sharply above some model size. "Emergent" = not predictable by extrapolating from smaller models. This mattered doubly: scientifically (capabilities aren't smooth in scale even though loss is) and for safety planning (if abilities appear unpredictably, you can't forecast what the next 10× model will do).

**The mirage critique** (Schaeffer et al., 2023, "Are Emergent Abilities of Large Language Models a Mirage?"): the sharpness is largely an artifact of **discontinuous metrics**, not discontinuous model improvement. Exact-match on a 5-digit arithmetic problem scores 0 unless *every* token is right; a model can be improving steadily on per-digit accuracy while exact-match sits at zero - until per-token quality crosses the threshold where whole answers start landing, and the metric leaps. Replace exact match with continuous measures (per-token likelihood, edit distance) and the curves become smooth; conversely, you can manufacture "emergence" in ordinary systems by choosing a harsh enough metric. The underlying model improvement is a smooth power law all along.

**Where it lands** - the nuanced position interviewers want:

- The mirage critique is substantially right about *measurement*: much reported emergence dissolves under continuous metrics, and smooth internal progress often precedes visible capability. Loss curves genuinely are smooth.
- But it doesn't make thresholds irrelevant: **the discontinuous metric is often the real-world requirement**. Code either passes tests or doesn't; an agent either completes a task or doesn't; arithmetic is only useful exactly right. If deployment utility is a step function of smooth underlying skill, then *product-level* emergence is real even when *model-level* emergence is a mirage - you still experience "suddenly it works" between model generations.
- Practical synthesis: track smooth leading indicators (per-token metrics, pass@k at high k, log-likelihood on target tasks) to *forecast* when threshold metrics will flip; don't conclude "the model can't do X" from a harsh metric at one scale; and for capability/safety forecasting, assume smooth competence growth with metric-dependent visibility.

**Follow-ups:** Give a concrete task where the deployment metric is inherently discontinuous - what smooth proxy would you monitor? How does this debate affect scaling-law-based capability forecasts? Does chain-of-thought change what appears emergent?

</details>

### 34. Explain Mixture-of-Experts: the router, top-k experts, total vs active parameters. Why does it win?

<details><summary><b>Answer</b></summary>

MoE replaces each transformer block's dense MLP with **E parallel expert MLPs** plus a lightweight learned **router** (typically a single linear layer producing scores over experts, per token, per layer). For each token, the router selects the **top-k** experts (k = 1 or 2 classically; DeepSeek-style designs use finer-grained experts with larger k, often plus an always-on shared expert); the token is processed by only those experts, and their outputs are combined weighted by the router's (softmaxed) gate values. Attention layers usually stay dense; routing decisions are made independently per token and per layer.

This decouples two things dense models entangle: **capacity** (total parameters - all experts) and **per-token compute** (active parameters - only k experts' worth). Mixtral 8x7B: 8 experts, top-2, ~47B total but ~13B active per token. DeepSeek-V3: ~671B total, ~37B active. In a dense model those numbers are equal by definition.

Why it wins: scaling laws reward parameters, but dense parameter growth raises per-token FLOPs proportionally. MoE buys parameter count - more stored knowledge, more specialised computation - at a fraction of the FLOP cost. Empirically, an MoE reaches a given loss with substantially less training compute than a dense model of equal quality, and serves with the latency profile of its *active* size. The implicit bet, which holds in practice, is that not every token needs every parameter: experts specialise (observed specialisation is often syntactic/token-level - code, punctuation, numbers - rather than the tidy topical "math expert" story), and conditional computation exploits that. It's the same economic logic as overtraining: optimise quality per *inference* FLOP, not per parameter.

The costs (previewing the follow-up question): routing is a discrete, load-balancing-sensitive operation that complicates training; and at inference **all experts must be resident in memory** - you pay memory for total params while only computing with active ones, which shapes where MoE makes deployment sense (large batched serving, expert-parallel clusters) and where it doesn't (single consumer GPU).

**Follow-ups:** Why route per-token rather than per-sequence? What do experts actually specialise in, empirically? Is a 47B-total/13B-active MoE comparable to a 13B dense model or a 47B dense model - on what axis?

</details>

### 35. What goes wrong when training MoE models, and what's the inference memory caveat?

<details><summary><b>Answer</b></summary>

**Training instabilities - mostly downstream of one problem: routing is a discrete decision trained with gradient descent.**

- **Router collapse / load imbalance**: the rich-get-richer loop. Early-favoured experts get more tokens, train faster, get better, attract more traffic - until a few experts absorb everything and the rest are dead weight. Standard fix: an **auxiliary load-balancing loss** penalising deviation from uniform expert utilisation per batch. But this creates a tension - the balancing loss actively fights the router's quality-driven preferences, and overweighting it hurts the model. (DeepSeek-V3 notably pushed an auxiliary-loss-free balancing scheme using learned per-expert bias adjustments, precisely to escape this tension.)
- **Router logit blowup**: router logits growing large destabilises training (saturated softmax, huge gradients) - mitigated by the **router z-loss** (from ST-MoE, Zoph et al.), penalising large logsumexp of router logits. MoE runs are empirically more spike- and divergence-prone than dense runs, requiring more careful precision handling (routers often kept in fp32).
- **Non-differentiable top-k**: gradients flow only through selected experts' gate weights; the "would another expert have been better?" counterfactual gets no direct signal - routing learning is noisy.
- **Systems coupling**: experts are sharded across devices (expert parallelism), so token routing becomes all-to-all network communication; load imbalance is now also a *hardware* stall problem. **Capacity factors** cap tokens per expert; overflow tokens get dropped (silently skipping computation) - a quality/throughput knob dense models don't have. Fine-tuning MoEs is also touchier (routers can destabilise on narrow distributions).

**The inference memory caveat**: sparsity saves FLOPs, not memory. Every expert must be loaded and resident, because any token may route anywhere - a ~47B-total/13B-active model needs ~94 GB in fp16, the memory of a 47B dense model with the latency of ~13B. Consequences: MoE suits high-throughput batched serving on memory-rich, fast-interconnect clusters (where large batches keep all experts busy and per-token bandwidth for weights is amortised); it's a poor fit for single-GPU or on-device deployment, where a dense model of equal *quality* often deploys better. At small batch sizes the advantage narrows further - you stream lots of weights for few tokens.

**Follow-ups:** Why does the load-balancing loss trade quality for stability? What does expert parallelism do to inference latency tails? When would you recommend dense over MoE despite MoE's training-compute win?

</details>

### 36. What are the root causes of hallucination, and what actually mitigates it?

<details><summary><b>Answer</b></summary>

Root causes, from the objective outward:

1. **The training objective optimises plausibility, not truth.** Next-token prediction rewards continuing text the way the corpus would - a fluent, confident, *wrong* citation and a correct one can be nearly indistinguishable in loss. The model learns the *form* of factual assertion, and form generalises beyond the facts that back it: ask for a paper on topic X by author Y and it will assemble a plausible title because that's exactly what its objective taught it to do.
2. **No calibrated abstention channel.** Pretraining contains almost no examples of "I don't know" issued *because the writer lacked knowledge* in a way correlated with the model's own knowledge gaps. And the incentive analysis (formalised in OpenAI's 2025 work on why models hallucinate) is blunt: under binary-graded training and evals, guessing has positive expected value and abstaining scores zero - models are systematically trained to be confident test-takers. Post-training can make it worse: human raters historically preferred confident, complete-looking answers.
3. **Knowledge is parametric, lossy, and frozen** - compressed statistics over a corpus with a cutoff, no provenance, no lookup; interpolation between memorised fragments produces confabulated composites. Sampling adds stochastic error, and autoregression **compounds** it: one fabricated entity early forces the model to stay consistent with its own fiction.

Mitigations, roughly in order of practical leverage:

- **Grounding (RAG + citation)**: retrieve source text into context and require quoted/cited answers - converts recall into constrained reading comprehension, plus makes verification possible. The single biggest lever for knowledge tasks.
- **Tool use**: calculators, code execution, search - route the failure-prone operation out of the weights entirely.
- **Abstention-aware post-training and evals**: train and grade with credit for calibrated "I don't know" and penalties for confident errors, not just accuracy - attacking cause #2 directly; frontier labs now report hallucination/abstention metrics.
- **Verification layers**: self-consistency (sample k, check agreement), a checker pass validating claims against sources, logprob/entropy flags on entities → escalate or verify.
- **Product design**: show citations, expose uncertainty, keep humans in the loop where errors are costly.

Honest framing: mitigations reduce rate and blast radius; nothing eliminates it - a system claim ("verified against sources"), not a model claim, is what you can actually ship.

**Follow-ups:** Why can RLHF *increase* confident hallucination? Design a hallucination eval for a RAG product - what's the metric? When is a hallucination-shaped answer actually desirable (creative tasks) and how do you switch regimes?

</details>

### 37. What are reasoning models, and how does test-time compute change the picture? When would you use one versus a standard model?

<details><summary><b>Answer</b></summary>

Reasoning models (OpenAI's o1 lineage, DeepSeek-R1, and the extended-thinking modes of frontier models) are LLMs post-trained with **RL against verifiable rewards** to produce long chains of thought before answering. The recipe R1 made public: take a strong base model, run RL (GRPO - group-relative policy optimisation, comparing sampled solutions within a group to compute advantages without a value network) on problems with checkable answers - math with known solutions, code with unit tests. Reward correctness; the emergent result is that the model *learns* to think longer - exploring, backtracking, self-checking ("wait, let me reconsider") - because those behaviours win reward. Length isn't directly incentivised; it emerges because deliberation pays.

The conceptual shift is **test-time compute as a scaling axis**: accuracy on hard problems scales with tokens spent thinking, not just with parameters or training compute. Instead of buying capability once at training time, you spend it per-query, proportional to difficulty - a knob (thinking budgets, effort settings) that didn't exist before. Related techniques - self-consistency (sample k, majority-vote), best-of-n with verifiers - are the parallel-sampling version of the same idea.

**When to use reasoning models**: multi-step math and quantitative analysis; hard debugging and non-boilerplate code; planning in agentic loops; problems with verifiable structure where being right matters more than being fast. Gains are large precisely where standard models fail by skipping steps.

**When not to**: extraction, classification, summarisation, routine formatting - thinking adds cost and latency, not accuracy; latency-sensitive UX (thinking can add seconds-to-minutes before the first visible answer token); high-volume cheap paths. The tradeoff is stark: 10-100× more output tokens, output tokens priced above input, and you pay for thinking tokens you may never display. Overthinking is a real failure mode - simple questions answered slowly, occasionally *worse* through second-guessing.

The 2026 production pattern is routing and budgeting: hybrid models expose thinking as a dial (off / bounded budget / high effort); systems route easy traffic to fast paths and reserve deliberation for queries that earn it. Treat reasoning as a resource to allocate, not a model to default to.

**Follow-ups:** Why do verifiable rewards matter so much - what goes wrong RL-training reasoning against a learned preference reward? How does GRPO differ from PPO? How would you decide a thinking budget per request class in production?

</details>

### 38. What is distillation, and how is it used in the LLM ecosystem?

<details><summary><b>Answer</b></summary>

Distillation trains a small **student** model to imitate a large **teacher**, transferring capability into a cheaper deployment footprint. The classic form (Hinton et al., 2015) matches the teacher's **soft targets**: minimise KL divergence between student and teacher output distributions, per token. The full distribution is far richer than the one-hot label - the teacher's relative probabilities over plausible alternatives ("dark knowledge") encode similarity structure a hard label discards - so the student learns more per example than from ground truth alone.

In the LLM world, two regimes:

- **Logit/white-box distillation**: requires teacher logits, so teacher weights must be accessible (your own model, or open weights). Token-level KL on shared vocabulary; richest signal, most infrastructure.
- **Sequence-level / black-box distillation**: generate outputs from the teacher and SFT the student on them - no logits needed, works through an API-shaped boundary. This is by far the dominant mode today: frontier labs distill their flagship internal models into the -mini/-flash/-haiku serving tiers, and the open ecosystem trains small models on synthetic data from large ones. DeepSeek-R1's release made the pattern vivid: R1-generated reasoning traces fine-tuned into Qwen and Llama models produced small models with strong reasoning - **reasoning distillation** (student imitates the teacher's chain of thought, not just final answers) turned out to transfer capability remarkably well, and much more cheaply than running RL on the small model directly.

Why it beats training small models from scratch: the teacher acts as a data engine and curriculum - its outputs are cleaner, more consistent, and better-formatted than raw web text, so the student reaches quality per parameter that its own scale couldn't extract from raw data. Combined with overtraining (question 32), it's how modern small models got so good.

Limits and caveats: the student inherits the teacher's errors, biases, and style ceiling - you generally can't distill *past* the teacher; coverage gaps in generated data become student blind spots; quality/diversity filtering of teacher outputs is most of the actual engineering; and most commercial API terms prohibit distilling their outputs into competing models - the legal/ToS dimension is a real consideration, and a reason labs restrict logprob exposure.

**Follow-ups:** Why do soft targets carry more information than hard labels - can you formalise it? When does on-policy distillation (student generates, teacher corrects/scores) beat plain imitation of teacher outputs? How would you build a distillation data pipeline with quality filtering?

</details>

### 39. Beam search is standard in machine translation. Why is it rarely used for open-ended LLM generation?

<details><summary><b>Answer</b></summary>

Beam search maintains the B highest-scoring partial sequences, expanding each with candidate next tokens and keeping the global top B by cumulative log-probability - approximate maximum-a-posteriori decoding for the full sequence, fixing greedy's myopia (a locally suboptimal token can win later).

It works in translation/ASR/constrained summarisation because those tasks have a **narrow set of acceptable outputs tightly determined by the input** - the highest-likelihood sequence is genuinely likely to be the best answer, and beam sizes of 4-10 reliably help. The output distribution is low-entropy for good reason.

For open-ended generation it fails for a deeper reason than cost - **the mode of the distribution is not what you want**. Holtzman et al. ("The Curious Case of Neural Text Degeneration") showed high-likelihood text from LLMs is degenerate: repetitive, generic, self-looping (repetition self-reinforces, so a repeating beam keeps scoring well), while natural human text is consistently *lower*-probability under the model - humans routinely choose "surprising" continuations, and there are astronomically many good continuations, each individually improbable. Maximising sequence likelihood chases a mode that corresponds to bland, loop-prone text; sampling from the (truncated) distribution matches the entropy profile of natural language. In short: open-ended quality ≈ a *sample* from a well-shaped distribution; translation quality ≈ the *argmax* of a peaked one.

Secondary but real practical reasons: beam search multiplies KV cache memory and compute by B - expensive precisely where the KV cache is already the binding constraint - and it serializes poorly in batched serving stacks (vLLM and friends treat it as a second-class citizen). Length bias (log-prob sums favour short sequences, requiring length normalization hacks) adds more friction.

Where beam-shaped ideas persist: constrained decoding (forcing outputs into a grammar/JSON schema), some structured-output and speech pipelines, and - reframed - best-of-n sampling with a *verifier or reward model* replacing likelihood as the ranking function, which fixes exactly the "likelihood ≠ quality" failure and is core to test-time-compute methods.

**Follow-ups:** Why does likelihood diverge from quality specifically for open-ended tasks - what's the entropy argument? Why does best-of-n with a reward model succeed where beam search fails? What's length bias in beam search?

</details>

### 40. Where do the parameters and FLOPs actually live in a transformer? Walk me through the budget.

<details><summary><b>Answer</b></summary>

Per decoder block, for a Llama-2-7B-shaped model (d_model = 4096, 32 heads, head_dim 128, SwiGLU d_ff = 11008, full MHA):

- **Attention**: four projections W_q, W_k, W_v, W_o, each d×d → 4d² ≈ 67M params. With GQA (e.g. 8 of 32 KV heads), K and V shrink 4× → ~2.5d² ≈ 42M.
- **MLP (SwiGLU)**: three matrices (gate, up, down), each d × d_ff → 3 · 4096 · 11008 ≈ **135M params - roughly 2/3 of the block**. (SwiGLU uses d_ff ≈ 2.7d with three matrices instead of the classic 4d with two - roughly parameter-neutral by design.)
- **Norms**: negligible (~2d each).

Times 32 blocks: ~6.5B. Plus **embeddings/LM head**: vocab × d = 32000 × 4096 ≈ 131M each (262M untied). The scaling insight: embedding params are *linear* in d while block params are *quadratic*, so vocab matters enormously for small models (a 1B model with a 128k vocab can spend >30% of params on embeddings - why small models tie weights and historically kept vocabs small) and is noise at 70B+.

**FLOPs**: training ≈ 6·N·D (forward 2ND + backward 4ND); inference forward pass ≈ 2·N per token - matrix-multiply params dominate. The critical caveat: **attention's QKᵀ and weights·V FLOPs scale with sequence length** (~per-token cost ∝ n·d per layer) and *aren't in N*. At short contexts (≤4k), MLPs dominate compute and 2N is accurate; at 100k+, attention score computation overtakes the parameter FLOPs - the crossover is why long-context prefill is expensive and why attention-efficiency work matters even though attention holds a minority of parameters.

Why this budget matters practically: (1) it explains why **MoE targets the MLP** - that's where the parameters are, so that's where conditional compute pays; (2) LoRA placement discussions and quantization sensitivity analyses are really conversations about this map; (3) interpretability's working hypothesis that MLPs store knowledge while attention routes it aligns with where the capacity sits; (4) at decode time the whole budget becomes a *bandwidth* budget - every parameter is read per token, so params ≈ bytes moved, which is why small-batch decode speed tracks model size in GB, not FLOPs.

**Follow-ups:** Derive the 6ND training-FLOP estimate. At what context length does attention compute overtake MLP compute for this architecture? How does GQA change the parameter and bandwidth budgets differently?

</details>

### 41. Open-weights vs closed-weights models: how do you think about the tradeoff as an engineer in 2026?

<details><summary><b>Answer</b></summary>

Frame it as an engineering decision with several axes, not an ideology question.

**Capability and velocity.** Frontier closed models (API-served: OpenAI, Anthropic, Google) generally lead on the hardest tasks - deep reasoning, long-horizon agentic work - with the gap to top open-weights models (Llama, Qwen, DeepSeek, Mistral lineages) repeatedly compressing to months on measurable benchmarks, then reopening at each frontier release. Practical rule: if your workload needs the frontier, closed usually wins today; if a 6-12-month-old capability level suffices - most production workloads: extraction, summarisation, classification, RAG answering, routine codegen - open weights are typically adequate and far cheaper per token when self-hosted at scale.

**Control and deployment.** Open weights give you: on-prem/VPC deployment for data-sovereignty, privacy, and regulated environments; full fine-tuning/distillation/quantization rights (subject to licence); pinned versions forever - no silent model drift under your evals, no deprecation on a vendor's schedule, no rate limits; logits/internals access (custom decoding, interpretability, research). Closed gives you: zero infra burden, immediate access to frontier capability, elastic scaling, and vendor-side safety/abuse tooling.

**Cost structure.** Closed = opex, linear in tokens, zero fixed cost - wins at low/spiky volume and lets you start instantly. Self-hosted open = GPU capacity + serving engineering (vLLM/SGLang/TensorRT-LLM, monitoring, upgrades) - wins at high sustained volume, especially with a distilled/fine-tuned small model tuned to one task. The crossover is a real calculation (utilisation matters more than list prices); many teams get it wrong in both directions.

**Risk axes.** Closed: vendor lock-in, model deprecations breaking prompt-tuned behaviour, data-handling contracts, price changes. Open: licence terms are not uniformly permissive (read them - "open weights" ≠ open source; training data and code usually stay closed either way), you own safety/red-teaming, and you own incidents.

**The 2026 default architecture** is pragmatic hybridity: frontier closed API for the hardest paths, cheap models (often open, often distilled) for high-volume paths, a router/gateway abstraction so models are swappable, and your own evals as the arbiter - because the honest answer to "which is better" is "against your workload, measured, this quarter."

**Follow-ups:** Sketch the break-even math for self-hosting a 70B-class model versus API pricing. What contractual/data-governance questions matter when sending regulated data to a closed API? How do you design a system so the model layer stays swappable?

</details>
