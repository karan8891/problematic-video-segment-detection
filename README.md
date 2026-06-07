# Problematic Video Segment Detection

## Documentation

Detailed documentation is available in the `docs/` directory:

- [Architecture Overview](docs/architecture.md)  
  Explains the API layer, persistence layer, asynchronous processing flow, analyzer pipeline, and report generation design.

- [Model Selection and Tooling Notes](docs/model_selection.md)  
  Explains why Whisper Tiny, ffmpeg, transcript analysis, and the prototype visual analyzer were selected, including latency, memory, cost, and upgrade tradeoffs.

- [Operational Notes](docs/operational_notes.md)  
  Covers logging, failure handling, artifact storage, monitoring opportunities, scalability path, and security considerations.

- [Screenshots and Evidence](screenshots/)  
  Contains Swagger API execution evidence, pytest results, and terminal logs showing ffmpeg media extraction and Whisper Tiny processing.

Dockerfile and docker-compose.yml are included. Docker build was attempted on the development laptop, but the local Docker build failed while installing the Whisper dependency. The application was fully validated locally with Python, FFmpeg, Whisper Tiny, Swagger, and pytest.

## Overview

This project implements an asynchronous backend system that analyzes videos and identifies potentially problematic content. Instead of returning a simple pass/fail result, the system generates a structured report containing timestamped findings, severity levels, evidence, and supporting artifacts.

The solution was designed with a modular architecture that allows analyzers to be swapped or upgraded independently.

---

## Features

### Video Submission

Submit a video URL for processing.

```http
POST /videos
```

Response:

```json
{
  "video_id": "123",
  "status": "queued"
}
```

---

### Processing Status

Check processing progress.

```http
GET /videos/{video_id}/status
```

Response:

```json
{
  "video_id": "123",
  "status": "completed",
  "overall_risk": "high"
}
```

---

### Findings Report

Retrieve timestamped findings.

```http
GET /videos/{video_id}/report
```

---

### Processing Artifacts

Retrieve generated artifacts and metadata.

```http
GET /videos/{video_id}/artifacts
```

---

### Ask Questions About a Video

Ask questions regarding analysis results.

```http
POST /videos/{video_id}/ask
```

Example:

```json
{
  "question": "Why is this video high risk?"
}
```

---

## Architecture

FastAPI receives requests and persists video metadata.

Background processing is executed asynchronously using FastAPI BackgroundTasks.

The processing pipeline performs:

1. Video download
2. Frame extraction
3. Audio extraction
4. Whisper Tiny transcription
5. Text analysis
6. Risk scoring
7. Report generation
8. Artifact persistence

---

## Technology Stack

* Python
* FastAPI
* SQLite
* SQLAlchemy
* OpenAI Whisper Tiny
* OpenCV
* ffmpeg
* Docker

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

```bash
pytest
```

---

## Docker

```bash
docker compose up --build
```

---

## Current Limitations

* Visual analysis currently uses a lightweight prototype analyzer.
* OCR analysis is not implemented.
* Frame classification can be upgraded with CLIP or NSFW classifiers.
* SQLite is used for simplicity and can be replaced by PostgreSQL.
* FastAPI BackgroundTasks can be replaced by Celery + Redis for production workloads.

---

## Future Improvements

* CLIP-based visual classification
* OCR pipeline
* NSFW image detection
* Distributed workers
* Vector search for video question answering
* Multi-language moderation

---
