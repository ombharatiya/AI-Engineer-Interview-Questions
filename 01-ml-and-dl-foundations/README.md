# 🧠 ML & Deep Learning Foundations

Every AI Engineer loop - frontier lab, big tech, or startup - still opens with fundamentals: interviewers use them to separate people who *operate* models from people who *understand* them. Expect these questions in phone screens, as warm-ups before system design, and as depth probes when you claim LLM experience ("you fine-tuned a model - why AdamW? why warmup?"). You don't need research-level math, but you must explain these concepts crisply and connect them to modern transformer training.

## Crash course

### Generalization: bias, variance, and the modern caveat

**Bias** is error from a model too simple to capture the signal; **variance** is error from fitting noise in a particular training set. Expected test error decomposes as `bias² + variance + irreducible noise`. Diagnose with the **train/val gap**: high train error = underfitting (bias); low train error but high val error = overfitting (variance). The modern caveat: heavily overparameterized networks violate the classical U-shaped curve (**double descent**) - past the interpolation threshold, bigger models often generalize *better*, which is part of why scaling works.

**Regularization toolkit** (know what each one trades away):
- **L2 / weight decay** - shrinks weights toward zero; MAP estimation with a Gaussian prior.
- **L1** - drives weights exactly to zero (sparsity); Laplace prior.
- **Dropout** - randomly zeroes activations at train time (rescaled so inference needs no change); an implicit ensemble. Large-scale LLM pretraining often sets it to 0 because data is effectively unlimited.
- **Early stopping** - halt when val loss stops improving; cheap and surprisingly close to L2 in effect.
- **Data augmentation** - encodes invariances (crops/flips in vision, paraphrase/back-translation in NLP).

### Data hygiene: splits, cross-validation, leakage

Train fits parameters, **validation** picks hyperparameters/checkpoints, **test** is touched once. Use **k-fold CV** when data is small; use **temporal splits** for anything time-dependent. **Leakage** is the classic silent killer - the subtle forms are: fitting scalers/encoders/vocabularies on the full dataset before splitting, near-duplicates across splits, the same user/patient in train and test (group leakage), and features that encode the label's future. The LLM-era version is **benchmark contamination**: eval data present in pretraining corpora.

### Metrics: when accuracy lies

With 1% positives, predicting "negative" always gives 99% accuracy. Know the confusion-matrix vocabulary cold: **precision** = TP/(TP+FP), **recall** = TP/(TP+FN), **F1** = harmonic mean. **ROC-AUC** measures ranking quality (probability a random positive scores above a random negative) but is insensitive to class imbalance because FPR is normalized by the huge negative class; **PR-AUC** is the honest metric for rare positives (its baseline is the prevalence, not 0.5). **Calibration** - whether a predicted 0.8 means 80% - is separate from discrimination; measure with reliability diagrams/ECE, fix post-hoc with **temperature scaling**.

### Optimization: SGD → momentum → Adam → AdamW

- **SGD** follows noisy mini-batch gradients; noise doubles as regularization.
- **Momentum** keeps an EMA of gradients - damps oscillation across steep ravines, accelerates along consistent directions.
- **Adam** adds a per-parameter adaptive step size from an EMA of squared gradients (plus bias correction). Handles the wildly different gradient scales across transformer layers.
- **AdamW** decouples weight decay from the adaptive update. In plain Adam, an L2 penalty gets divided by the second-moment term, so high-gradient weights are barely regularized; AdamW applies decay directly (`w ← w − lr·λ·w`). This is *the* transformer default (typical λ ≈ 0.1, β₂ ≈ 0.95 for LLMs, no decay on biases/norm params).

**Schedules:** linear **warmup** (Adam's second-moment estimate is garbage for the first steps; deep transformers can diverge without it), then **cosine decay** to ~10% of peak - or a **warmup-stable-decay (WSD)** schedule when you want to keep training from intermediate checkpoints.

### Backprop and gradient pathologies

Backprop is the chain rule plus dynamic programming: cache activations on the forward pass, reuse them to compute vector-Jacobian products backward (~2× the forward FLOPs - hence the ~6·N·D training-FLOPs rule of thumb). Deep stacks multiply many Jacobians, so gradients **vanish** (saturating activations, small weights) or **explode**. Fixes: residual connections (gradient flows through the identity path), normalization layers, ReLU/GELU instead of sigmoid/tanh, variance-preserving init (**Xavier** for tanh, **He** = var 2/fan_in for ReLU; transformers typically use small normal init ~0.02 with scaled-down residual projections), and **gradient clipping** (global norm 1.0 is the standard).

### Batch norm vs layer norm

**BatchNorm** normalizes each feature across the batch - great for convnets, terrible for transformers: it breaks with variable-length sequences, small/streaming batches, autoregressive decoding, and needs synced statistics across devices. **LayerNorm** normalizes across features *within each token* - batch-independent, works at batch size 1. Modern LLMs mostly use **RMSNorm** (LayerNorm minus mean-centring) placed **pre-norm** (before each sublayer), which is markedly more stable to train than the original post-norm placement.

### Losses, softmax, temperature

**Cross-entropy is MLE**: maximising the likelihood of a categorical distribution = minimising negative log-likelihood = cross-entropy. Its gradient through softmax is beautifully simple - `p − y` - and never saturates on confident-wrong predictions (unlike MSE + sigmoid). **MSE** is MLE under Gaussian noise: right for regression, wrong for classification. **InfoNCE** trains embedding models (CLIP, modern sentence embedders): cross-entropy over similarity scores where the positive pair must beat in-batch negatives, sharpened by a temperature τ.

```python
import numpy as np

def softmax(logits, T=1.0):
    z = logits / T
    z = z - z.max()          # log-sum-exp trick: shift-invariant, avoids overflow
    e = np.exp(z)
    return e / e.sum()
# T < 1 sharpens (→ argmax as T→0); T > 1 flattens (→ uniform). Same knob as LLM sampling temperature.
```

### Embeddings and similarity

**Cosine** compares direction only; **dot product** also rewards magnitude; **Euclidean** on unit-normalized vectors is monotonically equivalent to cosine (`‖a−b‖² = 2 − 2·cos`). Use whatever similarity the embedding model was *trained* with (most contrastive text embedders: cosine). Your ANN index metric (inner product vs L2 vs cosine in FAISS/HNSW) must match.

### Distribution shift

**Covariate shift** (inputs change), **label/prior shift** (class frequencies change), **concept drift** (the input→label relationship itself changes). Production monitoring: input-feature stats (PSI/KL vs a reference window), embedding-drift detectors, prediction-distribution drift, and delayed-label metrics - plus fixed golden/canary eval sets for LLM apps, where an upstream model version bump is itself a distribution shift.

### How modern LLM training maps onto classic framings

Pretraining is **self-supervised** learning (next-token labels manufactured from the data itself), SFT is plain **supervised** learning, RLHF/GRPO-style preference tuning is **reinforcement learning**, and contrastive embedding training is self-supervised too. Clustering your user queries to find intents? That's the rare genuinely **unsupervised** step in a modern stack.

## Interview questions

See [questions.md](questions.md) - 32 questions with detailed answers, from basic to advanced.

## Red flags interviewers watch for

- Reciting "bias-variance tradeoff" as a definition but unable to *diagnose* which one a given train/val curve shows, or what to change next.
- Saying accuracy, or defaulting to ROC-AUC, for a 0.1%-positive problem without mentioning PR-AUC, precision/recall at a threshold, or costs.
- Claiming L2 regularization and weight decay are always identical - missing why AdamW exists.
- "Transformers use layer norm because it works better" with no mechanism (batch dependence, variable-length sequences, decode-time batch of 1).
- Explaining backprop as "the network learns from its errors" - no chain rule, no cached activations, no cost intuition.
- Not knowing that dropout is disabled (and needs no rescaling with inverted dropout) at inference, or that eval-mode vs train-mode bugs are a classic production failure.
- Never having heard of data leakage beyond "don't train on test" - can't name a subtle example like fitting preprocessing on the full dataset or group leakage.
- Treating temperature as an LLM-only sampling trick, without connecting it to softmax, distillation, and contrastive losses.

## Further reading

- [Deep Learning (Goodfellow, Bengio, Courville)](https://www.deeplearningbook.org/) - the canonical reference for everything in this page.
- [A Recipe for Training Neural Networks - Andrej Karpathy](https://karpathy.github.io/2019/04/25/recipe/) - the debugging/overfitting mindset interviewers want to hear.
- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) - Kingma & Ba.
- [Decoupled Weight Decay Regularization (AdamW)](https://arxiv.org/abs/1711.05101) - Loshchilov & Hutter; why transformers use AdamW.
- [Layer Normalization](https://arxiv.org/abs/1607.06450) - Ba, Kiros, Hinton.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) - Guo et al.; temperature scaling.
- [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748) - the InfoNCE loss.
- [Deep Double Descent](https://arxiv.org/abs/1912.02292) - Nakkiran et al.; the modern view of overfitting.
