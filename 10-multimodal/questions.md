# Multimodal Models - Interview Questions

21 questions: 6 basic, 8 intermediate, 7 advanced.

## Basic

### 1. Walk me through how a modern VLM gets an image into an LLM.

<details><summary><b>Answer</b></summary>

Three components: a **vision encoder**, a **projector**, and the **LLM**. The image is split into fixed-size patches (e.g. 14×14 or 16×16 pixels); each patch is linearly embedded and a ViT runs over the patch sequence, producing one embedding per patch - a 224×224 image with 16×16 patches yields 196 patch embeddings. A small **projector** (an MLP in LLaVA-style models) maps those from the vision encoder's space into the LLM's token-embedding space. The projected vectors are then spliced into the input sequence alongside real text-token embeddings, and the LLM attends over everything uniformly - from the transformer's perspective, image patches are just tokens it never saw in its text vocabulary.

Two details interviewers listen for. First, the vision encoder is almost never trained from scratch: it's a CLIP- or SigLIP-pretrained ViT, so its features are already language-aligned, which is why a tiny projector is enough to bridge the two models. Second, training is staged: stage 1 freezes both towers and trains only the projector on image-caption pairs (cheap alignment), stage 2 unfreezes the LLM for visual instruction tuning on image-question-answer data, and later stages add high-resolution handling and preference tuning.

Design variations worth naming: **resampler/Q-Former** projectors (Flamingo, BLIP-2) compress hundreds of patch embeddings into a fixed set of ~32-64 learned query tokens to save context; Flamingo instead injects vision via gated cross-attention layers rather than inline tokens; Fuyu drops the vision encoder entirely and linearly projects raw patches straight into the decoder. Modern open models (LLaVA-NeXT, Qwen-VL, InternVL) mostly converge on MLP projector + image tiling for high resolution.

**Follow-ups:** Why can you get away with training only the projector in stage 1? What breaks if you use a randomly initialized vision encoder instead of CLIP? How does the model handle an image whose aspect ratio doesn't match the encoder's training resolution?

</details>

### 2. What is CLIP, how is it trained, and why did it become the foundation for so much multimodal work?

<details><summary><b>Answer</b></summary>

CLIP trains an image encoder and a text encoder jointly so that matching images and captions land close together in a shared embedding space. Training is **contrastive**: take a batch of N image-text pairs, compute all N×N cosine similarities between image and text embeddings, and optimise a symmetric cross-entropy loss so each image's highest similarity is with its own caption and vice versa. Every other pair in the batch serves as a negative, which is why CLIP training uses huge batches (~32k) - more negatives make the task harder and the embeddings sharper. The original model trained on ~400M web-scraped image-text pairs.

Why it transfers: the supervision is **open-vocabulary natural language** rather than a fixed label set. An ImageNet classifier learns features sufficient to separate 1000 classes; CLIP has to organise visual features around anything humans write about images - objects, styles, scenes, text in the image, emotions. That yields three things. First, **zero-shot classification**: embed prompts like "a photo of a {class}" for each candidate class, embed the image, pick the nearest text embedding - the largest CLIP hits ~76% ImageNet top-1 with no ImageNet training. Second, **cross-modal retrieval** for free: text-to-image search is just nearest neighbours in the shared space. Third, and most consequentially, CLIP's image tower became the default **vision encoder for VLMs** - its language-aligned features are why gluing a ViT to an LLM with a small projector works at all.

Caveats a strong candidate volunteers: CLIP is weak on compositional structure - word order, object-attribute binding, counting (it behaves somewhat bag-of-words); its text encoder truncates at 77 tokens; and the two modalities occupy measurably separated regions of the "shared" space (the modality gap). SigLIP, which replaces the softmax contrastive loss with a pairwise sigmoid loss, scales better with batch size and is the common modern substitute.

**Follow-ups:** Why do large batches matter so much for contrastive learning? How would you use CLIP to build a zero-shot content moderation filter, and where would it fail? What's the modality gap and when does it bite?

</details>

### 3. How do images become tokens, and why does image resolution drive inference cost?

<details><summary><b>Answer</b></summary>

The vision encoder emits one embedding per patch, and each of those occupies a sequence position in the LLM exactly like a text token - so token count scales with (resolution ÷ patch size)². More pixels means more patches means more tokens, and you pay for tokens in dollars, latency, and context budget.

Concrete provider math: OpenAI's GPT-4o-class high-detail mode resizes the image and cuts it into 512×512 tiles at ~170 tokens per tile plus 85 base tokens (newer models count small patches, same area-scaling principle); Anthropic charges roughly (width × height) / 750 tokens and downscales anything over ~1568px on the long edge, capping an image around ~1.6k tokens; Gemini charges ~258 tokens for small images and tiles larger ones into 768×768 crops at ~258 tokens each. Order of magnitude to keep in your head: **a readable document page is ~1-2k tokens**, so a 100-page PDF sent as images is ~150k tokens per request - that's a real cost and may not even fit the context window.

This is why **tiling / dynamic resolution** schemes exist (LLaVA-NeXT's AnyRes, Qwen-VL's dynamic resolution): the model gets a downscaled global view plus native-resolution crops, spending tokens proportional to image size instead of a fixed budget. It's also why resolution is the first knob in any quality-vs-cost tradeoff: OCR accuracy on small text collapses below a legibility threshold, but pixels beyond the encoder's effective resolution buy nothing. A good answer connects this to prefill compute too - image tokens dominate prefill for vision-heavy workloads, which is where prompt caching of repeated images earns its keep.

**Follow-ups:** You're processing receipts and the model misreads totals - walk me through how you'd decide whether to raise resolution or change approach. Why does a resampler-based model (fixed 64 tokens per image) struggle with dense documents? How would you estimate the monthly bill for a screenshot-heavy agent?

</details>

### 4. What do vision-language models reliably get wrong?

<details><summary><b>Answer</b></summary>

Four families of failure, all predictable enough that they should shape any system design:

- **Counting**: beyond ~4-5 objects, counts are guesses. Patch-based encoders with attention pooling produce something closer to a bag of features than an enumerable scene representation.
- **Spatial reasoning**: left/right confusions, relative positions, relative sizes, and anything requiring precise geometry (reading an analog clock is a famous stumble). Contrastive pretraining never required spatial precision - a caption matches whether the dog is left or right of the chair.
- **Fine text and OCR under resolution pressure**: small or dense text degrades sharply once downscaling makes glyphs illegible. The dangerous version is **numeric hallucination** - the model outputs a *plausible* number rather than admitting it can't read the real one. A misread "$1,234.56" as "$1,284.56" sails through any fluency check.
- **Charts and hallucinated objects**: reading unlabelled values off axes is estimation, not extraction; and models name objects that plausibly co-occur with a scene but aren't present (the object-hallucination literature, e.g. the POPE benchmark, measures exactly this).

There's also a compositionality weakness inherited from contrastive vision encoders: attribute binding ("red cube left of blue sphere") and relations are shaky, as shown by bag-of-words-style probes like ARO.

Mitigations worth naming: increase effective resolution via tiling; crop-and-re-ask on regions of interest; route text-dense inputs through OCR and provide both the image and OCR text; use self-consistency (sample multiple reads, compare) for critical numbers; validate extractions against schemas and arithmetic checks (line items sum to total); and use tools - bounding-box grounding or a calculator - rather than trusting raw VLM output for counts and math.

**Follow-ups:** Why does contrastive pretraining specifically produce weak spatial reasoning? How would you detect numeric hallucination in production without humans reviewing every document? Which of these failure modes have reasoning models improved, and which persist?

</details>

### 5. Give me the intuition for how diffusion models generate images.

<details><summary><b>Answer</b></summary>

Two processes. The **forward process** is fixed and destructive: take a real image and add a small amount of Gaussian noise repeatedly - hundreds to a thousand steps, per a **noise schedule** that controls how much noise per step - until nothing but noise remains. The **reverse process** is learned: train a network that, given a noisy image and the timestep, predicts the noise that was added (equivalently, a cleaner version of the image). That's the whole training objective - regression on noise, sampled at random timesteps across the dataset (DDPM, 2020).

**Generation** runs the reverse chain: start from pure Gaussian noise, repeatedly apply the network to remove a bit of predicted noise, and after enough steps a coherent image emerges. The reason this works where "generate an image in one shot" is hard: each step is a small, well-conditioned correction. Early (high-noise) steps commit to global structure and composition; late steps refine texture and detail. The model never has to solve the whole problem at once - it learns a field of "which direction is more image-like from here" (the score), and sampling follows it.

Numbers worth knowing: training uses ~1000 discrete noise levels; sampling doesn't need to retrace all of them - modern samplers (DDIM and successors) produce good images in 20-50 steps, and **distilled** models (latent consistency models, adversarially distilled turbo variants) get to 1-4 steps, which is what makes real-time generation possible. Text conditioning enters through cross-attention onto text-encoder embeddings, and classifier-free guidance amplifies its effect at sampling time. Also say the phrase "latent diffusion" - production systems don't diffuse pixels, they diffuse a VAE-compressed latent - because it's the single biggest practical efficiency win in this stack.

**Follow-ups:** What exactly does the network predict - noise, the clean image, or something else, and does it matter? Why can samplers skip most of the 1000 training steps? What does the noise schedule trade off?

</details>

### 6. How does Whisper work, and why is it so robust compared to earlier ASR systems?

<details><summary><b>Answer</b></summary>

Whisper is a plain **encoder-decoder transformer** applied to speech. Audio is resampled to 16kHz and converted to a log-Mel spectrogram (a time-frequency image of the sound) in 30-second windows; the encoder processes the spectrogram; the decoder is an autoregressive text model that generates the transcript token by token, cross-attending into the encoded audio. It's seq2seq translation where the source language is sound.

The elegant part is the **multitask token interface**: the decoder's output is prefixed with special tokens that specify the task - language ID, transcribe vs. translate-to-English, whether to emit timestamps. One model, one architecture, task selected by prompt tokens rather than separate heads. Sizes ranged from ~39M (tiny) to ~1.5B (large) parameters.

Robustness comes from data, not architecture: **~680k hours of weakly-supervised** audio-transcript pairs scraped from the web, spanning accents, background noise, domains, and dozens of languages. Prior ASR systems trained on ~1k hours of clean read speech (LibriSpeech) achieved superhuman benchmark numbers but fell apart on real-world audio; Whisper traded a little benchmark WER for far better out-of-distribution behaviour. That "scale weak supervision beats curated supervision" lesson is the same one as CLIP's, and interviewers like hearing the parallel drawn.

Failure modes to volunteer: **hallucination on non-speech** - silence, music, or noise can trigger fluent invented text (it's a language model decoder; it wants to talk), repetition loops on long-form audio, and no native speaker diarization (who spoke when - needs a separate system). Long audio requires chunking with overlap and merge logic. The evaluation metric is **WER** (word error rate = insertions + deletions + substitutions over reference length), reported per-domain because aggregate WER hides accent and noise disparities.

**Follow-ups:** Why does Whisper hallucinate on silence, and how would you guard against it in production? How would you build streaming transcription from a 30-second-window batch model? What does weak supervision mean here and why did it beat curated data?

</details>

## Intermediate

### 7. Design a document-extraction system. When do you use an OCR pipeline versus sending pages to a VLM?

<details><summary><b>Answer</b></summary>

Start with the decision axes: **cost per page, accuracy on your specific fields, auditability, and document heterogeneity.**

**OCR pipeline**: layout analysis + text recognition (open-source Tesseract/PaddleOCR, or managed Textract / Google Document AI / Azure Document Intelligence) produces text with bounding boxes; an LLM (or templates, for fixed forms) extracts fields from that text. Strengths: cheap at scale - managed OCR runs on the order of ~$1.50 per 1,000 pages for plain text (~10× more with table/form analysis), roughly an order of magnitude cheaper than frontier-VLM page reads - self-hosted OCR widens that to 100×+; character-level coordinates enable click-to-verify audit UIs and redaction; behaviour is stable and debuggable. Weaknesses: multi-column reading order, complex layouts, handwriting, stamps, checkboxes, and tables that span pages - and OCR errors poison the downstream LLM silently.

**OCR-free VLM**: send the page image with an extraction prompt, get structured JSON back. Strengths: handles layout, handwriting, and visual context jointly; one stage to build and maintain; dramatically better on messy heterogeneous documents. Weaknesses: cost; **plausible-value hallucination** on fields it can't read (worst possible failure for invoices and medical records); most models don't return coordinates, weakening auditability; resolution limits on dense pages.

The production answer is a **cascade**: classify documents first; run cheap OCR on everything; handle clean, templated docs with the cheap path; escalate hard or high-value pages to a VLM - and when you do, give the VLM *both* the page image and the OCR text, since they fail differently and the combination beats either. Independently of path: validate against a schema (types, ranges, checksums like line-items-sum-to-total), compute per-field confidence, and route low-confidence extractions to human review. Measure per-field accuracy on a labelled set from your own traffic - public benchmark scores won't predict your invoice layout.

**Follow-ups:** How do you catch a VLM confidently misreading a dollar amount? Where does human-in-the-loop go, and how do you decide the confidence threshold? How does the calculus change at 10M pages/month?

</details>

### 8. How would you reliably extract tables and charts from documents?

<details><summary><b>Answer</b></summary>

Treat tables and charts as different problems: tables contain the data; charts usually only *depict* it.

**Tables.** For born-digital PDFs with embedded text, rule-based extractors (Camelot/Tabula-style, using ruling lines and text positions) are cheap and exact - try them first. For scanned or complex tables, either a table-structure model (e.g. Microsoft's Table Transformer, trained on PubTables-1M) reconstructs the grid from the image, or a VLM transcribes the table directly to markdown/HTML. VLMs are genuinely good at this now, including merged cells and multi-row headers - but they fail by *plausible reconstruction*: dropping a row, duplicating a line, or inventing a value while keeping perfect formatting. So validate structurally: consistent column counts, type checks per column, and arithmetic checks (subtotals sum, percentages hit ~100). For critical tables, transcribe twice (different temperature or crops) and diff - disagreement flags cells for review.

**Charts.** First ask whether the numbers exist as text: if data labels are printed, extraction is OCR-shaped and reliable. If not, the VLM is *estimating* values by visually interpolating against axes - treat outputs as approximations (±5-10% is common on bar charts, worse for scatter/log scales), and never feed them into downstream arithmetic as exact. Benchmarks like ChartQA use "relaxed accuracy" (within 5% counts as correct) precisely because of this. Where possible, go upstream for the source data; where not, extract axis ranges and tick values first (those are text, hence reliable), then ask for values relative to them - it measurably improves estimates.

Cross-cutting: render tables/charts at high resolution (tiling), crop the region of interest and re-ask rather than querying the full page, and keep provenance - page number and bounding region - attached to every extracted cell so humans can verify quickly.

**Follow-ups:** A VLM returns a beautifully formatted table with one hallucinated row - what catches it? When would you fine-tune a small model for table extraction instead of prompting a frontier VLM? How do you evaluate chart extraction when ground truth is only the image?

</details>

### 9. Why do latent diffusion? Walk me through the components of a Stable-Diffusion-style system.

<details><summary><b>Answer</b></summary>

Because pixel-space diffusion wastes compute on imperceptible detail. A 512×512 RGB image is ~786k values, and the denoising network runs 20-50+ times per generation over all of them. **Latent diffusion** first trains a **VAE** that compresses the image ~8× per side into a 64×64×4 latent - ~48× fewer values - and runs the entire diffusion process in that latent space. The perceptual compression (VAE) and semantic generation (diffusion) are cleanly separated: the VAE handles "what makes textures look real," diffusion handles "what makes scenes make sense." That factorisation is what brought image generation from cluster-scale to consumer-GPU-scale, and it's the reason the original paper is titled around *high-resolution* synthesis.

Components of the full system:

- **VAE encoder/decoder** - image ↔ latent. Only the decoder runs at generation time (once, at the end).
- **Denoising network** - historically a U-Net with attention; modern systems (SD3, Flux) use a **DiT** (diffusion transformer), which scales better and follows the same scaling-law playbook as LLMs. Newer models also swap DDPM-style noise prediction for **rectified flow / flow matching** objectives - straighter denoising trajectories, fewer sampling steps.
- **Text encoder(s)** - CLIP text towers and/or T5; embeddings enter the denoiser via cross-attention. T5's inclusion is a big reason newer models render text in images and follow long prompts better.
- **Sampler/scheduler** - the numerical integrator that steps from noise to latent; choice trades step count against quality.
- **Classifier-free guidance** at sampling time to sharpen prompt adherence.

Worth volunteering: the VAE is a quality *ceiling* - anything it can't reconstruct (historically: small faces, fine text) no amount of diffusion quality can recover, which is why later models upgraded to higher-channel latents (e.g. 16-channel in SD3-class models).

**Follow-ups:** Why 4 (or 16) latent channels rather than compressing harder? What does moving from U-Net to DiT buy? Where does ControlNet-style conditioning hook into this architecture?

</details>

### 10. Explain classifier-free guidance. What actually happens when you turn the scale up?

<details><summary><b>Answer</b></summary>

Classifier-free guidance (CFG) is the trick that makes conditional diffusion actually obey the prompt. During training, the text condition is randomly dropped (replaced with a null/empty embedding) ~10-20% of the time, so a single network learns both **conditional** denoising ("what does this noisy image look like given this caption") and **unconditional** denoising ("what does a generic image look like"). At sampling time you run both predictions and extrapolate:

```python
pred = eps_uncond + s * (eps_cond - eps_uncond)   # s = guidance scale
```

The vector `(eps_cond - eps_uncond)` isolates *the direction in which the prompt changes the prediction*; multiplying by `s > 1` exaggerates exactly that component. It replaced classifier guidance, which needed a separate noise-robust classifier and its gradients - CFG gets the same effect from the generative model itself, which is why it's "classifier-free."

Effects of the scale: `s = 1` is pure conditional sampling - prompt adherence is mediocre because the condition only weakly shifts the prediction. Typical operating range is ~5-9. As you push higher: prompt adherence and apparent sharpness improve, but **diversity collapses** (samples converge toward a prompt-archetype), colours oversaturate, contrast blows out, and anatomical/geometric artifacts appear - you're extrapolating outside the distribution the model was trained to denoise. Practical costs and consequences worth naming: CFG **doubles compute per sampling step** (two forward passes, usually batched); **negative prompts** are just replacing the unconditional branch's null embedding with an "away-from-this" condition, so the extrapolation points away from the negative; and distilled few-step models often bake guidance in during distillation, which is why turbo-style models expose no meaningful CFG knob.

**Follow-ups:** Why does high guidance hurt diversity specifically? How do negative prompts work mechanically? Why do guidance-distilled models generate at CFG ≈ 1?

</details>

### 11. Compare diffusion and autoregressive approaches to image generation. Why did AR come back?

<details><summary><b>Answer</b></summary>

**Autoregressive** image generation tokenizes the image - a VQ-VAE/VQGAN maps it to a grid of discrete codes from a learned codebook - and a transformer predicts those codes as a sequence, exactly like language modelling (DALL·E 1, Parti). **Diffusion** keeps the image continuous and generates by iterative parallel refinement of the whole canvas. Through 2022-2024 diffusion won on quality-per-FLOP and dominated; AR came back because of what it buys when the image generator *is* the LLM.

Tradeoffs:

- **Integration and instruction following**: an AR image head inside an omni-model (GPT-4o-style native image generation) shares the LLM's world knowledge and conversation state. That's why these systems are strikingly better at rendering long correct text in images, following multi-constraint prompts, and **conversational editing** ("same scene, but make it night") - the "prompt understanding" is the LLM itself, not a bolted-on CLIP/T5 encoder feeding cross-attention.
- **Latency shape**: diffusion does 20-50 full-canvas passes (1-4 when distilled); AR decodes thousands of image tokens sequentially, which is slow, though scale-prediction and parallel-decoding variants narrow the gap.
- **Fidelity bottlenecks**: AR quality is capped by the discrete tokenizer's reconstruction quality; diffusion's analogue is the VAE, but continuous latents lose less. Diffusion still tends to win on fine texture and photorealism per unit compute.
- **Training**: AR reuses the entire LLM stack - loss, infra, scaling laws (Parti showed clean scaling to 20B); diffusion has its own mature recipe and its transformer variant (DiT) gets similar scaling benefits.

The 2026 landscape is honestly hybrid: diffusion-first products for pure text-to-image quality and speed, AR/omni-model generation where editing, text rendering, and dialogue integration matter, and research blending both (AR over latents, diffusion heads on LLMs). A strong answer refuses to declare a single winner and instead maps approach to product requirement.

**Follow-ups:** Why do omni-models render text in images so much better? What does the discrete tokenizer bottleneck AR generation on? If you needed 100ms generation for a live preview feature, which family and what tricks?

</details>

### 12. Design a production voice agent. Pipeline vs speech-to-speech, the latency budget, and interruption handling.

<details><summary><b>Answer</b></summary>

Two architectures. The **pipeline**: streaming ASR → LLM → streaming TTS. The **native speech-to-speech model**: one model consumes and emits audio tokens directly (GPT-4o Realtime-style; open equivalents like Moshi).

**Latency is the defining constraint.** Human turn-taking gaps average ~200ms; anything over ~1 second voice-to-voice feels laggy, so the bar is **sub-second, target ~500-800ms**. A pipeline's budget decomposes roughly as: VAD/endpointing 100-300ms (you must wait to decide the user finished - the irreducible tax), streaming-ASR finalisation ~100-200ms, LLM time-to-first-token 200-500ms, TTS time-to-first-audio 100-300ms, plus network. Naively summed you blow the budget, so everything overlaps: ASR streams partials while the user speaks, the LLM starts on the endpoint (or speculatively before it), TTS begins on the first sentence rather than the full reply, and audio plays while later sentences generate. A small/fast model for the conversational layer with tool calls to heavier systems is a common split. Speech-to-speech models collapse the stack - ~300ms-class average response is achievable - and they hear prosody (sarcasm, hesitation, emotion) and generate expressive audio without a lossy text bottleneck. Their cost: the text midpoint disappears, so guardrails, logging, evals, and precise output control get harder, and tool integration runs through event protocols rather than plain text.

**Interruptions (barge-in)** are mandatory, not a nicety: run echo cancellation so the mic doesn't hear the agent's own output; run VAD continuously *during* playback; on detected user speech, stop TTS within ~100-200ms, cancel in-flight LLM generation, and - critically - truncate conversation state to what the user actually *heard*, not what you generated, or the agent will reference things it never said aloud. Also handle backchannels ("mm-hmm" shouldn't trigger a full stop) - a small classifier on the interrupting audio helps.

**Follow-ups:** Where do you put safety filtering in a speech-to-speech architecture with no text midpoint? How do you evaluate a voice agent end-to-end? The user interrupts mid-tool-call - what state do you roll back?

</details>

### 13. How do models understand video, and what are the current limits?

<details><summary><b>Answer</b></summary>

Predominantly: **sample frames, encode them like images, add the audio track, and let the LLM reason over the sequence.** The default is uniform sampling around ~1 fps (Gemini's documented approach; ~258 tokens per frame there). The immediate consequence is cost: at ~1 fps, an hour of video is ~3,600 frames ≈ ~1M tokens - video is the most token-hungry modality by far, and most practical engineering is about spending those tokens well.

Sampling strategies, in increasing sophistication: **uniform** (simple, misses fast events between samples); **scene-change/keyframe detection** (cheap classical CV picks visually distinct frames - much better token efficiency on cut-heavy content); **query-aware two-pass** (cheap low-fps pass to segment and summarise, then re-sample the relevant window densely - the video analogue of retrieve-then-read); and **audio-first** (transcribe with ASR, use the transcript to locate moments, then look at frames - for talky content the transcript carries most of the information at a fraction of the cost).

Limits to name honestly: **temporal reasoning** is the weak spot - event ordering, causality ("did he fall because the ladder slipped?"), counting repetitions (exercise reps is a classic failure), and anything happening *between* sampled frames (fast motion, subtle actions). Long-horizon coherence degrades: a needle-in-haystack frame in hour two competes with a million tokens of context. Native video encoders that model motion across frames exist in research and in parts of frontier stacks, but sampled-frames-plus-LLM remains the deployed norm.

Production checklist: match sampling rate to the question (surveillance ≠ lecture summarisation), cache encoded video for repeated queries (prompt caching matters enormously here), and consider frame-level retrieval - embed frames, retrieve relevant timestamps per query - instead of stuffing the whole video into context.

**Follow-ups:** How would you build "find when the package was delivered" over 24h of doorbell footage without ingesting 24h of tokens? Why is counting event repetitions so hard? When does 1 fps break down?

</details>

### 14. Build text-to-image search over 100M product images. Walk me through the design.

<details><summary><b>Answer</b></summary>

The backbone is a **CLIP-style dual encoder**: offline, embed all 100M images with the image tower into an ANN index (HNSW or IVF-PQ - at 100M vectors, quantization matters for memory: 100M × 768 dims × fp16 ≈ 150GB raw, so product-quantize or use a vector DB that does); online, embed the text query with the text tower and take nearest neighbours by cosine similarity. Because both modalities share one space, cross-modal retrieval is literally nearest-neighbour search - that's CLIP's superpower - and the same index gives image-to-image "find similar" for free.

What separates a senior answer is the practical failure list:

- **Domain shift**: stock CLIP is trained on web alt-text; "SKU-style" queries ("men's slim-fit oxford, navy, 15.5/34") aren't captions. Fine-tune the dual encoder on your own (query, clicked-product-image) pairs with hard negatives - click logs are the goldmine. SigLIP-class checkpoints are a stronger starting point than original CLIP.
- **Text encoder limits**: CLIP's 77-token cap and caption bias - long or attribute-heavy queries need either a fine-tuned encoder or query rewriting into caption style.
- **Attribute binding**: "red shirt with blue logo" retrieving blue shirts with red logos is the classic contrastive-encoder failure. Fix in reranking, not retrieval: run the top ~50 candidates through a VLM reranker ("does this image match this description?") or match structured attributes extracted at ingestion.
- **Hybrid with metadata**: pure visual search loses to metadata filters on price/brand/size; the right system is vector search *and* structured filters *and* BM25 over titles, fused.
- **The modality gap**: image and text embeddings cluster in separate cones, so absolute cosine scores are miscalibrated across modalities - rank within a query, don't threshold across queries without calibration.

Evaluate with recall@k on labelled (query, relevant-set) pairs from real traffic, plus online CTR/purchase-through A/B tests.

**Follow-ups:** How do you mine hard negatives from click logs without poisoning training with position bias? A merchandiser complains "red dress" surfaces orange dresses - debug path? When is a caption-then-BM25 pipeline actually better than embedding search?

</details>

## Advanced

### 15. Design multimodal RAG over 50k PDFs full of tables, charts, and diagrams. Where does ColPali-style retrieval fit?

<details><summary><b>Answer</b></summary>

Three architectures, in ascending fidelity:

1. **Parse-to-text RAG**: extract text, chunk, embed, retrieve. Fails the premise - charts and diagrams vanish, tables mangle. Baseline only.
2. **Caption-and-embed**: at ingestion, a VLM writes a dense description of every figure, chart, and table; descriptions are embedded alongside body text (tables often dual-indexed as markdown + description). At answer time, retrieve descriptions but hand the *original image* to the VLM for generation - the caption is a retrieval key, not the evidence. This is the pragmatic production default: works with any text-retrieval stack, cheap at query time. Its ceiling: retrieval quality is capped by caption quality - whatever the captioner didn't mention is unfindable.
3. **Screenshot-based retrieval (ColPali)**: skip parsing entirely. A VLM (PaliGemma in the original paper) encodes each **page image** into ~1k patch-level embeddings; queries encode into token-level embeddings; scoring is ColBERT-style **late interaction** - for each query token, take the max similarity over the page's patch vectors, and sum. Because matching happens at patch granularity, a query about "the latency graph" can match the actual chart region without anyone having described it. On visually-rich document benchmarks (ViDoRe) this beats OCR-based pipelines significantly. Costs: **multi-vector storage** (~1k vectors per page, and 50k PDFs can easily mean a million pages - mitigated by pooling and binary quantization, but real), ingestion GPU time, and answer-time cost since retrieved evidence is page *images* the generator VLM must read (~1-2k tokens per page).

My design for 50k PDFs: hybrid. Text-chunk retrieval and ColPali-style page retrieval run in parallel, fused (RRF), with retrieved pages rendered to the VLM as images alongside top text chunks. Cite page numbers with thumbnail provenance. Evaluate retrieval (recall@k on a labelled query set, checking specifically that figure-dependent questions retrieve the right pages) separately from generation faithfulness.

**Follow-ups:** How do you keep multi-vector storage from exploding at 5M pages? When is caption-and-embed strictly better than ColPali? How do you evaluate whether chart-dependent questions are actually being answered from the chart?

</details>

### 16. How do you evaluate multimodal systems - understanding and generation?

<details><summary><b>Answer</b></summary>

**Understanding.** The standard instruments are VQA-style benchmarks: VQAv2 (natural-image QA), TextVQA and OCRBench (text-in-image), DocVQA (documents - scored with ANLS, a normalized edit-distance metric that forgives near-miss strings), ChartQA (charts - "relaxed accuracy," within 5% of the true value, because exact chart reading is estimation), and MMMU (college-level multi-discipline reasoning) as the flagship capability benchmark. Know the caveats you'd raise as a practitioner: contamination (benchmarks leak into training data; treat vendor-reported numbers sceptically), and the short-answer format's mismatch with real product tasks. For open-ended outputs, **VLM-as-judge** with an explicit rubric works, with two rules: the judge must actually see the image (a text-only judge scoring image answers is a real and embarrassing anti-pattern), and the judge inherits VLM blind spots - don't judge counting or spatial tasks with a model that fails them; verify judge-human agreement on a calibration set first.

For products, the benchmark that matters is one you build: for document AI, **per-field extraction accuracy** on a few hundred labelled documents from your own traffic, sliced by document type and field criticality, catches regressions no public benchmark will.

**Generation.** Three layers: **FID** compares feature distributions of generated vs. real image sets - fine for training-run comparisons, meaningless for a single image, and gameable; **CLIPScore** measures prompt-image alignment via embedding similarity - cheap, but inherits CLIP's blindness to composition and counting; **compositional checks** (GenEval-style: detector-verified object counts, colours, positions) probe exactly what CLIPScore misses. None of these substitute for **human evaluation** - side-by-side preference (arena-style Elo) remains the gold standard, splitting judgments into fidelity, prompt adherence, and aesthetics because they diverge. ASR is WER per domain/accent slice; TTS is MOS-style human ratings plus WER-of-ASR-on-output as an automatic intelligibility proxy.

**Follow-ups:** Your VLM-judge agrees with humans 70% of the time - usable? How would you detect that a benchmark leaked into a vendor's training data? Design the eval for a chart-heavy financial-document assistant.

</details>

### 17. Compare projector/adapter designs - MLP vs resampler vs cross-attention. How does the choice interact with the training recipe?

<details><summary><b>Answer</b></summary>

Three families:

- **Linear/MLP projection** (LLaVA line): map every patch embedding into the LLM's embedding space, splice inline. Lossless - all visual detail reaches the LLM - and trivially simple, but token cost scales with resolution: with tiling, a single high-res image can be 2-3k tokens. The pragmatic modern compromise adds light pooling (e.g. 2×2 average of adjacent patch tokens) to cut tokens ~4× with modest loss.
- **Resampler / Q-Former** (Flamingo's Perceiver Resampler, BLIP-2): a small transformer with N learned query vectors (~32-64) cross-attends into the patch features and outputs exactly N tokens regardless of input size. Constant, cheap token budget - great for interleaved many-image contexts and video - but it's a lossy information bottleneck: fixed capacity regardless of content is precisely wrong for dense documents, which is why resampler-based models historically lagged on OCR/document benchmarks and why the field swung back to MLP+tiling as document use cases became dominant.
- **Cross-attention insertion** (Flamingo's gated cross-attn layers): vision never enters the token sequence; instead, new cross-attention layers interleaved into the frozen LLM read visual features directly. Zero context consumed, and gating (initialized to zero) provably preserves the base LLM at initialization - but you're modifying the LLM's architecture, adding parameters per layer, and complicating serving; it has largely lost to the inline-token approaches in open models.

Interaction with training: MLP projectors enable the cheap staged recipe - stage 1 trains only the projector (millions of caption pairs, both towers frozen), stage 2 unfreezes the LLM for instruction tuning; whether to unfreeze the *vision encoder* is a real decision (unfreezing helps at scale with enough data, but degrades the encoder on small budgets). Resamplers have more trainable capacity in the adapter itself, needing more stage-1 data. High-resolution support is its own late stage - you extend tiling after basic alignment. And the projector choice sets the KV-cache and prefill economics of every future inference: fixed-64-token images are 20-30× cheaper to serve than 2k-token images.

**Follow-ups:** Why did resampler-based models underperform on DocVQA? When would you unfreeze the vision encoder and what can go wrong? How does token-per-image count change multi-image and video capability?

</details>

### 18. You need to process 10M document pages per month. VLM or traditional OCR? Do the math.

<details><summary><b>Answer</b></summary>

Set up the unit economics first, then let accuracy requirements pick the point on the curve.

**VLM path**: a page at readable resolution is ~1.5k input tokens, plus prompt; structured output ~500 tokens. 10M pages ≈ ~15B input + ~5B output tokens/month. At small-model pricing (~$0.15/M input, ~$0.60/M output) that's ~$2k + $3k ≈ **~$5k/month**; at frontier pricing (~$3/M input, ~$15/M output) it's ~$45k + $75k ≈ **~$120k/month**. Batch APIs typically cut this ~50% if latency allows. Self-hosting an open VLM changes the calculus to GPU-hours: at ~1-2s/page per GPU, 10M pages is ~3-6k GPU-hours/month - tens of thousands of dollars on cloud H100s, less on reserved capacity, plus engineering.

**OCR path**: managed OCR runs ~$1.50 per 1,000 pages for plain text (**~$15k/month**), roughly 10× more with table/form analysis; self-hosted open OCR is near-pure compute at cents per thousand pages. But OCR alone doesn't extract fields - add an LLM pass over the OCR *text* (~500-800 tokens/page instead of 1.5k of image tokens, and cheap models suffice) for a few thousand dollars more.

So the naive comparison - small VLM (~$5k) vs OCR+LLM (~$5-20k) - is closer than most people expect in 2026; the real differentiators are elsewhere: **accuracy on your fields** (handwriting and messy layouts favour VLMs; clean templated forms don't need one), **auditability** (OCR gives coordinates; most VLMs don't), **error character** (OCR fails visibly with garbage; VLMs fail invisibly with plausible values - the latter is worse for financial data), and **latency/throughput**.

My actual recommendation is a **cascade**: document classifier up front; templated/clean pages through OCR+small-LLM; hard pages (handwriting, degraded scans, weird layouts - maybe 10-20% of volume) through a VLM with both image and OCR text; validation and low-confidence human review at the end. That buys ~VLM accuracy at ~OCR-dominated cost.

**Follow-ups:** How do you decide the escalation threshold in the cascade? At what accuracy delta does the frontier model justify 20× cost? How does the answer change if 40% of pages are handwritten?

</details>

### 19. How does modern TTS work, and what makes speech generation hard in a real-time product?

<details><summary><b>Answer</b></summary>

Two generations of architecture. **Classic two-stage**: an acoustic model converts text (usually phonemes) to a mel spectrogram - Tacotron 2 autoregressively, FastSpeech 2 in parallel with explicit duration/pitch prediction - and a **neural vocoder** (HiFi-GAN class) converts spectrogram to waveform. Robust and fast, still widely deployed, but speaker identity is baked in at training and expressiveness is limited.

**Codec language models** are the modern paradigm: a neural audio codec (EnCodec/SoundStream) compresses waveforms into discrete token streams at a few hundred tokens/second; an autoregressive transformer then generates audio tokens conditioned on text - VALL-E established the pattern. Because it's just a language model over audio tokens, you get in-context learning: condition on a few seconds of reference audio and it continues in that voice - **zero-shot voice cloning**, which is simultaneously the headline feature and the headline safety problem. Diffusion/flow-based TTS is the other strong family, generally winning on stability, with codec-LMs winning on expressiveness and cloning.

What's actually hard:

- **Prosody depends on meaning**: emphasis, phrasing, and intonation require understanding the sentence - "I never said she stole it" has seven readings. LLM-adjacent TTS is closing this gap; it's why omni-models speaking natively can sound better than pipeline TTS.
- **Text normalization**: "Dr.", "3/4", "$1,024", "2026-07-12" - classic, unglamorous, still a top source of production bugs.
- **Streaming and latency**: a voice agent needs **time-to-first-audio ~100-300ms**, so you synthesise incrementally as LLM text streams in. The trap: prosody is a function of the *whole* sentence - chunk mid-clause and you get unnatural contours or pitch discontinuities at boundaries. Practical fixes: chunk at clause/sentence punctuation, small lookahead buffer, overlap-fade at joins.
- **Long-form stability**: AR audio models can loop, skip words, or drift in energy over paragraphs - guard with alignment checks (run ASR over the output and compare WER against the input text as an automatic regression signal).
- **Cloning abuse**: consent verification for voice enrolment and watermarking of synthetic audio are table stakes for any cloning feature.

**Follow-ups:** Why does sentence-chunked streaming TTS sound choppy and how do you fix it? How would you automatically regression-test TTS quality in CI? What changes when TTS moves inside a speech-to-speech omni-model?

</details>

### 20. Adapter-based VLMs vs natively multimodal (early-fusion) models - what's the real tradeoff?

<details><summary><b>Answer</b></summary>

**Adapter-based** (late fusion): take a pretrained vision encoder and a pretrained LLM, glue them with a projector, train the glue and fine-tune. **Natively multimodal** (early fusion): one transformer pretrained from scratch on interleaved multimodal data - either discrete tokens for everything (Meta's Chameleon tokenizes images with a VQ tokenizer into the same vocabulary as text) or continuous patch embeddings without a separate encoder (Fuyu feeds linearly projected patches straight into the decoder). Gemini was natively multimodal from its first pretraining; GPT-4o brought native audio in/out.

Why adapters dominate open-source: they're **cheap and modular** - you reuse two paid-for pretrainings, alignment training is a rounding error of LLM pretraining cost, and you can swap encoders or upgrade the LLM independently. Their structural ceiling: the vision encoder is a **frozen bottleneck** trained on a contrastive objective - whatever CLIP-style pretraining didn't preserve (precise spatial detail, fine text at odd resolutions) is gone before the LLM ever sees the image, and the two representation systems only meet at a thin interface late in training.

What early fusion buys: **deeper cross-modal integration** (attention mixes modalities from layer 0, learned jointly across all of pretraining rather than in a short alignment phase), **unified generation and understanding** (a token-based model emits image tokens as readily as text - one model both reads and draws, enabling native image generation and true interleaved output), and freedom from encoder constraints (Fuyu handles arbitrary resolutions and aspect ratios by construction). What it costs: full multimodal pretraining at frontier scale, delicate data mixture balancing (modalities can degrade each other), and real training-stability problems - Chameleon documented divergences from modality competition under a shared softmax, requiring QK-norm and norm-placement surgery to train at all.

The honest 2026 summary: frontier labs converged on native multimodality because at their compute scale the integration quality wins; the open ecosystem remains overwhelmingly adapter-based because the recipe is reproducible for ~0.1% of the cost - and for most understanding tasks, well-executed adapters remain competitive.

**Follow-ups:** Why does a shared softmax over mixed-modality tokens cause instability? If you had one frontier pretraining run, what data-mixture questions would you have to answer? Where do adapter models still beat native ones on benchmarks, and why?

</details>

### 21. You're shipping an image-generation feature. Walk me through the safety design: NSFW filtering, deepfakes, and provenance.

<details><summary><b>Answer</b></summary>

Defence in depth across four stages - no single layer survives contact with adversarial users.

**Training time**: filter the training corpus (NSFW, CSAM via hash-matching against known-material databases like PhotoDNA/NCMEC's, and decide your policy on real people and artist styles) - capability the model never learned is the only filter that can't be jailbroken. **Input time**: prompt classifiers plus policy checks, catching not just explicit requests but circumlocution ("attractive person, no clothes, artistic"); for image inputs (editing/reference features), scan uploads - real-person likeness, minors, and known-CSAM hashes; combining an uploaded face with sexualised or violent prompts is *the* deepfake abuse vector, so face-editing paths deserve the strictest rules. **Output time**: run vision classifiers on every generated image before display (nudity, violence, real-person likeness); this catches emergent unsafe outputs from innocent-seeming prompts. Tune thresholds knowing base rates: at millions of generations/day, a 1% false-positive rate is a support catastrophe - measure both directions.

**Provenance** - know the two mechanisms and their distinct failure modes: **C2PA Content Credentials** attach a cryptographically signed manifest (who made it, with what tool, edit history) - strong when present, but it's metadata: screenshots, re-encodes, and platform stripping remove it, so absence proves nothing. **Invisible watermarking** (Google's SynthID class) embeds a signal in pixels that survives compression, resizing, and mild edits - more robust, but detectable only with the owner's detector and removable by determined adversaries. Ship both; OpenAI, Google, and Meta all do some combination. Say the honest part: provenance lets *your* content be identified; it does not solve deepfake *detection* in the wild - post-hoc classifiers for arbitrary synthetic media are an unreliable arms race, which is why policy (impersonation rules, takedown processes) and regulation (EU AI Act synthetic-media transparency obligations) carry weight that classifiers can't.

Operationally: red-team continuously (jailbreaks evolve weekly), log for abuse-pattern review, human-review appeal paths for false positives, and rate-limit + investigate accounts probing the filters.

**Follow-ups:** A user screenshots the image - what survives, C2PA or SynthID, and why? How do you evaluate an NSFW classifier before launch, and what base-rate math matters? What changes for an open-weights release where you don't control inference?

</details>
