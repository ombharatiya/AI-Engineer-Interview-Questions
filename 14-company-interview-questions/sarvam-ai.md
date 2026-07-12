# 🪔 Sarvam AI - AI Engineer Interview Questions

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, technical reports, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- Sarvam runs a **proof-of-work** loop, not a LeetCode marathon. Multiple candidate reports describe a **long, proctored build session** (one report: ~2.5 hours to build a Voice Activity Detector from scratch) where you are allowed to use any tool, including AI coding assistants. The signal is: can you ship a working thing under time pressure.
- Loop shape varies by team and is only moderately documented. A common pattern from public reports: **briefing call -> time-boxed practical task/assignment -> follow-up technical rounds that dig into your submission -> a DSA-ish round in some tracks -> founder/CTO and HR conversations.**
- They weight **Indic language depth** heavily: multilingual tokenization and fertility, code-mixed (Hinglish) handling, transliteration and script normalization, and low-resource adaptation. Generic English-only NLP answers read poorly here.
- **Speech and voice pipelines** are core product surface (Saaras ASR, Bulbul TTS, real-time voice agents). Expect at least one round that touches streaming latency, VAD/endpointing, or ASR/TTS for Indian languages if you are on an applied or agents track.
- **Efficiency and pragmatism** run through everything: small models that punch up (Sarvam-1 is 2B), MoE at the frontier (Sarvam-105B with ~9B active), quantization, on-device (Sarvam-Edge), and sovereign/on-prem deployment. They are building for cost-sensitive, population-scale, sometimes offline settings.

## Company context

Sarvam AI is India's sovereign-AI frontier lab: founded in August 2023 in Bengaluru by Vivek Raghavan and Pratyush Kumar (both from AI4Bharat at IIT Madras), it builds LLMs, speech models, and voice agents centred on Indian languages. It was selected under the government's IndiaAI Mission to build India's sovereign foundation model, receiving one of the mission's largest compute allocations (a reported ~4,096 H100 GPUs for about six months) to train a family of models (Sarvam-Large, Sarvam-Small, Sarvam-Edge). Its public model lineup spans Sarvam-1 (a 2B Indic base model), Sarvam-M (24B, built on Mistral Small), the newer Sarvam-30B and Sarvam-105B MoE models, plus Saaras (ASR), Bulbul (TTS), Mayura (translation), and Sarvam Vision. The team is small and high-bar and backed by Lightspeed, Peak XV, and Khosla Ventures (unicorn valuation as of the 2026 Series B). "AI engineer" here usually means end-to-end ownership: you might tune a model, wire an agent harness, build a low-latency voice pipeline, and deploy it on-prem for a government or enterprise customer, often in the same quarter.

## Roles & titles they hire

From their public careers page (sarvam.ai/careers), recurring archetypes include:

- **Applied AI Engineer, Sarvam Agents** - design agent flows, wire up tools, ship the harness, own agent reliability in production
- **Full Stack AI Engineer** - build production-grade systems from infra up through the services on top (RAG, copilots, document intelligence)
- **AI Engineer - Intern** - product features across the full stack: RAG, agents, copilots, document intelligence for education and healthcare use cases
- **Forward Deployed Software Engineer** (roughly 2-5 years) - work directly with customers and product teams to ship real solutions in production
- **Backend Engineer, API Team** - the serving and API layer behind the models
- Plus research-leaning roles around pretraining, post-training, speech, and Indic data

Roles cluster in Bengaluru, mostly in-person given the startup's velocity.

## The interview loop

Public detail is moderate and comes mostly from candidate write-ups (Glassdoor, Grapevine, individual blogs) rather than an official published process, so exact rounds vary by team and seniority. The consistent theme across reports is **proof of work over algorithmic trivia**: a practical, tool-allowed build task is the centrepiece. The table below is assembled from those reports and clearly marks what is inference.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter / briefing call | ~30 min, explains the task and expectations (reported, varies) | Motivation, background, "why Sarvam / why Indic AI" |
| Practical task / assignment | Time-boxed build; one report describes a ~2.5 hr proctored session (e.g. build a VAD from scratch), any tools allowed including AI assistants (reported, varies) | Can you ship a working solution fast; setup speed, debugging under pressure, library fluency |
| Technical deep-dive on your submission | 1-2 rounds discussing your code, logic, and design choices (reported, varies) | Depth behind the build; tradeoffs, what you would change, why |
| Founder / CTO "induction" round | One report: self-intro plus 2 problems to solve with LLM use allowed, ~1 hr (reported, varies) | Raw problem-solving, communication, culture and drive |
| DSA / fundamentals round | Present in some tracks per reports; not universal (reported, varies) | Core CS fundamentals where the role needs them |
| HR / offer | Discussion | Fit, expectations, logistics |

Reported end-to-end timelines are short for the category, often around 1-2 weeks. Because the loop is not officially published and varies, ask your recruiter exactly what each stage evaluates and whether AI tools are permitted in the build round (reports say yes, but confirm).

## What they emphasise

- **Indic tokenization and fertility.** Sarvam-1's headline is a tokenizer with fertility of 1.4-2.1 across supported languages, described as 2-4x more efficient than existing multilingual tokenizers. If you cannot explain why an English-centric tokenizer mangles Devanagari or Tamil and what that costs, you are not calibrated for this company.
- **Code-mixed, real-world Indian speech and text.** Their ASR (Saaras) is tuned for Hinglish, telephony-quality 8 kHz audio, and code-switching. Handling "Main kal market ja raha hoon" without forcing it into pure Hindi or pure English is a first-class requirement, not an edge case.
- **Low-latency voice pipelines.** Voice agents pairing Saaras (ASR) + an LLM + Bulbul (TTS) target sub-250ms streaming latency. Streaming, endpointing/VAD, barge-in, and partial hypotheses are expected fluency for applied/agents roles.
- **Efficiency across the size spectrum.** From a 2B base model to a 105B MoE with ~9B active params to on-device Sarvam-Edge, the through-line is quality per FLOP and per rupee. Quantization, MoE routing, and small-model tricks matter.
- **Adaptation with scarce data.** Building for 10+ Indian languages, many low-resource, means synthetic data generation, transliteration, continued pretraining, and tokenizer surgery are daily tools, not exotica.
- **Sovereign, population-scale, pragmatic delivery.** On-prem/air-gapped deployment, data residency, and forward-deployed customer work (government, enterprise) reward engineers who own the whole stack and ship, not just model in a notebook.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Why is tokenization the first bottleneck for Indian-language LLMs, and how does a low-fertility tokenizer like Sarvam-1's change the economics?

<details><summary><b>Answer</b></summary>

Fertility is tokens per word. An English-centric BPE tokenizer (say Llama's) has never seen much Devanagari, Tamil, or Bengali script, so it falls back to near byte-level splitting: a single Hindi word can explode into many subword or byte tokens, often roughly 4-8 (illustrative, varies by tokenizer and word). Sarvam-1's tokenizer reports fertility of 1.4-2.1 across its 10 Indic languages, described as 2-4x more efficient than typical multilingual tokenizers.

Why this dominates everything downstream: (1) **Cost and speed** scale with token count, so a 4x fertility gap means a 4x longer sequence for the same sentence, i.e. 4x the KV cache, compute, and latency, and roughly 4x the API cost for equivalent text. Sarvam reports this contributes to 4-6x faster inference versus larger models. (2) **Effective context shrinks.** An 8k context that holds a long English document might hold a quarter as much Hindi, so RAG chunks, few-shot examples, and conversation history all get squeezed. (3) **Quality suffers.** When words shatter into byte fragments, the model wastes capacity relearning that these fragments compose a word, and morphology (Indian languages are heavily inflected) is harder to model. Better token boundaries free capacity for actual semantics.

The design lever is training tokenizer vocabulary on a balanced, script-aware corpus so common Indic morphemes get their own tokens, and sizing the vocab so no single language starves. The tradeoff is vocab budget: every language you cover well costs embedding rows and softmax compute, so you balance coverage against a fixed vocabulary size.

**Follow-ups:** How would you measure fertility empirically across a multilingual corpus? What breaks if you simply bolt 20k new Indic tokens onto an existing English tokenizer's vocab?

</details>

### 2. Build a Voice Activity Detector from scratch: detect where speech is present in an audio stream. How do you approach it, and how do you make it robust for phone-quality Indian-language audio?

<details><summary><b>Answer</b></summary>

Start simple and layer up, because the interviewer wants a working pipeline plus judgement about failure modes. A minimal energy-based VAD over 20-30 ms frames:

```python
import numpy as np

def frame_signal(x, sr, frame_ms=25, hop_ms=10):
    n = int(sr * frame_ms / 1000); hop = int(sr * hop_ms / 1000)
    return np.stack([x[i:i+n] for i in range(0, len(x)-n, hop)])

def vad(x, sr, thresh_db=-40, hang=5):
    frames = frame_signal(x, sr)
    energy = 10 * np.log10((frames**2).mean(axis=1) + 1e-10)
    speech = energy > thresh_db
    # hangover: keep trailing frames to avoid clipping word endings
    out, count = speech.copy(), 0
    for i in range(len(speech)):
        if speech[i]: count = hang
        elif count > 0: out[i] = True; count -= 1
    return out
```

Then explain why raw energy is not enough and what I would add: (1) a **noise floor estimate** that adapts, since a fixed dB threshold fails across a quiet office and a noisy street or 8 kHz telephony line; (2) **zero-crossing rate and spectral features** to separate speech from stationary hum; (3) **hangover / hysteresis** (shown above) plus a minimum-speech-duration so we do not clip the soft ends of Indian-language words or trigger on clicks; (4) for production, a small **learned model** (a lightweight neural VAD like an RNN or the Silero-style CNN) trained on labelled Indic telephony audio, because code-mixed conversational speech with background TV, traffic, and cross-talk defeats hand-tuned thresholds.

The reason VAD matters for a voice agent is **endpointing**: it decides when the user stopped speaking so the ASR can finalise and the LLM can respond. Too eager and you cut people off mid-sentence (worse in languages with trailing vowels); too slow and latency balloons. Tune the trailing-silence timeout as a product decision, and support barge-in so the user can interrupt TTS.

**Follow-ups:** How do you tune the endpoint silence timeout differently for a form-filling bot versus open conversation? How would you evaluate VAD quality without frame-level labels?

</details>

### 3. Design a real-time voice agent for a citizen helpline in Hindi and three regional languages, targeting sub-250ms perceived latency over a phone line. What is the architecture?

<details><summary><b>Answer</b></summary>

The pipeline is ASR -> LLM -> TTS, but the whole game is streaming and overlap so the caller never hears dead air. Components map to Sarvam's stack: **Saaras** for streaming ASR (tuned for Indian accents, code-mixing, and 8 kHz telephony), an LLM (a Sarvam model), and **Bulbul** for TTS.

Latency budget, and how to hide it: (1) **Streaming ASR over a WebSocket** emits partial hypotheses as the user speaks, so transcription is nearly done the moment they stop. (2) **VAD-based endpointing** (see the VAD question) fires the turn boundary; tune the trailing-silence timeout, since that single number dominates perceived responsiveness. (3) **Stream the LLM** token by token, and start **TTS on the first sentence or clause** rather than waiting for the full answer. Bulbul streaming audio out means first audio can play within a few hundred ms of the user finishing. (4) **Barge-in**: run VAD on the inbound line even while TTS plays so the caller can interrupt, which you must handle or the bot feels robotic.

Design choices that matter here: keep the LLM turn short and structured (helplines are task-oriented, so bias toward retrieval-grounded, concise answers); pre-warm and pin models to avoid cold starts; co-locate ASR/LLM/TTS to kill network hops; and for a government helpline, likely **on-prem/sovereign** deployment with call recording and audit for compliance. Handle telephony realities: 8 kHz mono, packet loss, DTMF, and long silences. Add a fallback to a human agent and a deterministic path for high-stakes intents (do not let the model freelance on, say, benefit eligibility).

Perceived latency is not end-to-end compute; it is time-to-first-audio plus never leaving a gap, so overlap ASR finalisation, LLM generation, and TTS aggressively.

**Follow-ups:** Where would you cache to cut latency for common queries? How do you keep the LLM from switching language mid-answer when the user code-mixes?

</details>

### 4. Whisper transcribes Hinglish poorly, often forcing output into one language or hallucinating. Why, and how would you build an ASR that handles code-mixed speech?

<details><summary><b>Answer</b></summary>

The root cause is training distribution and modelling assumptions. Whisper is trained mostly on monolingual web audio with a single language token per utterance, so it treats language as a global switch rather than something that flips word to word. Given "Main kal market ja raha hoon", it tries to commit the whole utterance to Hindi or English, producing script inconsistency, transliteration errors, or, in low-energy segments, confident hallucination (a known Whisper failure on silence and accented speech). It also underrepresents Indian accents and telephony audio.

What Sarvam's Saaras does differently, and what I would replicate: (1) **Train on real Indian code-mixed and vernacular speech at scale** - thousands of hours across accents, dialects, and 8 kHz telephony, so the acoustic model actually knows these phonetics. (2) **Decide the output convention deliberately.** For Hinglish you usually want to keep English words in Latin and Hindi words in their spoken form rather than force-translating; that is a labelling and post-processing decision, and you optimise the model toward it rather than fighting a monolingual prior. (3) **Allow intra-utterance language switching** instead of one global language token, so the model can flip mid-sentence. (4) **Robust endpointing and anti-hallucination**: pair with a good VAD and suppress output on non-speech to avoid Whisper's silence-hallucination behaviour.

Practical build: fine-tune or continue-train a strong multilingual acoustic model on curated Indic + code-mixed data, use a tokenizer/vocab that covers the relevant scripts and Latin, and evaluate on a **code-mixed test set with WER plus a code-switch-aware metric**, because standard WER on a forced-monolingual reference will mislead you. Streaming matters too: partial hypotheses need to stay stable as context arrives.

**Follow-ups:** How would you build a labelled code-mixed evaluation set cheaply? Would you normalize output to native script or keep transliteration, and why?

</details>

### 5. Sarvam-M ships a hybrid "think" and "non-think" mode and was post-trained with SFT then RLVR. Explain how you would build that, and why RLVR over vanilla RLHF.

<details><summary><b>Answer</b></summary>

Hybrid thinking means one model that can either produce a fast direct answer (non-think, for conversation) or a longer chain-of-thought before answering (think, for math, code, reasoning), toggled by a control token or system instruction. You build it in post-training, not architecture.

**SFT stage:** curate prompts spanning difficulty and domains, generate completions (from permissible strong models), filter by a custom scoring/quality bar, and crucially include **both** styles: reasoning traces wrapped so the model learns to emit them under the think toggle, and crisp direct answers under the non-think toggle. You also fold in Indic-language data and cultural adjustment here so the behaviours exist in Hindi, Tamil, and so on, not just English. The model learns the mode conditioning from the format of these examples.

**RLVR stage:** Reinforcement Learning with Verifiable Rewards. Instead of training a learned preference reward model (classic RLHF), you use domains where correctness is **programmatically checkable**: math answers graded against ground truth, code run against unit tests, instruction-following checked by rules. The reward is the verifier's verdict. Why prefer it here: (1) verifiable rewards are less hackable and less noisy than a learned reward model, which drifts and gets gamed; (2) they directly target the capabilities Sarvam reports gains on (Sarvam-M reports roughly +21.6% on math and +17.6% on programming benchmarks over the base, plus about +20% on Indian-language benchmarks); (3) you avoid the cost and bias of collecting huge human-preference datasets, which is especially painful across many low-resource languages. You still use curriculum (instruction following, then harder math/code), reward shaping, and prompt sampling to keep training stable. The limitation is that RLVR only covers verifiable domains, so subjective quality, tone, and safety still need preference data or rules.

**Follow-ups:** How do you stop the think mode from bloating latency and cost on simple queries? How would you design a verifier for an Indic-language instruction-following task where there is no single correct string?

</details>

### 6. A regional government wants an assistant in a low-resource language with only a few thousand sentences of clean text. How do you adapt a model to it?

<details><summary><b>Answer</b></summary>

A few thousand sentences is far too little for pretraining and thin even for fine-tuning, so the plan is data amplification plus targeted adaptation, not a from-scratch model. Ordered by leverage:

(1) **Start from a base that already covers a linguistically related language.** If the target shares script (Devanagari) or family with, say, Hindi or Marathi, transfer is far cheaper. Sarvam-1's Indic coverage and tokenizer make it a better starting point than an English-centric base.

(2) **Fix the tokenizer if the script is poorly covered.** Measure fertility on the target; if it is high, extend the vocabulary with target-language tokens and initialize new embeddings from subword averages, then let continued pretraining settle them. Skip this if fertility is already acceptable, since vocab surgery has its own risks.

(3) **Amplify data.** Use translation (Mayura-style) and transliteration to bootstrap from high-resource languages, generate synthetic instruction data, and mine parallel/monolingual web and speech transcripts. Sarvam publicly leans on synthetic data generation for exactly this. Keep a small human-verified gold set uncontaminated for evaluation.

(4) **Adapt cheaply.** Continued pretraining on the amplified monolingual corpus to teach the language, then LoRA or light SFT on instruction data for the task. LoRA limits catastrophic forgetting of other languages and is swappable per deployment.

(5) **Ground with RAG** for facts (schemes, forms, eligibility) so you are not relying on the small model to memorise government specifics, and you can update them without retraining.

(6) **Evaluate honestly**: build a human-checked test set in the target language; do not trust benchmark scores on machine-translated evals, which reward the translator's artefacts. Watch for the model reverting to the related language under pressure.

**Follow-ups:** How do you detect and prevent synthetic-data quality collapse? When would you decide the language is too low-resource to serve responsibly and route to human agents instead?

</details>

### 7. Write code to measure a tokenizer's fertility across languages, and explain what you would do with the result.

<details><summary><b>Answer</b></summary>

Fertility is mean tokens per word. The measurement must be per language on comparable content, and word counting has to respect scripts that do not delimit with spaces the same way.

```python
from collections import defaultdict

def fertility(tokenizer, corpus_by_lang):
    # corpus_by_lang: {"hi": [sentence, ...], "en": [...], ...}
    results = {}
    for lang, sentences in corpus_by_lang.items():
        n_words = n_tokens = 0
        for s in sentences:
            words = s.split()                       # crude; see caveats
            n_words += len(words)
            n_tokens += len(tokenizer.encode(s, add_special_tokens=False))
        results[lang] = n_tokens / max(n_words, 1)
    return results

# Interpreting: fertility ~1.1 (English) vs ~5 (an unseen Indic script)
# means that language costs ~5x the tokens per word -> cost, latency,
# and effective-context penalty all scale with that ratio.
```

Caveats I would raise unprompted: `str.split()` is a poor word boundary for many Indian languages and for scripts without spaces, so use a language-aware segmenter or at least a consistent Unicode-aware rule, and compare on **parallel** content (the same sentences translated) so you are measuring the tokenizer, not differences in what each corpus talks about. Also report token-per-character or token-per-byte alongside fertility, since word definitions vary.

What I do with it: rank languages by fertility to find where the tokenizer is starving. High fertility on a target language flags either retraining the tokenizer on a balanced corpus or extending the vocabulary with that language's frequent morphemes. It also feeds cost and context-budget planning: if Kannada runs 3x English fertility, your RAG chunker, few-shot budget, and pricing all need adjusting for Kannada users. This is exactly the analysis behind Sarvam-1's low-fertility design.

**Follow-ups:** Why can two tokenizers with the same vocab size have very different fertility on Tamil? How would parallel-corpus fertility differ from fertility measured on independent monolingual corpora?

</details>

### 8. Design cross-lingual RAG: the knowledge base is in English and Hindi, but users ask in Tamil, Telugu, or transliterated Hinglish. How do you retrieve and answer correctly?

<details><summary><b>Answer</b></summary>

The core problem is that the query language, the document language, and the script can all differ, so lexical matching and naive embeddings fail. Design around a shared multilingual semantic space plus deliberate normalization.

**Retrieval:** use a **multilingual embedding model** so a Tamil query and an English passage about the same thing land near each other in vector space; this is the load-bearing choice. Handle transliteration up front: "sarkari yojana" typed in Latin must map to the same concept as the Devanagari form, so add a transliteration/normalization step (native-script conversion or transliteration-robust embeddings) before embedding. Consider **hybrid retrieval**: dense vectors for cross-lingual semantics plus BM25 on a normalized field to catch exact entity and scheme names, which embeddings often blur. A cross-encoder reranker (also multilingual) sharpens the top-k.

**Generation:** retrieve in whatever language the answer lives, but instruct the model to **answer in the user's language**. Two options for the context: pass source-language passages and let a strong multilingual model reason across languages (fewer moving parts, risk of the model leaking the source language), or translate retrieved passages into the user's language first (cleaner output, adds latency and translation error). I would start with the former using a Sarvam-class multilingual model and measure.

**Evaluation and safety:** build a cross-lingual eval set (query in language A, gold answer grounded in language-B docs) and measure retrieval hit rate and answer faithfulness per language, because quality is very uneven across languages. Watch two failure modes: the model answering in the wrong script, and citations that do not actually support a translated claim. For government content, keep citations and enforce grounding so mistranslation cannot silently change a fact.

**Follow-ups:** How do you keep entity names (scheme names, place names) from being mangled across scripts? Where does chunking need to change when documents mix English and Hindi in the same page?

</details>

### 9. Bulbul-style TTS has to speak code-mixed, mixed-script text naturally. What are the hard parts of text normalization and prosody for Indian-language TTS?

<details><summary><b>Answer</b></summary>

TTS quality for Indian languages is decided as much in the **text front-end** as in the acoustic model. The hard parts:

(1) **Text normalization is language- and context-dependent.** Numbers, dates, currency, and abbreviations expand differently per language ("100" spoken in Hindi versus Tamil), and the same digits can be an amount, a year, or a phone number. Getting "Rs 2,500" or "12/03" right needs a normalizer that knows the language and the semantic type.

(2) **Mixed script and code-mixing.** Real text is "aapka OTP 4 5 6 hai" - Devanagari plus Latin plus digits in one line. The model must pronounce English words with an appropriate accent, read digits in the surrounding language, and not stumble at script boundaries. Transliteration decisions (do you speak an English word as English or Indianised) are product choices baked into training data.

(3) **Grapheme-to-phoneme and inherent vowels.** Indic (Abugida) scripts carry inherent vowels and use conjuncts and diacritics; schwa deletion in Hindi ("kamal" not "kamala") is a classic G2P trap that sounds obviously wrong if mishandled.

(4) **Prosody: emphasis, pauses, intonation.** Bulbul V3 is described as using an LLM front-end to infer prosodic structure from context and intent rather than treating text as a flat sequence, which is how you get natural pacing, questions that rise, and correct emphasis. Prosody patterns differ across Indian languages, so this is not one-size-fits-all.

(5) **Voice quality and coverage.** Expressive, professional-sounding voices across 11+ languages, plus voice cloning, means large, clean, well-labelled speech data per language and speaker - the data problem again.

Evaluation is subjective (MOS-style listening tests) plus targeted checks on numbers, code-mixed lines, and known G2P traps, because aggregate naturalness scores hide the specific errors users notice.

**Follow-ups:** How would you handle a sentence that switches script mid-word? Why is an LLM-based front-end better than rule-based prosody for expressive TTS, and what does it cost you?

</details>

### 10. How do you deploy a capable assistant on cost-sensitive or on-device hardware (think Sarvam-Edge) without a datacentre GPU? Walk through the efficiency toolkit.

<details><summary><b>Answer</b></summary>

The constraint drives everything: limited memory and compute, often no reliable network (so cloud fallback is not guaranteed), and cost per query that has to be tiny at population scale. The toolkit, roughly in order:

(1) **Right-size the model.** A well-trained small model beats a throttled large one on-device. Sarvam-1 is deliberately 2B; the Edge tier goes smaller. Match the model to the task rather than shipping a generalist you cannot afford. Distillation from a larger Sarvam model into a small student is the standard move.

(2) **Quantization is the biggest lever.** Weight-only int4 (AWQ/GPTQ-family) roughly quarters weight memory and speeds memory-bandwidth-bound decode, which is what dominates on weak hardware. Below 4-bit degrades unevenly, so validate. On-device you often go int8 or int4 with per-channel scales and check quality on the actual languages, because quantization damage can hit non-English disproportionately.

(3) **Tokenizer efficiency compounds here.** With low Indic fertility (the Sarvam-1 point), you generate fewer tokens per response, which directly cuts on-device latency and energy. Efficiency starts before the weights.

(4) **KV-cache thrift.** GQA (Sarvam-1 uses 16 query heads over 8 KV heads) shrinks the cache; cap context, and quantize the KV cache if memory is tight, since at longer contexts the cache, not the weights, is the constraint.

(5) **Runtime and format.** Use an edge runtime (llama.cpp / GGUF, ONNX, or a mobile NN runtime), exploit any NPU/accelerator, and precompute/cache common responses. Batch is usually 1 on-device, so per-request latency, not throughput, is the metric.

(6) **Hybrid routing** where a network exists: handle common intents locally, escalate hard queries to a bigger cloud model, and degrade gracefully offline.

The overall philosophy is quality per rupee and per watt, which is exactly the sovereign, population-scale brief.

**Follow-ups:** Why does weight-only int4 help decode but barely help prefill? How would you decide, per query, whether to answer on-device or escalate to the cloud?

</details>

### 11. How would you evaluate an Indic LLM properly? Why is running translated English benchmarks not enough?

<details><summary><b>Answer</b></summary>

Translated English benchmarks are a trap for several reasons, and naming them is half the answer. (1) **Translation artefacts leak into the score**: a translated MMLU measures partly how the model handles translationese, not native comprehension, and the machine translation itself introduces errors and unnatural phrasing. (2) **Cultural and factual grounding is missing**: questions about Indian law, history, civics, geography, and everyday context are simply absent from Western benchmarks, yet they are what the product is for. (3) **Script and transliteration issues**: exact-match metrics punish a correct answer written in the wrong script or a valid transliteration, and tokenization differences distort perplexity comparisons across languages. (4) **Uneven per-language quality**: an aggregate number hides that the model is great in Hindi and broken in Odia.

What I would build: (1) **native, human-authored evaluation sets per language** covering the target tasks, plus India-centric knowledge (community efforts and graduate-level Indic subject benchmarks exist for this). (2) **Task-appropriate metrics**: for generation, use human or LLM-judge grading with a rubric rather than brittle exact match; normalize script before any string comparison; report per-language, never just the mean. (3) **Code-mixed and real-usage tests**, since users type Hinglish and speak code-mixed. (4) For voice products, **end-to-end evals**: WER on code-mixed ASR, MOS for TTS, and task-success for the full agent, not just the LLM in isolation. (5) A small, **uncontaminated gold set** guarded from training data so scores stay honest.

The mindset Sarvam rewards: your eval set is a first-class artefact, built for the languages and users you actually serve, and you distrust any single aggregate number.

**Follow-ups:** How would you use an LLM-as-judge for Hindi without importing the judge's English bias? How do you guard an eval set against contamination when you also generate synthetic training data?

</details>

### 12. Forward-deployed scenario: a state agency wants to move a paper-and-call-centre welfare-scheme service onto a multilingual assistant, on-prem for data residency. How do you scope and ship it?

<details><summary><b>Answer</b></summary>

Treat it as a real forward-deployed engagement: understand the workflow before touching a model. Scope first: which schemes, which languages and dialects, what channels (phone/IVR, WhatsApp, web, kiosk), literacy and device reality (many users are voice-first, low-bandwidth, feature phones), and the hard compliance constraints (data residency, so on-prem or sovereign cloud; audit logging; PII handling; accessibility).

Architecture: (1) **Voice-first pipeline** for the call-centre channel - Saaras ASR, a Sarvam LLM, Bulbul TTS - streaming for low latency (see the voice-agent question), with human-agent fallback for complex or high-stakes cases. (2) **RAG over the scheme documents** so eligibility rules, forms, and deadlines are grounded and citable, and updatable without retraining, which matters because policy changes. (3) **Deterministic guardrails on high-stakes intents**: eligibility and entitlement answers must be grounded and, where consequential, routed to a human or a rules engine, never free-form generated. (4) **On-prem serving**: models and vector store inside the agency's network, an inference layer (continuous batching, paged KV cache), a gateway for authn/z, full request/response audit to their systems, and PII redaction. Size models to their actual GPUs and quantize as needed.

Delivery discipline: build a **gold eval set from real citizen queries per language**, measure retrieval hit rate, answer faithfulness, and task success before launch; pilot on a few schemes and one or two languages, then expand; instrument latency, containment (resolved without a human), and error escalation. Plan for the unglamorous parts: telephony quirks, code-mixed input, updating scheme data, and a clear escalation and correction loop. Success is measured in citizens served correctly per rupee, not demo polish.

**Follow-ups:** How do you prevent the assistant from confidently stating an eligibility conclusion it should not? What is your rollout and monitoring plan for adding the fifth and sixth languages?

</details>

## How to prepare

Priority order for this repo's topics:

1. **[02-llm-fundamentals](../02-llm-fundamentals/)** - tokenization and fertility are the single most Sarvam-specific topic; also GQA, RoPE, MoE (Sarvam-30B/105B), and hybrid reasoning. Be able to reason about tokenizer design and multilingual tradeoffs, not just recite transformer blocks.
2. **[10-multimodal](../10-multimodal/)** - speech is core: ASR, TTS, VAD/endpointing, streaming, and code-mixed audio. If you are on an applied or agents track, this and voice pipelines are where you differentiate.
3. **[08-inference-and-production](../08-inference-and-production/)** - quantization, KV-cache math, small-model and on-device efficiency (Sarvam-Edge), and low-latency streaming serving. Efficiency is a company value here.
4. **[05-fine-tuning-and-alignment](../05-fine-tuning-and-alignment/)** - SFT, RLVR vs RLHF, LoRA/QLoRA, continued pretraining, and low-resource/synthetic-data adaptation (the Sarvam-M post-training story and Indic language extension).
5. **[04-rag-and-retrieval](../04-rag-and-retrieval/)** - cross-lingual and multilingual RAG, hybrid retrieval, and grounding for citizen/enterprise assistants.
6. **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - the Sarvam Agents track: tool wiring, agent harness, and reliability in production.
7. **[11-ai-system-design](../11-ai-system-design/)** - practise end-to-end designs. Closest existing case study: **[customer support agent](../11-ai-system-design/case-studies/03-customer-support-agent.md)** - Sarvam's forward-deployed voice-agent and citizen-helpline work is exactly this shape, plus multilingual and on-prem constraints.

Company-specific moves:

- **Read the Sarvam-1 and Sarvam-M writeups** and understand the specifics: the 1.4-2.1 fertility claim, GQA + SwiGLU + RoPE at 2B, and the SFT-then-RLVR hybrid-reasoning recipe. Being able to talk about why each choice was made covers a lot of the technical bar.
- **Build a small voice agent** with their APIs (Saaras + an LLM + Bulbul) or an open equivalent. Get first-hand feel for streaming latency, endpointing, and barge-in, because a reported build round is literally a VAD from scratch.
- **Do the tokenizer exercise for real**: measure fertility of a mainstream tokenizer versus an Indic-aware one on parallel Hindi/Tamil/English text. This turns the headline claim into something you can discuss from experience.
- **Practise the proof-of-work format**: a time-boxed build where AI tools are allowed. Rehearse fast setup, reading unfamiliar library docs, and debugging under a clock, since that is what they grade.
- **Have a crisp view on sovereign AI and Indic language technology**: why it matters, the low-resource data problem, and how you would evaluate quality honestly across languages. "Why Sarvam / why Indic AI" is a real question.

## Sources

- [Sarvam AI careers page](https://www.sarvam.ai/careers) - role titles and archetypes (Applied AI Engineer / Sarvam Agents, Full Stack AI Engineer, Forward Deployed Software Engineer, AI Engineer Intern, Backend Engineer)
- [Sarvam-1 on Hugging Face](https://huggingface.co/sarvamai/sarvam-1) - architecture, parameters, GQA config, training tokens, and languages
- [Sarvam-1 announcement (IndiaAI)](https://indiaai.gov.in/article/sarvam-ai-unveils-sarvam-1-optimized-language-model-for-indian-languages) - tokenizer fertility (1.4-2.1), efficiency and inference-speed claims, training setup
- [Sarvam-M on Hugging Face](https://huggingface.co/sarvamai/sarvam-m) and [Sarvam-M coverage (Entrepreneur India)](https://www.entrepreneur.com/en-in/news-and-trends/sarvam-ai-launches-24b-parameter-open-source-llm-for-indian/492204) - 24B, built on Mistral Small, SFT + RLVR, hybrid think/non-think, benchmark deltas
- [Sarvam models overview (docs.sarvam.ai)](https://docs.sarvam.ai/api-reference-docs/getting-started/models) - Saaras (ASR), Bulbul (TTS), Mayura, model lineup
- [Sarvam to build India's sovereign LLM (Sarvam blog)](https://www.sarvam.ai/blogs/indias-sovereign-llm) - IndiaAI Mission selection, compute allocation, model variants, AI4Bharat collaboration
- [Sarvam AI (Wikipedia)](https://en.wikipedia.org/wiki/Sarvam_AI) - founding, founders, funding/investors, model timeline, valuation
- [Grapevine: Sarvam Backend AI Engineer interview](https://www.grapevine.in/round1/job-interview/e87b2eb9-8bcf-4122-8122-2afaa2500801) - candidate-reported stage breakdown (assignment, technical rounds, DSA, HR)
- [GetPersonalisedCV: Sarvam AI interview experience](https://getpersonalisedcv.in/blog/sarvam-ai-interview-experience-84-lpa-ml-engineer) - candidate report of the ~2.5 hr proctored build session (VAD from scratch), tools-allowed, no-DSA proof-of-work format
- [Glassdoor: SarvM.ai interviews](https://www.glassdoor.com/Interview/SarvM-ai-Interview-Questions-E7826863.htm) - aggregated candidate reports (unofficial; process varies)

*Interview-process detail is drawn from a small number of public candidate reports and is not officially published, so treat the loop as indicative rather than fixed.*
