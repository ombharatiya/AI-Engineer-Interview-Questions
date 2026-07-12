# ML & Deep Learning Foundations - Interview Questions

32 questions: 10 basic, 13 intermediate, 9 advanced.

## Basic

### 1. Explain the bias-variance tradeoff. How do you tell which one is hurting your model?

<details><summary><b>Answer</b></summary>

Expected test error decomposes into three parts: **bias²** (error from a model too simple to represent the true function), **variance** (error from sensitivity to the particular training sample - fitting noise), and irreducible noise. A linear model on a nonlinear problem has high bias; a deep net trained on 500 examples has high variance.

You diagnose it from the **train/val gap**, not from theory:

- High train error ≈ high val error → high bias (underfitting). Fixes: bigger/richer model, more features, train longer, reduce regularization.
- Low train error, much higher val error → high variance (overfitting). Fixes: more data, regularization (weight decay, dropout, early stopping), augmentation, smaller model as a last resort.

Learning curves sharpen the diagnosis: if val error is still falling as you add data, more data helps (variance problem); if train and val curves have plateaued together at a bad level, more data won't help (bias problem).

A strong candidate adds the modern caveat: the classical U-shaped "more capacity → more overfitting" curve breaks down for heavily overparameterized networks. **Double descent** (Belkin et al.; Nakkiran et al.) shows test error can *decrease again* past the interpolation threshold - which is consistent with the empirical reality that scaling up transformers improves generalization. So "your model is too big" is rarely the right first hypothesis in deep learning; data quality, leakage, and training recipe usually matter more.

**Follow-ups:** Your val loss is much lower than train loss - what could cause that? (Dropout active only at train time, augmentation on train only, easier val distribution.) How does regularization move you along the tradeoff? Where does double descent leave the classical picture?

</details>

### 2. How do you detect overfitting and underfitting in practice, and what do you do about each?

<details><summary><b>Answer</b></summary>

Watch train and validation loss over training. **Underfitting**: both losses are high and close together, or train loss is still steadily decreasing when you stop - the model hasn't extracted the available signal. **Overfitting**: train loss keeps falling while val loss plateaus and then rises - the model is memorizing.

For underfitting: increase capacity (width/depth/params), improve features or input representation, train longer, raise the learning rate if optimization is stalling, reduce regularization strength.

For overfitting, in rough order of preference:
1. **More or better data** - almost always the highest-leverage fix.
2. **Data augmentation** - cheap synthetic diversity.
3. **Regularization** - weight decay, dropout, label smoothing.
4. **Early stopping** - checkpoint on val loss, keep the best.
5. Reduce model size - usually the last resort in deep learning.

Karpathy's training recipe is the practical framing interviewers like: first *deliberately overfit* a small batch to near-zero loss to prove the model and pipeline can learn at all, then regularize back toward generalization. If you can't overfit 100 examples, you have a bug, not a regularization problem.

Two traps worth naming: (1) a val loss that's suspiciously *better* than expected often means leakage, not brilliance; (2) in LLM fine-tuning, "overfitting" often shows up as behavioural regressions (loss on the SFT set drops while general capability degrades - catastrophic forgetting), so you monitor held-out capability evals, not just the fine-tuning loss.

**Follow-ups:** Why start by overfitting a single batch? Your SFT loss is decreasing nicely but users say the model got worse - what happened? When would you accept some overfitting deliberately?

</details>

### 3. Compare L1 and L2 regularization. Why does L1 produce sparse weights?

<details><summary><b>Answer</b></summary>

Both add a penalty on weight magnitude to the loss. **L2** adds λ‖w‖², shrinking all weights proportionally toward zero but rarely *to* zero. **L1** adds λ‖w‖₁ and drives many weights exactly to zero, performing implicit feature selection.

Why sparsity: the L1 penalty's gradient is a constant ±λ regardless of the weight's size, so it keeps pushing small weights all the way to zero, where the subgradient lets them stay; L2's pull is proportional to w, so it weakens as weights shrink and never quite finishes the job. Geometrically, the L1 ball has corners on the axes, and the loss contour typically first touches the constraint region at a corner - where some coordinates are exactly zero.

The Bayesian view is a good differentiator: L2 = MAP estimation with a **Gaussian prior** on weights; L1 = MAP with a **Laplace prior** (sharper peak at zero, heavier tails).

In practice: L1 matters for linear models and feature selection (lasso); deep learning almost exclusively uses L2-style **weight decay**. One subtlety that sets up a later question: with adaptive optimizers like Adam, adding L2 to the loss is *not* equivalent to weight decay - the penalty gets rescaled by the per-parameter adaptive term. That's exactly the bug AdamW fixes by decoupling the decay from the gradient update. Also note common practice: no weight decay on biases or LayerNorm gains, since they're low-dimensional and decaying them just distorts activations.

**Follow-ups:** What's elastic net and when would you use it? Why is L2-in-the-loss different from weight decay under Adam? Why exclude LayerNorm parameters from weight decay?

</details>

### 4. How does dropout work - and what changes between training and inference?

<details><summary><b>Answer</b></summary>

During training, dropout independently zeroes each activation with probability p (commonly 0.1-0.5), forcing the network not to rely on any single unit and breaking co-adaptation. It's often described as training an implicit ensemble of exponentially many thinned subnetworks that share weights.

The train/inference asymmetry is the part interviewers actually probe. With **inverted dropout** (what every modern framework implements), surviving activations are scaled by 1/(1−p) *at training time*, so the expected activation magnitude matches between train and inference - at inference, dropout is simply disabled and no rescaling is needed. The classic bug: forgetting `model.eval()` in PyTorch, so dropout stays active in production and predictions are noisy and degraded. (The same call also switches BatchNorm to running statistics - two bugs for the price of one.)

```python
mask = (torch.rand_like(x) > p).float()
x = x * mask / (1 - p)   # inverted dropout: rescale at train time
```

Where it's used today: the original Transformer applied dropout to each sub-layer's output before the residual add and to the embedding sums (p=0.1); standard implementations also drop attention weights. But large-scale LLM *pretraining* typically uses dropout of 0 - with a massive, single-epoch data stream there's little memorization pressure, and dropout just wastes capacity. It reappears in fine-tuning, where datasets are small: LoRA setups commonly apply dropout ~0.05-0.1 to the adapter inputs.

Variants worth naming if asked: DropPath/stochastic depth (drop whole residual branches, common in vision transformers) and Monte Carlo dropout (keep dropout on at inference and sample repeatedly for a crude uncertainty estimate).

**Follow-ups:** Why do large pretraining runs set dropout to 0? What does `model.eval()` change besides dropout? How would you use MC dropout to get uncertainty estimates?

</details>

### 5. Walk me through train/validation/test splits. When do you use cross-validation, and when is it a bad idea?

<details><summary><b>Answer</b></summary>

Three sets, three jobs: **train** fits parameters, **validation** drives all the choices you make between runs (hyperparameters, architecture, checkpoint selection, early stopping), and **test** estimates generalization *once*, at the end. Every decision you make while looking at a set "spends" it - tune against the test set enough times and it silently becomes a second validation set, and your reported number is optimistic.

**k-fold cross-validation** (typically k=5 or 10) rotates the validation fold and averages, giving a lower-variance estimate when data is scarce - standard for classical ML on thousands of rows. Use **stratified** k-fold for imbalanced classes so each fold preserves prevalence.

When CV is wrong or impractical:
- **Deep learning at scale** - training 5× is prohibitively expensive; a single held-out set is standard, and with millions of examples its variance is fine.
- **Time series** - random folds leak the future into training. Use temporal splits: train on the past, validate on the future (walk-forward validation).
- **Grouped data** - if the same user/patient/document appears in multiple rows, split by group ID, or the model recognises entities instead of generalizing.

For LLM work the same discipline shows up as: held-out eval suites you don't train on, decontamination of pretraining data against benchmarks, and keeping a fresh, never-optimised-against eval for final go/no-go decisions - because prompt tuning against an eval overfits it exactly like hyperparameter tuning overfits a val set.

**Follow-ups:** How does the same-user-in-both-splits failure actually look in the metrics? What's nested cross-validation for? How would you decontaminate an LLM eval set?

</details>

### 6. Explain precision, recall, and F1. Give a concrete case where 99% accuracy means the model is useless.

<details><summary><b>Answer</b></summary>

From the confusion matrix: **precision** = TP/(TP+FP) - of everything flagged positive, what fraction was right; **recall** = TP/(TP+FN) - of all true positives, what fraction was found; **F1** = 2PR/(P+R), the harmonic mean, which punishes imbalance between the two (harmonic, so a model with P=1.0, R=0.01 gets F1≈0.02, not 0.5).

Accuracy lies whenever classes are imbalanced. Fraud at 1% prevalence: the constant classifier "not fraud" scores 99% accuracy and catches zero fraud - recall 0. Any headline accuracy must be compared against the majority-class baseline.

Which metric to optimise is a *cost* question, not a math question:
- False positives expensive (spam filter eating real mail, police alerts) → prioritise precision.
- False negatives expensive (cancer screening, fraud, safety filters) → prioritise recall.
- Use **F-beta** to encode the ratio explicitly: F2 weights recall higher, F0.5 weights precision higher.

Also know that precision/recall/F1 are **threshold-dependent** - they describe one operating point on the classifier's score distribution. Reporting "F1 = 0.83" without saying how the threshold was chosen (and on which split) is a red flag; sweep the threshold on validation data and pick the operating point that matches the product's cost structure.

This vocabulary transfers directly to LLM evals: hallucination detection, toxicity filtering, and RAG retrieval are all precision/recall problems (retrieval's recall@k is literally recall), and interviewers expect you to move fluently between the classic and LLM framings.

**Follow-ups:** Why the harmonic mean rather than arithmetic? Precision is 0.95 but the product team is unhappy - what would you check? How do micro- vs macro-averaged F1 differ on imbalanced multiclass?

</details>

### 7. What's the difference between parameters and hyperparameters? How do you tune hyperparameters efficiently?

<details><summary><b>Answer</b></summary>

**Parameters** are learned from data by the optimizer - weights, biases, embedding tables. A 7B-parameter LLM has 7 billion of them. **Hyperparameters** are set *before* training and control the learning process: learning rate, batch size, weight decay, dropout rate, architecture choices (depth, width, number of heads), warmup steps, LoRA rank. A quick sanity check interviewers like: a `Linear(in=4096, out=11008)` layer has 4096×11008 weights + 11008 biases ≈ 45M parameters.

Tuning approaches, in order of sophistication:
- **Grid search** - exhaustive over a discrete grid; wasteful in high dimensions.
- **Random search** - Bergstra & Bengio showed it beats grid search because typically only a few hyperparameters matter, and random sampling explores each dimension's marginal far better for the same budget.
- **Bayesian optimization / successive halving** (Optuna, ASHA/Hyperband) - model the response surface or aggressively kill bad trials early; the practical default for expensive training runs.

Practical guidance a senior candidate gives: learning rate is almost always the highest-impact hyperparameter - search it on a **log scale** (e.g., 1e-5 to 1e-3). Tune on a smaller proxy (subset of data, shorter run, smaller model) and transfer; this is the idea μP (μTransfer) makes principled for scaling model width. Don't tune everything at once - fix a sensible recipe (AdamW, cosine schedule, decay 0.1) and sweep the 2-3 knobs that matter. And every tuning decision must be made on validation data, never test.

**Follow-ups:** Why sample learning rate log-uniformly? If you can afford 20 runs, how do you allocate them? Is the number of training epochs a parameter or hyperparameter - and what about a learned temperature like CLIP's?

</details>

### 8. What's the difference between batch, mini-batch, and stochastic gradient descent? What does batch size actually change?

<details><summary><b>Answer</b></summary>

**Batch GD** computes the exact gradient over the full dataset per step - accurate but one slow step per epoch and infeasible at scale. **SGD** (strictly, single-example) updates on one sample - very noisy, poor hardware utilisation. **Mini-batch GD** - what everyone actually runs - averages the gradient over a batch (dozens to millions of tokens), balancing gradient quality against throughput. Confusingly, practitioners call mini-batch training "SGD" too.

What batch size changes:

- **Gradient noise**: variance of the gradient estimate scales ~1/batch size. Some noise is useful - it acts as implicit regularization and helps escape sharp minima; very large batches can generalize slightly worse without recipe adjustments.
- **LR coupling**: bigger batches support (and need) larger learning rates. The **linear scaling rule** (multiply LR by k when multiplying batch by k, plus warmup) comes from Goyal et al.'s "ImageNet in 1 hour" work. Beyond a problem-dependent **critical batch size** (McCandlish et al., gradient-noise-scale analysis), extra batch parallelism stops buying faster convergence - you're just averaging already-clean gradients.
- **Hardware**: larger batches improve accelerator utilisation; LLM pretraining uses enormous global batches (order of millions of tokens) via data parallelism, and **gradient accumulation** simulates large batches when memory is tight.

The interview trap: "bigger batch is always better." It isn't - per-step cost grows, per-step progress saturates past the critical batch size, and memory is finite. Batch size is a systems-and-optimization tradeoff, not a free knob.

**Follow-ups:** You double the batch size - what do you do to the learning rate and why? What is gradient accumulation actually equivalent to, and where does the equivalence break (hint: BatchNorm)? Why might a huge batch hurt generalization?

</details>

### 9. What are embeddings? Compare cosine similarity, dot product, and Euclidean distance - when does the choice matter?

<details><summary><b>Answer</b></summary>

An embedding is a learned dense vector (typically 256-4096 dims) where geometry encodes semantics: similar items map to nearby points. They're produced by an encoder trained so that a chosen similarity function scores related pairs highly - words, sentences, images, users, code.

The three similarity measures:
- **Dot product** a·b - rewards both alignment *and* magnitude. A long vector can dominate rankings regardless of direction.
- **Cosine** = a·b / (‖a‖‖b‖) - direction only; equivalent to dot product on unit-normalized vectors.
- **Euclidean** ‖a−b‖ - for unit vectors, ‖a−b‖² = 2 − 2·cos(a,b), so it's monotonically equivalent to cosine and produces identical rankings.

So on normalized vectors all three agree on ranking; the choice only matters when magnitudes carry information. The senior-engineer answer: **use the similarity the model was trained with**. Most modern text embedders (OpenAI text-embedding-3, Cohere, E5/GTE/BGE-style open models) are trained with cosine-based contrastive objectives and often ship pre-normalized vectors. Some retrieval models deliberately use raw dot product so magnitude can encode confidence or importance.

Operationally, your vector index metric must match: FAISS/pgvector/HNSW indexes are built for inner product, L2, or cosine, and a mismatch silently degrades retrieval quality. Two more advanced points worth volunteering: raw LLM hidden states are **anisotropic** (squashed into a narrow cone), which is why you use a contrastively trained embedder rather than pooling base-model activations; and **Matryoshka (MRL) embeddings** are trained so truncating to the first k dims still works, letting you trade recall for memory/latency.

**Follow-ups:** Why does normalizing make Euclidean and cosine equivalent - show it. When would dot product beat cosine in a recommender? What breaks if you index cosine-trained embeddings with an L2 metric without normalizing?

</details>

### 10. Define supervised, unsupervised, and self-supervised learning. Where does each stage of modern LLM training fit?

<details><summary><b>Answer</b></summary>

**Supervised**: learn from (input, label) pairs where labels come from outside the data - human annotation, logged outcomes. **Unsupervised**: find structure with no labels at all - clustering, density estimation, dimensionality reduction. **Self-supervised**: manufacture the labels *from the data itself* via a pretext task, then learn with standard supervised machinery - no annotation cost, effectively unlimited data.

Mapping the modern LLM pipeline is the real point of the question:

- **Pretraining** - self-supervised. Next-token prediction turns raw text into trillions of (context, next-token) pairs; the "label" is just the following token. Masked-language modeling (BERT) is the same idea with a different pretext task.
- **SFT / instruction tuning** - plain supervised learning: curated (prompt, response) pairs, cross-entropy on the response tokens.
- **Preference tuning (RLHF, or GRPO-style RL on rewards)** - reinforcement learning: the signal is a scalar reward (from a learned reward model, human preferences, or verifiable checkers for math/code), not per-token labels. DPO is the interesting edge case: it optimises a preference objective directly as a supervised-style loss on preference pairs, skipping the explicit RL loop.
- **Embedding models / CLIP** - self-supervised contrastive learning: positives are co-occurring pairs (text/image, query/passage), negatives come free from the batch.
- Genuinely **unsupervised** steps still exist around the edges: clustering user queries to discover intents, deduplicating pretraining corpora via near-duplicate detection.

The one-liner that lands well: self-supervision solved the labelling bottleneck - the reason LLMs work is that next-token prediction converts the entire internet into free supervised training data.

**Follow-ups:** Is a reward model trained supervised or by RL? Why is next-token prediction such a powerful pretext task compared to, say, autoencoding? Where does RLAIF/constitutional-style feedback fit in this taxonomy?

</details>

## Intermediate

### 11. What is data leakage? Give me three subtle examples you've seen or could imagine, and how you'd detect them.

<details><summary><b>Answer</b></summary>

Leakage is any path by which information unavailable at prediction time contaminates training or evaluation, inflating offline metrics that collapse in production. The blatant case - training on test rows - is rare; the subtle ones are what kill real systems:

1. **Preprocessing fit on the full dataset**: fitting a scaler, PCA, target encoder, or tokenizer/vocabulary on train+test before splitting. Test-set statistics bleed into the transform. Fix: fit transforms inside the training fold only (sklearn `Pipeline` inside CV exists precisely for this).
2. **Group leakage**: the same patient, user, or document contributes rows to both train and test. The model learns to recognise the entity, not the pattern. Detect with group-aware splits; symptom is a big metric drop when you switch to `GroupKFold`.
3. **Temporal leakage**: random splits on time-dependent data let the model train on the future. A churn feature like "days since last login" computed over a window that extends past the label date is a classic - the feature quietly encodes the outcome.
4. **Target leakage in features**: a column causally downstream of the label - e.g., "account_frozen" as a fraud feature, when freezing happens *because* fraud was detected.
5. **LLM-era: benchmark contamination** - eval questions present in the pretraining corpus. Detection: n-gram/substring overlap scans, canary strings, comparing performance on renamed/perturbed versions of the benchmark.

Detection heuristics: results too good to be true (near-perfect AUC on a hard problem); one feature with absurd importance; **adversarial validation** - train a classifier to distinguish train from test rows, and if it succeeds, your splits differ systematically; and large offline→online metric gaps.

**Follow-ups:** Your model gets 0.99 AUC on a fraud problem - walk me through your audit. How does k-fold CV make preprocessing leakage worse if done naively? How would you check whether an LLM has memorized your eval set?

</details>

### 12. ROC-AUC vs PR-AUC - what does each measure, and why does ROC-AUC look deceptively good on imbalanced data?

<details><summary><b>Answer</b></summary>

**ROC-AUC** plots true-positive rate (recall) against false-positive rate across all thresholds; its area equals the probability that a randomly chosen positive is scored above a randomly chosen negative - a pure *ranking* metric. Baseline is 0.5 regardless of class balance. **PR-AUC** plots precision against recall; its baseline is the positive prevalence.

The deception: FPR = FP/(FP+TN) is normalized by the *negative* count. With 1M negatives and 1k positives, a model producing 10,000 false positives has FPR = 1% - the ROC curve looks superb - but at a threshold that recovers most positives, precision might be ~9% (1k true vs 10k false alarms). ROC-AUC can read 0.98 while the precision an operator experiences is single digits. PR-AUC exposes this because precision has FP in the denominator directly, undiluted by the mass of easy negatives.

Rules of thumb:
- Balanced classes, or you genuinely care how well you rank negatives too → ROC-AUC is fine and has nicer statistical properties (prevalence-invariant, so comparable across datasets).
- Rare positive class where the product experience is "how many alerts are real" → PR-AUC, or better, **precision@k** / recall at a fixed FPR matched to the ops team's review budget.

Two caveats that signal depth: PR-AUC depends on prevalence, so you can't compare it across datasets with different base rates; and average precision (the standard PR-AUC estimator) is preferred over trapezoidal interpolation, which is biased optimistic for PR curves. Neither metric says anything about **calibration** - both are invariant to any monotonic rescaling of scores.

**Follow-ups:** Why is linear interpolation between PR points invalid? Your ROC-AUC improved but PR-AUC dropped - what happened? How do you choose the final operating threshold for production?

</details>

### 13. What does it mean for a classifier to be calibrated? How do you measure and fix miscalibration?

<details><summary><b>Answer</b></summary>

Calibrated means predicted probabilities match empirical frequencies: among all cases where the model says 0.8, ~80% should actually be positive. Discrimination (ranking, AUC) and calibration are orthogonal - you can rank perfectly while outputting probabilities that are all wrong by a squashing, and any monotone rescaling changes calibration without touching AUC.

**Measurement**: reliability diagrams (bin predictions by confidence, plot observed frequency per bin vs the diagonal); **ECE** (expected calibration error) summarises the gap as a weighted average across bins - beware its sensitivity to binning choices; **Brier score** and NLL are proper scoring rules that blend calibration and discrimination.

**Fixes** (fit on validation data, never train):
- **Temperature scaling** (Guo et al. 2017): divide logits by a single learned T > 0 before softmax. Modern nets are typically *overconfident* (T ≈ 1.5-3 fixes many vision models). One parameter, preserves ranking exactly, hard to overfit - the default choice.
- **Platt scaling** (logistic fit on scores) and **isotonic regression** (nonparametric, monotone; needs more data, can overfit small val sets).

Why it matters: any system that thresholds on expected cost - fraud review queues, medical triage, deciding when an LLM-based classifier should abstain or escalate to a human - needs probabilities that mean something, not just correct rankings.

LLM angle worth volunteering: base models are surprisingly well calibrated on multiple-choice tasks (token-probability vs accuracy), and RLHF tends to *worsen* that calibration - the GPT-4 technical report showed the post-RLHF model's calibration curve visibly degraded versus the pretrained model. Verbalised confidence ("I'm 90% sure") is a separate, generally worse-calibrated channel than token logprobs.

**Follow-ups:** Why does temperature scaling leave accuracy and AUC unchanged? How does class imbalance interact with calibration under resampling? How would you calibrate an LLM judge that outputs a 1-10 score?

</details>

### 14. Your fraud dataset is 0.5% positive. Walk me through your strategy for handling the imbalance.

<details><summary><b>Answer</b></summary>

First, fix the *measurement*, then the *training*, and keep the two concerns separate.

**Measurement**: accuracy and ROC-AUC will both flatter you (see the FPR dilution problem). Use PR-AUC, precision@k sized to the review team's capacity, or recall at a fixed FPR. Establish the cost matrix - a missed fraud might cost 100× a false alarm - because that determines the operating threshold later.

**Training-side options**:
- **Class weights / weighted loss** - upweight positives in cross-entropy. Simple, no data distortion, the usual first move.
- **Resampling** - undersample negatives (cheap, works when negatives are redundant; can discard signal) or oversample positives. **SMOTE** interpolates synthetic positives in feature space - sensible for low-dimensional tabular data, mostly pointless or harmful for high-dimensional learned representations, and never apply it before splitting or you leak synthetic copies into validation.
- **Focal loss** (from RetinaNet) - down-weights easy examples by (1−p)^γ so training focuses on hard ones; designed for extreme imbalance in detection.
- **Threshold moving** - often the most underrated tool: train normally, get calibrated probabilities, then pick the threshold that optimises expected cost. Imbalance doesn't prevent learning a good *ranker*; it breaks the default 0.5 threshold.
- **Reframing** - at extreme rarity or with novel attack patterns, anomaly-detection or one-class formulations may beat classification.

Critical subtleties: evaluate on the *natural* distribution, never a rebalanced one; if you resample or reweight, your output probabilities are biased and must be **recalibrated** before thresholding; and validate temporally, because fraud patterns drift and adversaries adapt.

**Follow-ups:** You oversampled and now predicted probabilities are inflated - why, and how do you correct them? When is undersampling actually preferable? How do delayed fraud labels (chargebacks arriving 60 days later) change your evaluation?

</details>

### 15. Explain momentum and Adam. What problem does each solve over vanilla SGD?

<details><summary><b>Answer</b></summary>

**Momentum** maintains an exponential moving average of gradients and steps along that average: `v ← βv + g; w ← w − lr·v` (β typically 0.9). In loss landscapes shaped like ravines - steep in some directions, shallow in others - vanilla SGD oscillates across the steep walls while crawling along the valley floor. Momentum cancels the oscillating components (they alternate sign and average out) and accumulates the consistent ones, giving up to a 1/(1−β) effective amplification along stable directions. It also smooths mini-batch noise.

**Adam** adds a second idea: **per-parameter adaptive step sizes**. It tracks both the first moment m (like momentum, β₁=0.9) and second moment v - an EMA of squared gradients (β₂=0.999 classically, ~0.95 in LLM practice) - and updates with `w ← w − lr · m̂ / (√v̂ + ε)`. Dividing by √v̂ normalizes each parameter's step by its typical gradient magnitude: parameters with rare/small gradients (embedding rows for rare tokens) get relatively larger steps; parameters with large, noisy gradients get damped. The hats are **bias correction** - both EMAs are initialized at zero and severely underestimate their targets early in training; without correction, early steps would be badly mis-scaled.

Why this matters for transformers: gradient scale varies enormously across a deep transformer (embeddings vs LayerNorm gains vs attention projections), and a single global LR can't serve them all - SGD is notoriously hard to make work on transformers, while Adam-family optimizers are robust. The flip side: Adam keeps two extra fp32 states per parameter (~8 bytes/param), a major memory cost that motivates 8-bit optimizers and ZeRO-style sharding.

**Follow-ups:** Why does Adam need bias correction - what happens without it? Why does SGD+momentum still often beat Adam on convnets? What's the memory footprint of Adam for a 7B model and how do you reduce it?

</details>

### 16. Adam vs AdamW - what exactly is "decoupled weight decay," and why did AdamW become the transformer default?

<details><summary><b>Answer</b></summary>

The difference is *where* the weight-decay term enters the update. In "Adam + L2," you add λw to the gradient, so the penalty flows through Adam's machinery - including division by √v̂. In **AdamW** (Loshchilov & Hutter, "Decoupled Weight Decay Regularization"), decay is applied directly to the weights, outside the adaptive update:

```python
# Adam + L2: penalty is rescaled by the adaptive term
g = grad + lam * w
w -= lr * m_hat / (v_hat.sqrt() + eps)   # decay diluted where v_hat is large

# AdamW: decay decoupled from gradient adaptation
w -= lr * m_hat / (v_hat.sqrt() + eps)
w -= lr * lam * w                         # uniform multiplicative shrinkage
```

Why the coupled version is broken: parameters with large gradient history (large v̂) have the L2 term divided down - precisely the weights moving the most get *the least* regularization, and the effective decay strength becomes an uncontrolled function of gradient statistics. It also entangles λ with the learning rate schedule in messy ways, making hyperparameters non-transferable across runs. With plain SGD, L2 and weight decay coincide - the distinction only exists for adaptive optimizers, which is exactly the trap the question tests.

AdamW restores a clean interpretation - every weight shrinks by the same fraction lr·λ per step - decouples the λ/lr search dimensions, and empirically generalizes better. It's the default in essentially every modern transformer recipe (GPT-series, Llama, etc.), with typical settings λ ≈ 0.1, β₂ ≈ 0.95, and decay disabled for biases, LayerNorm/RMSNorm parameters, and often embeddings.

**Follow-ups:** Why is weight decay ≡ L2 under SGD but not under Adam? Why exclude norm parameters from decay? What happens to effective weight decay as the LR is cosine-annealed to near zero?

</details>

### 17. Why do transformer training recipes use learning-rate warmup, and what does the rest of the schedule look like?

<details><summary><b>Answer</b></summary>

**Warmup** ramps the LR linearly from ~0 to peak over the first few hundred to few thousand steps. Three reinforcing reasons transformers need it:

1. **Adam's second-moment estimate is unreliable early.** v̂ is an EMA over a handful of noisy gradients, so the adaptive step m̂/√v̂ can be wildly mis-scaled; a full-size LR on top of that causes destructive early updates. (RAdam formalised this variance problem; warmup is the practical fix.)
2. **Early transformer training is fragile.** At init, attention distributions and the loss landscape are ill-conditioned; large steps can push the model into a state with exploding gradient norms or a loss divergence it never recovers from. Original post-LN transformers were *unusable* without warmup; pre-LN reduced but didn't eliminate the need.
3. **Large batches.** The linear-scaling regime (big batch → big LR) makes the first steps even more dangerous; Goyal et al. introduced warmup for exactly this in the ImageNet-in-1-hour work.

After warmup, the standard is **cosine decay** from peak LR down to ~10% of peak over the full token budget (the Chinchilla/Llama-style recipe). Decaying matters: high LR late in training keeps the model bouncing around the minimum; annealing lets it settle, and the final low-LR phase disproportionately improves the model.

A modern alternative worth naming: **WSD (warmup - stable - decay)** - hold LR constant after warmup, then decay sharply only in the last ~10-20% of training. The benefit is operational: you can branch a decayed "finished" checkpoint off a still-running stable-phase run at any time, which suits continued pretraining and data-mixture experiments (used by MiniCPM and DeepSeek-era recipes).

**Follow-ups:** What actually goes wrong if you skip warmup - describe the failure signature in the loss/grad-norm curves. Why does cosine-to-zero interact badly with wanting to resume training? How would you set peak LR for a model 10× bigger?

</details>

### 18. Explain backpropagation to me like I'm a strong software engineer who's never done ML. Why is it efficient?

<details><summary><b>Answer</b></summary>

A neural net is a composite function: `loss = f_L(...f_2(f_1(x, w_1), w_2)..., w_L)`. Training needs ∂loss/∂w for every weight. Backprop is just the **chain rule organised as dynamic programming**: compute the loss forward while caching each layer's activations, then sweep backward, multiplying by one local Jacobian at a time and reusing the running product - the "gradient signal" - at every layer.

The efficiency argument is the heart of a good answer. Naively, you could compute each weight's gradient independently (finite differences: perturb one weight, rerun the network) - that's O(#params) forward passes, hopeless for billions of parameters. Backprop computes *all* gradients in one backward sweep costing roughly **2× the forward pass**, because the backward pass reuses shared intermediate results exactly like memoization collapses an exponential recursion. Key implementation detail: you never materialise full Jacobian matrices - reverse-mode autodiff propagates **vector-Jacobian products**, which for a matmul layer are just two more matmuls (grads w.r.t. input and w.r.t. weights).

Reverse mode is the right direction because the loss is scalar: one output, many inputs → one backward sweep gets every derivative. (Forward-mode is efficient in the opposite regime, few inputs/many outputs.)

Engineering consequences worth stating: total training compute is ~3× forward (hence the ≈6·N·D FLOPs rule of thumb for transformers with N params and D tokens); the cached activations dominate training memory, which is why **activation checkpointing** trades recompute for memory; and frameworks implement this as autograd over a recorded computation graph - every op registers its VJP.

**Follow-ups:** Why is training memory so much larger than inference memory? What is activation checkpointing and what's its compute overhead? Where does the 6ND estimate come from?

</details>

### 19. What are vanishing and exploding gradients? What causes them, and what does modern architecture design do about them?

<details><summary><b>Answer</b></summary>

Backprop multiplies a chain of layer Jacobians. If those factors are typically <1 in magnitude, the product shrinks geometrically with depth - early layers get essentially zero gradient and stop learning (**vanishing**). If factors are >1, the product blows up - loss spikes, NaNs (**exploding**). Same mechanism, opposite sign of log-magnitude.

Classical causes: saturating activations (sigmoid's max derivative is 0.25; tanh saturates at extremes), poorly scaled initialization, and depth or recurrence (RNNs multiply by the same recurrent Jacobian per timestep, making them the pathological case - historically fixed by LSTM/GRU gating).

Modern fixes, each attacking a different link in the chain:
- **Residual connections**: `y = x + f(x)` gives Jacobian `I + ∂f/∂x` - the identity term provides a gradient highway that never vanishes, letting 100+-layer networks train. This is the single most important trick, and transformers are residual networks through and through.
- **Normalization** (LayerNorm/RMSNorm): keeps activation scales controlled so Jacobians stay well-conditioned; **pre-norm** placement (norm before each sublayer) keeps the residual path clean and is why GPT-2-onward models train stably at depth.
- **ReLU/GELU** activations: derivative ~1 on the active region, no two-sided saturation.
- **Variance-preserving init** (Xavier/He): start with Jacobian factors near unit scale.
- **Gradient clipping** (global norm, typically 1.0): a backstop against explosion - it rescales pathological updates rather than preventing the cause.

Diagnosis in practice: log per-layer gradient norms. A geometric decay across depth = vanishing; sudden grad-norm spikes preceding loss spikes = exploding, common in LLM pretraining and handled with clipping, LR reduction, or skipping the offending batch.

**Follow-ups:** Why exactly does `I + ∂f/∂x` fix gradient flow? Why do pre-norm transformers tolerate less warmup than post-norm? Your 30B pretraining run shows recurring loss spikes - what's your playbook?

</details>

### 20. Why can't you initialize all weights to zero? What do Xavier and He initialization actually do?

<details><summary><b>Answer</b></summary>

Zero (or any constant) init fails from **symmetry**: every neuron in a layer computes the identical function, receives the identical gradient, and takes the identical update - they never differentiate, so your wide layer is effectively one neuron. Randomness breaks the symmetry. (Biases *can* start at zero; the weights' randomness breaks symmetry for them.)

But random isn't enough - the **scale** must be right, or activations and gradients shrink/blow up geometrically with depth (the vanishing/exploding problem, baked in at step 0). The principled goal: preserve variance layer to layer.

- **Xavier/Glorot init**: variance 2/(fan_in + fan_out) - derived for symmetric activations like tanh, balancing forward activation variance and backward gradient variance.
- **He/Kaiming init**: variance 2/fan_in - accounts for ReLU zeroing half its inputs (halving variance), so it doubles the scale. Standard for ReLU-family networks.

Transformer practice goes further: GPT-2-style recipes use small normal init (std ≈ 0.02) and additionally **scale down the residual-branch output projections by 1/√(2·n_layers)** - because N residual branches add their variance into the stream, and without this the residual-stream magnitude grows with depth. Embeddings are often tied with the output head, which constrains their scale too. The research-flavoured extension is **μP (μTransfer)**: parameterize init and per-layer LRs so optimal hyperparameters transfer from small to large models - tune on a 40M model, train the 10B with the same settings.

Good candidates connect init to everything else: init, normalization, residuals, and warmup are four coordinated solutions to the same problem - keeping signal propagation well-conditioned in deep networks.

**Follow-ups:** Derive why fan_in appears in the variance formula for a linear layer. Why do residual networks need the extra 1/√N scaling? What breaks if you init a transformer with std 0.2 instead of 0.02?

</details>

### 21. Batch norm vs layer norm: how does each work, and why do transformers use layer norm?

<details><summary><b>Answer</b></summary>

Both normalize activations to zero mean and unit variance, then apply a learned scale γ and shift β. The difference is the axis. **BatchNorm** normalizes each feature/channel *across the batch* - statistics are computed over the N examples in the mini-batch. **LayerNorm** normalizes *across the feature dimension within a single example* (per token, in a transformer) - no dependence on other examples at all.

Why BN is wrong for transformers/LLMs:
- **Variable-length sequences and padding** make per-position batch statistics ill-defined and noisy.
- **Batch dependence**: BN's quality degrades at small batch sizes, and in distributed training the per-device batch may be tiny (SyncBatchNorm exists but adds communication).
- **Train/inference mismatch**: BN needs running statistics for inference - a persistent source of train/eval bugs - and is awkward for autoregressive decoding, where you generate one token at a time with effective batch size 1 per position.
- LayerNorm has none of these issues: each token normalizes itself, identical math at train and inference, any batch size.

Modern refinements worth knowing: **RMSNorm** (Llama, Mistral, most current LLMs) drops mean-centring and just divides by the root-mean-square, with a learned gain - cheaper, empirically as good. **Placement matters more than flavour**: the original transformer used **post-norm** (normalize after the residual add), which is unstable at depth and demands careful warmup; **pre-norm** (normalize inside the branch, before attention/MLP) keeps an unimpeded identity path through the residual stream and trains stably - universal since GPT-2. Some recent models add extra norms (e.g., QK-norm on attention queries/keys) specifically to prevent attention-logit blowups at scale.

**Follow-ups:** Why does BN generally underperform even in encoder-only transformers where decoding isn't an issue? What does RMSNorm remove and why is that OK? Explain mechanically why post-norm at depth is unstable.

</details>

### 22. Derive cross-entropy loss from first principles. Why is it "the right" loss for classification and language modeling?

<details><summary><b>Answer</b></summary>

Start from **maximum likelihood**. A classifier (or LM) defines a conditional distribution p_θ(y|x). Given i.i.d. data, MLE maximises Π p_θ(yᵢ|xᵢ); taking logs (monotone, turns products into sums, numerically necessary) and negating gives the training objective: minimise **negative log-likelihood** = −Σ log p_θ(yᵢ|xᵢ). For a categorical output with one-hot targets, that is exactly cross-entropy: H(y, p) = −Σ_c y_c log p_c = −log p(correct class). Language modeling is this applied per token: next-token cross-entropy is MLE of the text distribution, and **perplexity = exp(mean CE)** - "how many equally likely tokens is the model choosing among."

The information-theoretic view: minimising CE against the empirical data distribution is equivalent to minimising **KL(data ‖ model)** - you're matching the model distribution to the data distribution, and the gap above the data's own entropy is exactly the KL term.

Why it's *right* mechanically, not just philosophically:

1. **Gradient quality.** With softmax outputs, ∂CE/∂logits = **p − y**. Confidently wrong (p≈0 on the true class) → gradient near maximal; correct and confident → gradient near zero. No saturation on mistakes.
2. **Proper scoring rule**: expected CE is minimised only by predicting the true conditional probabilities, so it incentivises honest uncertainty - the basis for LM calibration.
3. It punishes confident errors unboundedly (−log p → ∞ as p→0), which is what you want when downstream decisions consume the probabilities.

The framing that lands in interviews: cross-entropy isn't one loss among many - it's what "do MLE on a categorical distribution" *compiles to*. MSE is the same statement for Gaussian noise; every standard loss is a likelihood in disguise.

**Follow-ups:** Show that softmax+CE gives gradient p − y. What does label smoothing change in this picture? Why is perplexity exp of CE, and what does perplexity 8 mean concretely?

</details>

### 23. Explain softmax and the temperature parameter. How do you compute softmax stably, and where does temperature show up across ML?

<details><summary><b>Answer</b></summary>

Softmax maps logits to a probability distribution: `p_i = exp(z_i/T) / Σ_j exp(z_j/T)`. With temperature T=1 it's the standard form. As **T→0** it approaches argmax (all mass on the top logit); as **T→∞** it flattens toward uniform. Dividing by T rescales logit *differences*, which is what controls sharpness. Softmax is invariant to adding a constant to all logits - only differences matter - which enables the stability trick.

**Numerical stability**: exp overflows fast (exp(89) overflows fp32). Subtract the max logit first - mathematically a no-op, numerically essential:

```python
def softmax(z, T=1.0):
    z = z / T
    z = z - z.max(axis=-1, keepdims=True)   # log-sum-exp trick
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)
```

In practice you compute `log_softmax` directly and use it with NLL for a fused, stable cross-entropy - never `log(softmax(z))` in two steps (catastrophic when a probability underflows to 0).

Temperature appears all over the stack, and connecting the dots is what makes this answer senior:
- **LLM sampling**: T scales next-token logits before sampling. Low T → deterministic, repetitive; high T → diverse, error-prone. T=0 conventionally means greedy decoding. Works alongside top-p/top-k truncation.
- **Knowledge distillation** (Hinton et al.): soften the teacher's distribution with T>1 so "dark knowledge" in the non-argmax classes carries gradient signal to the student.
- **Contrastive losses** (InfoNCE/CLIP/SimCLR): similarity scores divided by τ (~0.05-0.1) before the softmax; τ controls how hard the loss focuses on the most confusable negatives. CLIP famously *learns* its temperature.
- **Calibration**: temperature scaling fits a single T on validation logits to fix overconfidence - same knob, different objective.
- **Attention**: the 1/√d_k factor in scaled dot-product attention is exactly a fixed temperature keeping logit variance ~1 so the softmax doesn't saturate at init.

**Follow-ups:** Why does attention divide by √d_k - what happens without it? Why is low temperature *not* the same as top-k truncation? What breaks numerically if you compute log(softmax(z)) naively?

</details>

## Advanced

### 24. Why is MSE a bad loss for classification, even though it "works"? Connect it to the probabilistic view of loss functions.

<details><summary><b>Answer</b></summary>

Two independent arguments - mechanical and probabilistic - and a strong answer gives both.

**Mechanical: gradient starvation on confident mistakes.** For a sigmoid output p = σ(z) with MSE loss (p − y)², the gradient w.r.t. the logit is `2(p − y)·σ'(z)`, and σ'(z) = p(1−p) → 0 whenever the output saturates. So an example the model gets *confidently wrong* (p≈0, y=1) produces almost **no gradient** - precisely the examples that most need correction learn slowest. Cross-entropy's sigmoid/softmax gradient is `p − y` with no σ' factor: the derivative of the log exactly cancels the sigmoid's saturation, so confident errors get the largest updates. This also makes MSE-on-sigmoid non-convex in z per example with bad plateaus, whereas CE is convex in the logits.

**Probabilistic: wrong noise model.** Every loss is a negative log-likelihood under some noise assumption. MSE ⇔ Gaussian noise with fixed variance - a model for continuous targets that can be "off by 0.3." Class labels are categorical events; the correct likelihood is Bernoulli/categorical, whose NLL *is* cross-entropy. Using MSE asserts that predicting 0.7 for a true label 1 incurs the same kind of penalty as a regression miss, and it bounds the maximum penalty for total confidence in the wrong class at 1.0, where CE assigns unbounded penalty (−log p → ∞). CE is the negative log-likelihood of the categorical model, so training with it *is* MLE - which is why probabilities trained under CE are the ones with a clean probabilistic interpretation.

Nuance to volunteer: Brier score (MSE on probabilities) *is* a proper scoring rule and is used for evaluating calibration - the objection is about optimization dynamics and likelihood correctness for training, not that MSE on probabilities is meaningless. And regression flips everything: CE doesn't apply directly, MSE is exactly right under Gaussian assumptions, L1/Huber when you want robustness to outliers.

**Follow-ups:** Derive the p − y gradient and show where the cancellation happens. When would you use Brier score deliberately? What loss corresponds to Laplace noise, and when would you prefer it?

</details>

### 25. Explain contrastive learning and the InfoNCE loss. How are modern embedding models (CLIP, text retrievers) actually trained?

<details><summary><b>Answer</b></summary>

Contrastive learning trains an encoder so that "matching" pairs score high similarity and non-matching pairs score low - without per-example labels. **InfoNCE** operationalises it as cross-entropy over similarities: for query q with positive k⁺ among a set of negatives {kᵢ},

L = −log [ exp(sim(q,k⁺)/τ) / Σᵢ exp(sim(q,kᵢ)/τ) ]

i.e., an N-way classification where the "correct class" is the true partner. sim is usually cosine; **τ** (~0.05-0.1 typically; CLIP learns it, initialized to 0.07) sharpens the softmax so the loss concentrates on the hardest, most confusable negatives. Theoretically it's a lower bound on mutual information between the paired views (from the Contrastive Predictive Coding paper), though in practice people treat it as "softmax retrieval loss."

Where positives/negatives come from is the whole game:
- **CLIP**: positives are (image, caption) pairs from web data; negatives are all other pairs in the batch (**in-batch negatives**) - an N×N similarity matrix with a symmetric loss in both directions. Batch size is critical because it sets the number/difficulty of negatives; CLIP used ~32k.
- **Text embedding/retrieval models** (E5/GTE/BGE-style, DPR lineage): positives are (query, relevant passage); in-batch negatives are augmented with **hard negatives** mined by BM25 or a prior model - passages that are topically close but wrong, which teach fine-grained discrimination. Common recipe: large-scale weakly supervised contrastive pretraining on mined pairs, then fine-tuning on curated data with hard negatives, sometimes distilling from a cross-encoder reranker.
- **SimCLR-style self-supervised vision**: positives are two augmentations of the same image.

Failure modes worth naming: **false negatives** (in-batch "negatives" that are actually relevant) cap achievable quality on noisy data; small batches → easy negatives → mushy embeddings (memory banks/MoCo-style queues were built to fake bigger negative pools); and if you train with cosine+τ, you must serve with cosine (normalize before indexing).

**Follow-ups:** Why do larger batches help contrastive training but matter less for standard supervised training? How do hard negatives change what the embedding space learns? How would you build the training set for a code-search embedder?

</details>

### 26. Beyond L1/L2: explain early stopping, data augmentation, and label smoothing as regularizers. What is regularization, really?

<details><summary><b>Answer</b></summary>

The unifying definition: regularization is any technique that reduces generalization error without (primarily) reducing training error - equivalently, anything that injects a **prior** or constrains effective capacity so the model prefers solutions likely to generalize.

**Early stopping** halts training when validation loss stops improving (with a patience window) and restores the best checkpoint. It restricts how far the weights travel from initialization - for quadratic losses it's formally equivalent to L2 regularization with strength inversely related to training time. It's free (you monitor val loss anyway) and is the de facto standard in fine-tuning. Caveat: it spends the validation set; the checkpoint you pick is tuned to it. LLM-era note: single-epoch pretraining rarely "overfits" classically, but SFT on 10k examples absolutely does - 1-3 epochs with checkpoint selection on held-out evals is the norm.

**Data augmentation** encodes invariances as synthetic data: crops/flips/colour jitter in vision (label shouldn't change under them), paraphrase/back-translation in classic NLP, SpecAugment in speech. It's a prior expressed through data rather than through the loss - often the strongest regularizer available because it directly attacks variance with (pseudo-)new samples. The LLM analogue is less "augmentation" and more synthetic data generation and prompt-format diversification during SFT, guarding against format overfitting.

**Label smoothing** replaces the one-hot target with (1−ε) on the true class and ε/(K−1) elsewhere (ε≈0.1). It stops the model from chasing infinite logit gaps, improves calibration in supervised classification, and was standard in Inception-era vision and machine translation. Caveats: it distorts the probability semantics slightly, and it's known to hurt distillation (teacher's non-target information gets flattened). It's generally *not* used for LLM pretraining, where matching the data distribution - including its genuine uncertainty - is the objective.

Also in the family: dropout, weight decay, small-batch gradient noise, and - the most underrated one - **more data**, which is why "collect/clean data" beats clever regularizers in most production settings.

**Follow-ups:** Why is early stopping ≈ L2 for quadratic losses - give the intuition. When does augmentation *hurt*? Why does label smoothing conflict with knowledge distillation?

</details>

### 27. What kinds of distribution shift exist, and how would you monitor a deployed model - classical or LLM-based - for them?

<details><summary><b>Answer</b></summary>

Three canonical types, distinguished by *what* changes between training and serving:

- **Covariate shift**: P(x) changes, P(y|x) stable - new user demographics, new device types, traffic mix changes. The model sees inputs unlike its training data.
- **Label/prior shift**: P(y) changes - fraud rate doubles during holidays; class frequencies move while the class-conditional behaviour holds.
- **Concept drift**: P(y|x) itself changes - the same input now means something else. Adversarial domains (fraud, spam, abuse) drift *because* your model exists; attackers adapt to it.

Monitoring stack, ordered by signal latency:
1. **Input drift** (immediate): compare live feature distributions to a training/reference window - PSI, KL divergence, Kolmogorov - Smirnov tests per feature; for unstructured inputs, monitor drift in **embedding space** (distance between live and reference embedding distributions).
2. **Prediction drift** (immediate): shifts in the output score distribution or predicted-class mix often flag trouble before labels arrive.
3. **Proxy/behavioural metrics** (fast): CTR, user corrections, thumbs-down rates, escalation-to-human rates, retry rates.
4. **Ground-truth metrics** (delayed): true accuracy/PR once labels land - chargebacks at 60 days, churn at 90. The delay is why layers 1-3 exist.
5. **Golden/canary sets**: fixed eval suites replayed on a schedule - regression detection independent of traffic.

For LLM systems specifically: the *query* distribution drifts (new topics, new jailbreak patterns), and - uniquely - the **model itself shifts under you** when a provider updates a hosted model or you change a prompt. Treat prompts+model versions like code: pin versions, run eval suites (LLM-judge with periodic human audit) on every change, log samples for offline re-scoring, and monitor output properties (length, refusal rate, tool-call rate, judge scores) as prediction-drift signals.

Responses: retrain/fine-tune on recent data, recalibrate thresholds (cheap, often sufficient for prior shift), or fix upstream data pipelines - a surprising fraction of "drift" alerts are broken feature pipelines, not the world changing.

**Follow-ups:** How do you distinguish concept drift from a data-pipeline bug? Prior shift only - can you fix it without retraining? Design the drift monitoring for a RAG-based support bot.

</details>

### 28. When does cosine similarity mislead you? Discuss embedding-space pathologies relevant to retrieval systems.

<details><summary><b>Answer</b></summary>

Cosine similarity is only as meaningful as the geometry of the space it's computed in, and several pathologies corrupt that geometry:

**Anisotropy.** Raw hidden states from language models occupy a narrow cone rather than spreading over the hypersphere - average pairwise cosine between *random* sentences can be very high (this is why early "BERT embeddings via mean pooling" underperformed word-frequency baselines on similarity tasks). Consequence: absolute cosine values are uninterpretable; a 0.8 might be noise floor. Contrastive fine-tuning (the SimCSE lineage, and all modern embedders) explicitly spreads the space - the InfoNCE loss has a **uniformity** term pushing points apart and an **alignment** term pulling positives together. Practical rule: never ship nearest-neighbour search on base-LLM activations; use a contrastively trained embedder.

**Hubness.** In high dimensions, some points become "hubs" that appear in the k-NN lists of a disproportionate share of queries - an artefact of concentration of distances. Symptom: the same handful of chunks retrieved for everything. Mitigations: better embedders, score normalization per candidate, reranking with a cross-encoder.

**Training/serving metric mismatch.** A model trained with cosine (normalized) but indexed with raw inner product lets vector *norms* - which the training objective never disciplined - dominate rankings. Normalize at index time and query time, and configure the ANN index metric (IP vs L2 vs cosine) to match.

**Isotropic-but-meaningless directions.** Cosine weights all dimensions equally; if a few dimensions carry high-variance nuisance information (length, language, formatting), similarity reflects those. Matryoshka-style training and whitening transforms partially address this.

**Task mismatch** - the subtlest one for RAG: "similar" is task-relative. Question-to-answer relevance is asymmetric; a question is often most cosine-similar to *other questions*, not to passages answering it. Hence instruction-prefixed asymmetric embedders (separate query/passage prompts, E5/BGE-style) and cross-encoder rerankers on the top-k.

**Follow-ups:** How would you detect hubness in a production RAG system? Why does a cross-encoder beat bi-encoder cosine, and why not use it for first-stage retrieval? What do alignment and uniformity mean in the Wang & Isola framing of contrastive learning?

</details>

### 29. What is maximum likelihood estimation? Show how it generates the standard loss functions, and where the Bayesian view (MAP) connects to regularization.

<details><summary><b>Answer</b></summary>

MLE picks parameters that make the observed data most probable under the model: θ* = argmax_θ Π p_θ(dataᵢ). You maximise the **log**-likelihood in practice - monotone (same argmax), turns the product into a sum (i.i.d. data → per-example losses that mini-batch cleanly), and avoids floating-point underflow from multiplying thousands of probabilities. A likelihood is *not* a probability distribution over θ - it's the data's probability viewed as a function of parameters; it needn't integrate to 1 over θ.

The generative move interviewers want: **choose a noise model, get a loss for free.**
- Categorical likelihood over classes/tokens → NLL = **cross-entropy**. LLM pretraining is MLE of the text distribution, token by token.
- Gaussian likelihood with fixed variance around a predicted mean → NLL = **MSE** (up to constants).
- Laplace noise → **L1/MAE** (hence its robustness to outliers - heavy tails expect occasional large errors).
- Bernoulli → binary cross-entropy; Poisson → Poisson regression loss.

So "which loss?" is really "which conditional distribution do I believe generated the targets?"

**MAP** (maximum a posteriori) adds a prior: maximise log p(data|θ) + log p(θ). A zero-mean Gaussian prior on weights adds −λ‖θ‖², i.e., **L2/weight decay**; a Laplace prior adds −λ‖θ‖₁, i.e., **L1**. Regularization is literally a prior belief that weights should be small - the Bayesian and the penalised-optimization views are the same math.

Properties worth citing: MLE is consistent and asymptotically efficient under regularity conditions, but with finite data it overfits - it happily assigns probability 1 to events seen once (the smoothing problem in classical n-gram LMs). Priors/regularization are the finite-data correction. One modern wrinkle: RLHF-style objectives leave the MLE framework - they optimise expected reward with a KL leash back to the MLE-trained reference model, which is why the KL term is there: it anchors the policy to the distribution MLE learned.

**Follow-ups:** Derive MSE from the Gaussian likelihood explicitly. Why does MLE + one observation of a rare event give pathological probabilities, and what's the fix? What role does the KL penalty play in RLHF from this viewpoint?

</details>

### 30. What is double descent, and how does it change the classical story about model size and overfitting?

<details><summary><b>Answer</b></summary>

Classical statistical learning predicts a U-shaped test-error curve in model capacity: underfit → sweet spot → overfit, with the worst behaviour when the model can exactly memorize the data. **Double descent** (Belkin et al. 2019; scaled up empirically in Nakkiran et al., "Deep Double Descent") shows what actually happens with modern networks: test error rises as you approach the **interpolation threshold** (capacity ≈ just enough to fit the training set, including its noise), *peaks there*, and then **falls again** as you keep growing the model far past it. The classical U is the left half of a larger curve.

Intuition for the second descent: at the interpolation threshold there's essentially one way to fit the data, and it's contorted - forced to thread through noisy labels with a strained function. With massive overparameterization, *many* interpolating solutions exist, and the optimizer's implicit bias (SGD-family methods preferring low-norm/"smooth" solutions) selects well-generalizing ones from that set. Memorizing the noise no longer forces global weirdness.

Nakkiran et al. showed the phenomenon along three axes: **model-wise** (bigger nets), **epoch-wise** (train longer through a mid-training test-error bump), and **data-wise** - the genuinely counterintuitive one, where *more data can transiently hurt* a fixed-size model by moving the interpolation threshold onto it. Label noise amplifies the peak; regularization and early stopping can smooth it away, which is why practitioners rarely see a clean double-descent curve in the wild.

Why it matters for the LLM era: it dissolves the "your model is too big, it will overfit" instinct and is consistent with scaling practice - larger transformers generalize better, and capacity is budgeted against compute and data (Chinchilla-style scaling laws), not against classical overfitting fears. Caveat a strong candidate adds: one-epoch pretraining on trillions of tokens sits far from the interpolation regime anyway - memorization concerns there are about privacy/contamination, not test loss.

**Follow-ups:** Where does the implicit bias of SGD enter this story? How can adding training data hurt - walk through the mechanism. Does double descent contradict the bias-variance decomposition or just the classical capacity narrative?

</details>

### 31. Your LLM pretraining loss just spiked. Talk me through training stability: gradient clipping, mixed precision, and your debugging playbook.

<details><summary><b>Answer</b></summary>

Loss spikes are endemic to large-scale transformer training - occasional bad batches, attention-logit blowups, or optimizer state getting mis-scaled produce a huge gradient, a destructive update, and a loss that jumps and either recovers slowly, plateaus higher, or diverges.

**Standing defences** in every serious recipe:
- **Gradient clipping by global norm** (typically 1.0): compute the norm over all parameters; if it exceeds the threshold, rescale the whole gradient vector. Preserves direction, caps magnitude. Clipping *frequency* is itself a health metric - clipping every step means your LR is too high.
- **Mixed precision done right.** fp16 has a tiny dynamic range (max ~65k, and underflow is the bigger killer) and requires **loss scaling** - multiply the loss by a factor so small gradients survive fp16, unscale before the optimizer step, and skip steps whose gradients contain inf/NaN (dynamic loss scaling automates this). **bf16** keeps fp32's 8 exponent bits at lower mantissa precision, eliminating loss scaling - the modern default on A100/H100/TPU. Either way, keep **fp32 master weights and optimizer states**; accumulate large reductions in fp32.
- **Architectural/objective stabilisers**: pre-norm placement, QK-norm to stop attention-logit growth, and an auxiliary **z-loss** (used in PaLM, ~1e-4 · log²Z) keeping the softmax normalizer from drifting.
- Warmup + sane peak LR, β₂ ≈ 0.95 (shorter second-moment memory reacts faster to gradient-scale changes than 0.999).

**The playbook when a spike hits**: check grad-norm and per-layer norm logs - a grad-norm spike *preceding* the loss spike implicates optimization; no grad spike suggests data. Inspect the offending batch (corrupt documents, pathological repetition - data issues are the most common culprit). Standard remediations, escalating: rely on clipping and let it recover; **rewind to the last good checkpoint and skip the offending data shard** (used in OPT and BLOOM-era runs, documented candidly in OPT's logbook); lower peak LR; add stabilisers (QK-norm, z-loss). Also rule out infrastructure: a flaky GPU producing silent NaNs looks exactly like an optimization problem - per-rank gradient-norm logging localises it.

**Follow-ups:** Why does bf16 remove the need for loss scaling - what's the actual bit-level difference? Why lower β₂ for LLMs? Clipping fires on 40% of steps - what do you change?

</details>

### 32. Design the evaluation for a fraud model at 0.1% prevalence, end to end: metrics, thresholding, validation protocol, and monitoring.

<details><summary><b>Answer</b></summary>

This is a synthesis question - the interviewer wants the imbalance, calibration, leakage, and drift threads woven into one coherent design.

**Metrics.** Rule out accuracy (99.9% baseline) and be suspicious of ROC-AUC (FPR diluted by ~999:1 negatives). Primary offline metrics: **PR-AUC** for model comparison, plus operating-point metrics tied to capacity - if the fraud-ops team reviews 500 alerts/day, report **precision@500/day** and the recall achieved there; alternatively recall at a fixed FPR. Express the final objective in money: expected cost = FN_count·(avg fraud loss) + FP_count·(review cost + customer-friction cost).

**Thresholding.** Train a scorer, then **calibrate** on held-out data (isotonic or temperature/Platt - and recalibrate *after* any class reweighting or resampling, which biases probabilities). Choose the threshold minimising expected cost on validation; consider two thresholds (auto-block above high, human review in the middle band).

**Validation protocol.** Strictly **temporal splits** - train on months 1-9, validate on 10, test on 11-12 - because fraud drifts and adversaries adapt; random splits inflate results. **Entity-level grouping** so no card/account/device spans splits (group leakage otherwise lets the model recognise entities). Handle **label latency**: chargebacks take 30-90 days to arrive, so recent data has censored labels - evaluate on a window mature enough for labels to settle, and be explicit about it. Audit features for target leakage (anything downstream of a fraud decision, like "account_frozen"). Run **adversarial validation** to confirm train/test aren't trivially distinguishable for spurious reasons.

**Monitoring.** Immediate: input-feature drift (PSI/KS vs reference), score-distribution drift, alert volume. Fast proxies: review-queue precision (human analysts label alerts daily - a live precision estimate). Delayed: recall against matured chargeback labels, reported with the built-in lag. Feedback-loop trap: you only get labels for what you *investigate*, so blocked/ignored transactions are unlabeled - mitigate with a small exploration budget (let a random ~0.1% sample through un-actioned, or use analyst deep-dives) to estimate uncensored recall. Retrain cadence triggered by drift alarms, not just calendar.

**Follow-ups:** How exactly does the selective-labels problem bias naive retraining? The ops team's capacity halves - what changes in your metric and threshold? How do you A/B test a new fraud model when the intervention itself changes the labels you observe?

</details>
