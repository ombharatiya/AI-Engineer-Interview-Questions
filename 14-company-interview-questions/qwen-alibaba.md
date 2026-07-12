# ☁️ Qwen (Alibaba) - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, technical reports, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- Qwen (Tongyi Qianwen) is built by **Tongyi Lab inside Alibaba Cloud**, so the loop is a **big-tech loop plus model-depth rounds**: an online assessment and algorithmic coding rounds like any large-company software role, then deeper rounds on LLM internals for the Qwen/Tongyi org specifically.
- Company-specific interview detail is **thin publicly** - the general Alibaba process is reasonably documented (OA, resume screen, two to three technical rounds, a hiring-manager round, an HR round), but Tongyi-Lab-specific stages are inference from the category. Everything process-related below is marked accordingly.
- Expect to be probed on **what Qwen actually ships**: byte-level multilingual tokenization, GQA and KV-cache economics, dense-vs-MoE architecture choices, hybrid thinking modes with a thinking budget, training-free long-context extension (YaRN + Dual Chunk Attention), and code/maths reasoning.
- Two flavours of role: **research/algorithm** (foundation-model pretraining, post-training/RL, multimodal, evaluation) and **applied/infra** (large-scale training and serving systems, Alibaba Cloud Model Studio / DashScope productisation). Both sit inside a large-company loop.
- Open-weights conviction matters here: Qwen is one of the most-downloaded open model families in the world. Have a real opinion on **why an at-scale cloud business ships Apache-2.0 weights**, and be fluent in Chinese-plus-multilingual and coding/maths performance as first-class product goals.

## Company context

Qwen (Tongyi Qianwen) is the large-language-model family built by Tongyi Lab, Alibaba Cloud's foundation-model group. The team ships on a fast open-weight cadence that regularly tops open leaderboards: the Qwen2.5 and Qwen3 general models, Qwen2.5-Coder for code, the Qwen-VL / Qwen2.5-VL vision-language line, and reasoning variants (QwQ and Qwen3's thinking mode), with strong multilingual (especially Chinese), coding, and maths performance. The models back Alibaba Cloud products (Model Studio / DashScope APIs, the Tongyi app) and a huge external developer ecosystem via Hugging Face and ModelScope. "AI engineer" here spans two worlds: an algorithm/research engineer close to pretraining, post-training RL, or multimodal work, and an applied/systems engineer owning training infrastructure, inference serving, and the cloud APIs that expose the models. Because the employer is Alibaba, a large-company hiring machine sits underneath the model-depth expectations.

## Roles & titles they hire

Sourced from Alibaba/Alibaba Cloud careers portals and the dedicated Tongyi recruitment site; exact titles vary by campus vs experienced hire and by region. Treat the specific archetypes as typical for this category where noted.

- **LLM / Foundation Model Algorithm Engineer** - pretraining, data, architecture, scaling (research track)
- **Post-training / Alignment / RL Researcher** - SFT, preference optimization, reasoning RL, reward design
- **Multimodal Algorithm Engineer** - vision-language (Qwen-VL), audio/omni, generation
- **Machine Learning Systems / Infra Engineer** - distributed training, inference serving, kernels, quantization
- **Applied / Product Engineer** - Model Studio / DashScope, agent and tool-use frameworks, developer platform
- **Evaluation / Data Engineer** - benchmarks, contamination control, data pipelines
- Plus conventional **Software Engineer** and **Alibaba Cloud** roles (platform, backend, campus hires)

Locations cluster in China (Hangzhou, Beijing) with some Alibaba Cloud roles in Singapore and other hubs. Alibaba runs distinct campus (new-grad) and experienced-hire tracks.

## The interview loop

Public, company-specific detail on the Tongyi/Qwen loop is thin. What is documented is the **general Alibaba process**; the Qwen-team-specific rounds are inferred from the role category (frontier open-weight lab inside a big-tech cloud). Treat the table as a reasonable map, not a confirmed script. Rows drawn from general Alibaba candidate reports are marked "(reported, varies)"; rows that are category inference are marked "(inferred)".

| Stage | Format | What's evaluated |
|---|---|---|
| Resume / HR screen | Recruiter call (reported, varies) | Background, motivation, "why Alibaba / why Qwen", role fit |
| Online assessment | Timed coding / aptitude, common for campus hires (reported, varies) | Data structures and algorithms, basic problem solving |
| Technical round 1-2 | Live coding, ~60 min each (reported, varies) | Algorithms and DS, language depth (Java/C++/Python), clean code, thinking aloud |
| Model-depth / domain round | Deep-dive discussion, possibly paper walk-through (inferred) | LLM internals, your past ML work, architecture and training tradeoffs |
| System / ML system design | Whiteboard-style (inferred, reported for senior roles) | Training-cluster or serving design, data pipelines, evaluation |
| Hiring-manager round | Hybrid technical + behavioural, ~60 min (reported, varies) | Project depth, ownership, collaboration, incident handling |
| HR / final round | Discussion (reported, varies) | Career goals, level fit, logistics |

Number of rounds and their order shift by track (campus vs experienced), team, and seniority. For an algorithm/research seat, weight your prep toward the model-depth and design rounds; for applied/infra, toward systems design and coding.

## What they emphasise

- **Model internals as shipped, not as taught.** Qwen's public differentiation is concrete: GQA, a ~151K multilingual byte-level BPE vocab, dense and MoE variants, hybrid thinking with a thinking budget, and training-free long-context extension. Expect "explain why Qwen did X" rather than textbook definitions.
- **Multilingual and Chinese-first thinking.** Tokenizer design, script coverage, and cross-lingual transfer are product concerns, not trivia. Qwen3 expanded language coverage substantially over Qwen2.5.
- **Coding and maths reasoning.** Qwen2.5-Coder and the reasoning line are flagship efforts. Repo-level code training, fill-in-the-middle, and verifiable-reward RL for maths/code are fair game.
- **Efficiency and serving economics.** As a cloud business, cost per token matters: KV-cache math, MoE active-vs-total parameters, quantization, and long-context memory show up because they are Alibaba Cloud's bill.
- **Open-weight strategy and evaluation trust.** Shipping Apache-2.0 weights that top leaderboards raises the bar on honest evaluation (contamination control) and on articulating the business logic of open releases.
- **Big-tech fundamentals still count.** Algorithms, data structures, and clean code gate the loop like any large-company role. Do not skip the LeetCode-style prep because it is a frontier lab.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Qwen uses a byte-level BPE tokenizer with a vocabulary around 151K, augmented for multilingual coverage and with digits split into single characters. Why those choices for a multilingual, maths-capable model, and what are the tradeoffs?

<details><summary><b>Answer</b></summary>

Start with the goal: one tokenizer that compresses Chinese, English, and dozens of other scripts reasonably well while not sabotaging arithmetic. **Byte-level BPE** guarantees there is no out-of-vocabulary failure: any Unicode text falls back to bytes, so rare CJK characters, emoji, and code symbols always encode. A **large vocab (~151K)** buys compression: more multilingual merges mean fewer tokens per sentence, which is fewer forward passes per character and better effective context for non-Latin scripts. Qwen's reported ratios are roughly 3-4 characters per token for English and denser for Chinese, so a bigger vocab directly lowers serving cost for Chinese-heavy traffic.

**Digit splitting** (each digit its own token) is a deliberate maths choice. If "1234" is one merged token, the model has to memorise arithmetic on opaque chunks; splitting into `1 2 3 4` exposes place value consistently, so carrying and long addition generalise far better. It costs a few extra tokens on numbers, which is a cheap price.

Tradeoffs: a large vocab inflates the embedding and output-projection matrices (vocab x hidden), which grows parameters and the softmax cost, and it needs enough multilingual data so rare tokens are actually trained. Byte fallback can fragment a rare script into many byte tokens, hurting compression for the least-resourced languages. From Qwen2.5 onward the family moved to a **unified vocabulary** shared across text, code, and multimodal subfamilies, which simplifies serving and lets special tokens (roles, tool calls, FIM markers) live in one namespace.

**Follow-ups:** How would you measure whether the tokenizer is fair across languages? Why does adding a new language after pretraining rarely mean just retraining the tokenizer?

</details>

### 2. Qwen3 unifies a "thinking" mode and a "non-thinking" mode in a single model, with a thinking budget the caller can set. How would you train that, and how would you serve it?

<details><summary><b>Answer</b></summary>

The product goal is one checkpoint that can do fast, cheap answers for easy queries and long chain-of-thought for hard ones, with the caller trading latency for accuracy via a budget. Qwen3's reported recipe is a **four-stage post-training pipeline**: (1) a **long chain-of-thought cold start** that teaches the model to produce structured reasoning traces; (2) **reasoning RL** that rewards correct final answers on verifiable maths and code so the reasoning actually pays off; (3) **thinking-mode fusion**, blending the reasoning model back together with non-thinking behaviour so one model supports both styles, typically gated by a control token or template; and (4) a **general RL** stage to polish helpfulness, safety, and formatting across the mixed distribution.

Serving: expose the mode as a flag plus a **thinking budget** (a token cap on the internal reasoning, reported up to tens of thousands of tokens). When the budget is small or zero, the model skips or truncates the thinking span and answers directly; when it is large, it can reason further before the answer. Practically the reasoning tokens sit between control markers so you can bill or hide them, and you can route by difficulty: cheap classifier or heuristics decide whether to spend budget at all.

The hard part is not regressing the fast path. Fusing a heavy-reasoning model with a terse one risks the model over-thinking trivial prompts (latency and cost blow up) or leaking reasoning style into simple answers. That is exactly why a later general-RL stage and careful mode gating exist. Alibaba publicly noted the unified toggle had rough edges, which is a useful, honest thing to be able to discuss.

**Follow-ups:** How would you stop the model from "thinking" on trivial prompts? How do you evaluate whether extra budget actually buys accuracy rather than just tokens?

</details>

### 3. Qwen moved from dense-only to shipping both dense and MoE models (for example a 30B model with ~3B active parameters, and a 235B model with ~22B active). Explain the tradeoff, and when you would pick the 30B-A3B MoE over a 32B dense.

<details><summary><b>Answer</b></summary>

In a sparse MoE, each transformer block's feed-forward layer is replaced by many expert FFNs plus a router that sends each token to a small top-k of them. So **total parameters** are large (all experts stored) but **active parameters per token** are small (only the routed experts run). The 30B-A3B model holds ~30B weights but executes ~3B per token, so its decode FLOPs and latency resemble a ~3B dense model while its quality benefits from the far larger parameter pool.

The catch is asymmetric economics. **FLOPs scale with active params; memory scales with total params.** You must hold all ~30B weights in VRAM even though you only compute 3B worth per token. So MoE buys quality-per-FLOP and throughput, not quality-per-gigabyte.

When to pick 30B-A3B over 32B dense: when you are **compute or throughput bound with memory to spare** - high-QPS serving where you want the accuracy of a bigger model but cannot afford 32B of active compute per token, and you have the VRAM (or expert-parallel sharding) to hold all experts. Pick the **32B dense** when memory is the binding constraint (single smaller GPU, edge, tight VRAM), when you want predictable per-token cost without router load-imbalance surprises, or when simplicity of deployment and fine-tuning matters. Dense is also friendlier to naive quantization and LoRA. Training MoE adds a load-balancing auxiliary loss (or the router collapses onto a few experts) and all-to-all communication for expert parallelism, a systems tax dense models never pay.

**Follow-ups:** Why is batched inference harder for MoE (expert imbalance inside a batch)? How does expert-choice vs token-choice routing change the load-balancing story?

</details>

### 4. Qwen3 uses "strong-to-weak" distillation, bootstrapping the smaller models from flagship ones instead of running the full heavy post-training on every size. How does that work and why is it cheaper?

<details><summary><b>Answer</b></summary>

The insight: the expensive part of post-training is the search - long-CoT construction and reasoning RL that discovers good reasoning behaviour. Once a flagship model has paid that cost, you do not need every small model to rediscover it from scratch. **Strong-to-weak distillation** transfers the behaviour of the large "teacher" (thinking and non-thinking) into the smaller "student" checkpoints.

Concretely it usually combines two signals. **On-policy / logit distillation**: the student learns to match the teacher's output distribution (soft targets carry more information than hard labels, teaching relative preferences over tokens, not just the argmax). And **data distillation**: the teacher generates high-quality reasoning traces and responses that become supervised fine-tuning data for the student, including both mode styles so the student inherits the hybrid thinking capability.

Why it is cheaper: reasoning RL needs rollouts, reward computation, and many optimization steps at each model scale, and it is unstable and compute-heavy. Distillation replaces most of that with straightforward supervised or logit-matching objectives, which converge faster and more stably, and you generate the teacher data once and reuse it across all student sizes. Reported outcome: the small Qwen3 models reach strong performance for far less compute than running full RL at each size would take.

Risks to name: the student is capped by the teacher (you cannot distill capability the teacher lacks), distillation can transfer the teacher's biases and mistakes, and pure imitation without any RL can leave the student worse at exploration-sensitive tasks. In practice you often do a light RL or preference stage on top to recover the last bit.

**Follow-ups:** When does logit distillation beat SFT on teacher outputs, and when is it not worth the extra plumbing? How would you detect that the student has simply memorised teacher traces?

</details>

### 5. Qwen2.5 extends context to 128K (and up to about 1M for the Turbo variant) using YaRN plus Dual Chunk Attention, mostly training-free. Explain how that works and why post-hoc extension is attractive.

<details><summary><b>Answer</b></summary>

The core problem is RoPE: a model pretrained at, say, 32K tokens has never seen the rotary phases that correspond to positions far beyond that, so naive extrapolation to 128K produces garbage attention. The Qwen approach combines two training-free tricks.

**YaRN** rescales the RoPE frequencies so the effective positions at inference stay inside the range the model was trained on. Rather than uniformly stretching all frequencies (which blurs local, high-frequency structure), YaRN interpolates the low frequencies (long-range) more than the high ones and adds an attention-temperature correction, so long-range positions become representable without destroying short-range resolution.

**Dual Chunk Attention (DCA)** attacks the same problem from the attention side. It splits the long sequence into chunks and remaps relative positions so that no two tokens ever appear farther apart than the pretraining length. It uses distinct patterns: intra-chunk attention (original relative positions within a chunk), inter-chunk attention (positions across chunks kept in-range), and successive-chunk handling for continuity at boundaries. Together they let a model trained short attend coherently over very long inputs.

Why post-hoc is attractive: training natively at 128K or 1M is brutally expensive - attention memory and compute grow with sequence length, so long-context pretraining is often the single most costly thing you can do. Training-free extension gets most of the capability by adjusting positional handling at inference plus light long-context fine-tuning, at a fraction of the cost, and lets one base model serve multiple context tiers. The tradeoff is that extrapolated long-context quality still trails a natively long-trained model, and effective recall past the window degrades, so you validate with retrieval-style long-context evals, not just perplexity.

**Follow-ups:** Why does KV-cache memory, not FLOPs, often become the real 1M-token bottleneck? How would you test whether the model truly uses information 800K tokens back rather than just not crashing?

</details>

### 6. Implement grouped-query attention in PyTorch and explain where the KV-cache savings come from, since Qwen relies on GQA for serving efficiency.

<details><summary><b>Answer</b></summary>

GQA sits between full multi-head attention (one KV head per query head) and multi-query attention (one KV head total): query heads are split into groups, and each group shares one KV head. Qwen uses this to shrink the KV cache without the quality hit of full MQA.

```python
import torch, torch.nn.functional as F

def gqa(x, wq, wk, wv, wo, n_heads, n_kv_heads):
    B, T, D = x.shape
    hd = D // n_heads
    q = (x @ wq).view(B, T, n_heads, hd).transpose(1, 2)       # B, H, T, hd
    k = (x @ wk).view(B, T, n_kv_heads, hd).transpose(1, 2)    # B, Hkv, T, hd
    v = (x @ wv).view(B, T, n_kv_heads, hd).transpose(1, 2)
    rep = n_heads // n_kv_heads              # query heads per KV head
    k = k.repeat_interleave(rep, dim=1)      # expand KV to match query heads
    v = v.repeat_interleave(rep, dim=1)
    att = (q @ k.transpose(-2, -1)) / hd**0.5
    mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1)
    att = att.masked_fill(mask, float("-inf"))
    out = F.softmax(att, dim=-1) @ v          # B, H, T, hd
    return out.transpose(1, 2).reshape(B, T, D) @ wo
```

The savings: the KV cache stores keys and values for every past token, sized `2 * n_kv_heads * hd * seq_len` per layer. With MHA that is `n_kv_heads == n_heads`; GQA sets `n_kv_heads` much smaller (say 8 KV heads for 32 query heads), a 4x cache reduction. That matters because **decode is memory-bandwidth bound**: at each step you read the whole KV cache to attend, so a smaller cache means less bandwidth per token, larger batch sizes, and longer contexts on the same GPU. Note the cache is stored *before* the `repeat_interleave` (you keep the compact KV), and production kernels avoid materialising the repeat by indexing. Real serving uses `F.scaled_dot_product_attention` or FlashAttention for the fused kernel; this version is for clarity.

**Follow-ups:** Add the single-token decode path with a growing KV cache. Where does RoPE get applied, and why to q and k only, not v?

</details>

### 7. Qwen2.5-Coder trains with repository-level fill-in-the-middle using special tokens like `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>`, `<|repo_name|>`, and `<|file_sep|>`. Write the function that formats a repo-level FIM training example, and explain why repo-level beats file-level for real code completion.

<details><summary><b>Answer</b></summary>

FIM teaches the model to fill a gap given both left and right context, which is what an editor autocomplete actually needs (you have code before *and* after the cursor). The trick is to reorder: put prefix and suffix first, then have the model predict the middle. Repo-level FIM extends this across files so the model can use imports and definitions from elsewhere in the project.

```python
def format_repo_fim(repo_name, files, target_idx, cut_a, cut_b):
    # files: list of (path, content). Split the target file into pre/mid/suf.
    path, content = files[target_idx]
    pre, mid, suf = content[:cut_a], content[cut_a:cut_b], content[cut_b:]
    parts = [f"<|repo_name|>{repo_name}"]
    for i, (p, c) in enumerate(files):
        if i == target_idx:
            parts.append(
                f"<|file_sep|>{p}\n"
                f"<|fim_prefix|>{pre}<|fim_suffix|>{suf}<|fim_middle|>{mid}"
            )
        else:
            parts.append(f"<|file_sep|>{p}\n{c}")   # context files verbatim
    return "".join(parts) + "<|endoftext|>"
```

At training time the loss is on the whole sequence (or focused on the middle); at inference you feed everything up to `<|fim_middle|>` and let the model generate the missing span. The special tokens matter because they are unambiguous structural signals the model learns to key on: `<|repo_name|>` and `<|file_sep|>` mark project and file boundaries so cross-file references are learnable, and the FIM markers tell the model this is an infilling task, not left-to-right continuation.

Why repo-level wins: real completions depend on symbols defined in *other* files - a function you call, a type you import, a config constant. File-level training caps the model's world at one file, so it hallucinates signatures. Repo-level pretraining (reported around 32K-token context with long-context repo data) lets the model actually read the surrounding project, which is the difference between guessing an API and using the real one. The cost is longer sequences and careful data construction (ordering files, avoiding leakage of the answer into context).

**Follow-ups:** How would you order context files so the most relevant ones survive context truncation? Why can naive FIM masking accidentally leak the middle into the suffix, and how do you prevent it?

</details>

### 8. Qwen2.5-VL uses a native dynamic-resolution ViT with window attention and multimodal RoPE (MRoPE). Why native resolution instead of fixed-size tiling, and what does MRoPE encode?

<details><summary><b>Answer</b></summary>

Traditional vision-language models resize every image to a fixed square (224 or 336) or tile it into fixed crops. That throws away information: a wide document, a tall screenshot, or a high-resolution chart gets squashed or chopped, and the model loses aspect ratio and real-world scale. Qwen2.5-VL trains a **native dynamic-resolution ViT** that processes images at their actual spatial scale, producing a variable number of visual tokens proportional to image size. Big detailed images yield more tokens (more detail preserved), small images yield fewer (less waste). This is what lets the model do fine-grained tasks like reading small text, grounding boxes, and parsing documents where absolute and relative size matter.

The cost of variable, potentially large token counts is compute, so the ViT uses **window attention** in most layers: attention is restricted to local windows rather than full-image global attention, keeping cost roughly linear in the number of patches instead of quadratic, with a few full-attention layers to mix globally. That is the standard efficiency lever that makes native high resolution affordable.

**MRoPE (multimodal RoPE)** generalises rotary position embeddings from a single 1D text position to multiple coordinate axes: it encodes position along temporal, height, and width dimensions. For an image, a patch's position carries its 2D (row, column) location; for video, it also carries a temporal index, and Qwen2.5-VL couples that with dynamic FPS sampling so long videos are sampled sparsely and short clips densely. The payoff is that the language backbone gets genuine spatial and temporal structure - it can reason about where things are and when they happen, not just an unordered bag of visual tokens - while sharing one positional scheme with the text stream so the modalities align.

**Follow-ups:** How does variable token count per image complicate batching and serving? Why is native resolution especially important for OCR and grounding versus, say, image captioning?

</details>

### 9. Qwen's reasoning models are trained with reinforcement learning using verifiable rewards on maths and code. Explain that setup and why it is preferred over PPO with a learned reward model for these domains.

<details><summary><b>Answer</b></summary>

The core idea (RL with verifiable rewards, RLVR) is that for maths and code you do not need a learned reward model at all: correctness is checkable. For a maths problem you compare the final answer to ground truth; for code you run unit tests. That check is the reward - 1 if the answer is right or the tests pass, 0 otherwise (sometimes with partial credit). The policy generates a full reasoning trace and answer, gets the binary/graded reward, and RL pushes it toward reasoning paths that lead to correct answers.

Why this beats PPO with a learned reward model here: a learned reward model is a **proxy**, and policies are ruthless at exploiting proxy errors (reward hacking) - producing confident, well-formatted, wrong answers the reward model happens to like. A verifier that actually executes the code or checks the number is grounded truth, so there is far less to hack, and it removes the cost and drift of training and maintaining a separate reward model. It also scales cleanly: you can generate huge amounts of maths/code problems with automatic checkers.

On the algorithm side, group-relative methods (sampling several completions per prompt and using their relative rewards as the advantage) are attractive because they **drop the value/critic network**: with a verifiable 0/1 reward and a group baseline, you avoid the instability and memory of a learned value head that plain PPO needs. That makes large-scale reasoning RL cheaper and more stable.

Limits worth naming: verifiable rewards only exist where you can check answers, so this does not directly cover open-ended writing or subjective helpfulness (hence a separate general-RL stage). Sparse 0/1 rewards on very hard problems give little signal, so curriculum and reward shaping matter, and you must guard against the model gaming the checker (for example printing the expected output).

**Follow-ups:** How would you stop a code policy from hard-coding test outputs to pass the checker? When does a learned reward model still earn its keep despite the hacking risk?

</details>

### 10. Qwen ships open weights that top public leaderboards. As the engineer responsible for a release, how do you make sure the benchmark numbers are trustworthy and not contaminated?

<details><summary><b>Answer</b></summary>

Contamination - test data leaking into pretraining - is the single biggest threat to a leaderboard-topping open release, because your credibility is the product. The defence is layered.

**Prevention first.** Run **decontamination** on the pretraining and post-training corpora: n-gram or embedding-based overlap detection against the eval sets you care about (maths, code, knowledge benchmarks), and remove or flag matches. This is imperfect (paraphrases and translations slip through, especially for a multilingual model where a benchmark may exist in several languages), so treat it as reducing, not eliminating, risk.

**Detection and honesty.** Report results on **held-out and freshly-collected** evals, not just static public sets that have been on the internet for years and are almost certainly in everyone's training data. Use benchmarks with private test splits or rolling/time-gated versions where possible. Run contamination probes: check whether the model can complete verbatim held-back test items, or whether performance collapses on perturbed versions of the same questions (rename variables, change numbers) - a big drop signals memorisation rather than capability.

**Broaden the signal.** No single number should carry a release. Combine automatic benchmarks with human evaluation and, ideally, **third-party arena-style** comparisons the team does not control, plus real task evals (agentic, long-context, tool-use) that are harder to game than static multiple-choice. Watch for the classic tell: a model that is amazing on the reported benchmark and mediocre in the wild.

**Process.** Freeze eval code and prompts, publish the methodology and settings (few-shot count, decoding, chat template) so results are reproducible, and version everything. For an open-weights team, reproducibility by outsiders is itself the trust mechanism: if the community can rerun your numbers, contamination gets caught fast.

**Follow-ups:** Why is contamination especially insidious for a multilingual model? How would you design an eval that stays meaningful six months after release?

</details>

### 11. A standard Alibaba coding round. Design a data structure for a fixed-capacity cache that supports get and put in O(1) and evicts the least-recently-used entry when full. Implement it in Python.

<details><summary><b>Answer</b></summary>

This is the classic LRU cache, and it is worth knowing cold because the algorithmic rounds gate the whole loop regardless of how senior the model work is. The requirement is O(1) for both operations, which rules out scanning for the least-recently-used item. The standard answer is a **hash map plus a doubly linked list**: the map gives O(1) lookup by key, and the linked list keeps entries in recency order so eviction is O(1) at the tail and promotion on access is O(1) by splicing.

```python
class Node:
    __slots__ = ("k", "v", "prev", "next")
    def __init__(self, k=0, v=0):
        self.k, self.v, self.prev, self.next = k, v, None, None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}                      # key -> Node
        self.head, self.tail = Node(), Node()   # sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, n):
        n.prev.next, n.next.prev = n.next, n.prev

    def _push_front(self, n):              # most-recently-used at front
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        n = self.map[key]
        self._remove(n); self._push_front(n)
        return n.v

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            n = self.map[key]; n.v = value
            self._remove(n); self._push_front(n)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev            # evict at tail
            self._remove(lru); del self.map[lru.k]
        n = Node(key, value)
        self.map[key] = n; self._push_front(n)
```

Sentinel head/tail nodes remove the null-checking edge cases that trip people up under time pressure. In Python you could also use `collections.OrderedDict` with `move_to_end` and `popitem(last=False)` for a shorter answer, but interviewers usually want the underlying mechanism, so I would code the linked list and mention the shortcut. Complexity: O(1) time per operation, O(capacity) space.

**Follow-ups:** Extend it to LFU (least-frequently-used) - what changes? How does this relate to KV-cache eviction policies in long-context serving?

</details>

### 12. Alibaba open-sources Qwen under Apache 2.0 while running a commercial cloud business. Walk me through the strategy, and tell me about a time you owned an ambiguous technical decision end to end.

<details><summary><b>Answer</b></summary>

This is a hybrid strategy-plus-behavioural question, and both halves matter here. On strategy, the honest business case for open weights from a cloud company: **open models are demand generation for the cloud**. Every developer who builds on Qwen is a candidate to run it on Alibaba Cloud (Model Studio / DashScope) or to buy the hosted, larger, or managed variants. Open weights build ecosystem gravity, standardise the world on your architecture and tokenizer, attract external contributions and talent, and generate an enormous free evaluation and bug-finding loop. It also reframes competition: against closed frontier labs, being the default *open* choice is a defensible position, especially internationally and in markets sensitive to vendor lock-in. The tradeoff is that you give away the weights, so your moat shifts to scale, serving efficiency, the newest/biggest closed variants, data, and the cloud platform around the model. Being able to argue this crisply signals you understand why your work exists commercially, not just technically.

For the ownership half, use STAR and pick a real story where the requirements were genuinely unclear and you drove to a decision: frame the ambiguity (conflicting goals, no obvious right answer), the options you weighed with their tradeoffs, the data or experiments you used to decide, the call you made, and - critically - how you measured whether it worked and what you would change. Large AI orgs weight ownership, cross-team collaboration, and incident handling heavily in the hiring-manager round, so land the "I owned it, including the parts that went wrong" note rather than a tidy success story. Keep it concrete and quantified.

**Follow-ups:** Where is the open-weight strategy weakest, and what would change your mind? Tell me about a decision of yours that turned out wrong and how you caught it.

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - the highest-leverage dir for the model-depth rounds. Own attention variants (MHA/GQA/MQA), RoPE and long-context extension (YaRN, DCA), MoE routing and load balancing, tokenization, and the dense-vs-MoE tradeoff. Be able to implement, not just describe.
2. **[12-coding-challenges](../12-coding-challenges/)** - do not skip this. The Alibaba loop gates on algorithms and data structures like any big-tech role; grind the standard patterns (arrays, graphs, DP, LRU/heap-style design) in Python or Java.
3. **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - SFT, preference optimization, and reasoning RL with verifiable rewards (RLVR) and group-relative methods; this is Qwen's post-training core, plus the thinking-mode / distillation story.
4. **[08-inference-and-production](../08-inference-and-production/)** - KV-cache math, continuous batching, quantization, MoE serving, long-context memory. As a cloud business, serving economics are interview-relevant.
5. **[10-multimodal](../10-multimodal/)** - vision-language architecture (native dynamic resolution, MRoPE, window attention) for Qwen-VL-adjacent roles.
6. **[11-ai-system-design](../11-ai-system-design/)** - use the framework for "design LLM training/serving" and "design a code-completion system" prompts. Closest existing case study: **[AI code assistant](../11-ai-system-design/case-studies/02-ai-code-assistant.md)** - it maps directly onto Qwen2.5-Coder's repo-level FIM, latency, and context-assembly problems.
7. **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - contamination control and trustworthy benchmarking, which matter disproportionately for a leaderboard-topping open-weights team.

Company-specific moves:

- **Read the Qwen technical reports** (Qwen2, Qwen2.5, Qwen3, Qwen2.5-Coder, Qwen2.5-VL, and the Qwen2.5-1M long-context report, all on arXiv). Being fluent in their specific choices - 151K multilingual tokenizer, GQA, hybrid thinking, four-stage post-training, YaRN + DCA, repo-level FIM - covers a large fraction of any model-depth round.
- **Actually run a Qwen model** from Hugging Face or ModelScope: quantize it, serve it (vLLM), try thinking vs non-thinking mode and the thinking budget, and use Qwen2.5-Coder for FIM completion. Hands-on beats book knowledge in a lab that ships weights.
- **Use the products**: Alibaba Cloud Model Studio / DashScope APIs and the Tongyi app, so you can speak to the productisation side.
- **Prepare the big-tech behavioural round** with STAR stories on ownership, cross-team collaboration, and incident response, and have a crisp view on the open-weights-plus-cloud business strategy.
- **Refresh multilingual and Chinese-first framing**: tokenizer fairness, cross-lingual transfer, and why Chinese/maths/coding are first-class product goals for this team.

## Sources

- [Alibaba Group careers](https://careers.alibaba.com/) and [Alibaba Cloud careers](https://careers.alibabacloud.com/) - official role portals and campus vs experienced tracks
- [Tongyi Lab recruitment site](https://careers-tongyi.alibaba.com/) - dedicated Qwen/Tongyi hiring page (role archetypes; page is JS-rendered, so titles here are described as typical for the category)
- [Qwen3 Technical Report (arXiv)](https://arxiv.org/abs/2505.09388) - dense and MoE sizes, hybrid thinking + thinking budget, four-stage post-training, strong-to-weak distillation, 119-language coverage, Apache 2.0
- [Alibaba: Qwen3 hybrid reasoning announcement](https://www.alibabacloud.com/blog/alibaba-introduces-qwen3-setting-new-benchmark-in-open-source-ai-with-hybrid-reasoning_602192) - official framing of thinking modes and thinking budget
- [Qwen2.5 Technical Report (arXiv)](https://arxiv.org/abs/2412.15115) and [Qwen2.5-1M report (arXiv)](https://arxiv.org/abs/2501.15383) - tokenizer, long-context extension (YaRN, DCA)
- [Qwen2.5-Coder Technical Report (arXiv)](https://arxiv.org/abs/2409.12186) - file-level vs repo-level FIM, special tokens
- [Qwen2.5-VL Technical Report (arXiv)](https://arxiv.org/abs/2502.13923) - native dynamic-resolution ViT, window attention, MRoPE
- [Qwen documentation - key concepts](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html) - tokenizer vocabulary and unified-vocab details
- [SCMP: inside Tongyi Lab](https://www.scmp.com/tech/big-tech/article/3330653/meet-young-talent-scaling-alibabas-ai-future-tongyi-lab-developer-qwen-models) - team context and open-source strategy
- [Alibaba Software Engineer interview guide (Interview Query)](https://www.interviewquery.com/interview-guides/alibaba-software-engineer) and [Glassdoor Alibaba interviews](https://www.glassdoor.com/Interview/Alibaba-Group-Software-Engineer-Interview-Questions-EI_IE225974.0,13_KO14,31.htm) - general Alibaba loop (OA, coding rounds, HM and HR rounds); not Tongyi/Qwen-specific

*Note: company-specific interview detail for the Qwen/Tongyi team is thin in public sources. Process claims above lean on the general Alibaba loop and are marked as reported or inferred; model-depth content is grounded in Qwen's public technical reports.*
