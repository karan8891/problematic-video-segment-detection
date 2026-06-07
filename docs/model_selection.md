# Model Selection and Tooling Notes

## Whisper Tiny

### Purpose

Speech-to-text transcription.

### Why Selected

* Small footprint
* Fast inference
* Runs locally
* No external API cost

### Inputs

Audio extracted from video.

### Outputs

Timestamped transcript segments.

### Tradeoffs

Advantages:

* Low latency
* Open source
* Offline capable

Limitations:

* Lower accuracy than larger Whisper models
* Sensitive to noisy audio

---

## Text Risk Analyzer

### Purpose

Detect potentially problematic language.

### Method

Keyword and category matching over transcript segments.

### Categories

* Violence
* Hate Speech
* Sexual Content
* Self Harm
* Drug Related

### Future Upgrade

Replace with:

* DistilRoBERTa
* DeBERTa
* Moderation transformer models

---

## Visual Analyzer

Current implementation is a lightweight prototype.

Future production upgrades:

* CLIP
* NSFW Classifier
* Violence Detection Models

---

## ffmpeg

Used for:

* Audio extraction
* Frame extraction

Chosen because:

* Open source
* Industry standard
* Efficient media processing

---

## Performance Notes

Current prototype:

* API response is immediate.
* Processing runs asynchronously.
* Runtime scales approximately with video duration.

Future optimizations:

* Scene detection
* Frame sampling
* GPU inference
* Batch processing
* Horizontal worker scaling
