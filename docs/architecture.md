# Architecture Overview

## System Flow

```text
Client
   |
POST /videos
   |
FastAPI API Layer
   |
SQLite Persistence
   |
Background Task
   |
Video Download
   |
+-----------------------------+
| Media Processing Pipeline   |
+-----------------------------+
| Audio Extraction            |
| Frame Extraction            |
| Whisper Tiny                |
| Text Analyzer               |
| Metadata Analyzer           |
+-----------------------------+
   |
Risk Scoring
   |
Report Generation
   |
Persistence
   |
GET Status / Report / Ask
```

## Components

### API Layer

Responsible for request validation and response handling.

### Persistence Layer

Stores:

* Videos
* Findings
* Processing State

### Processing Layer

Handles long-running video analysis asynchronously.

### Analyzer Layer

Each analyzer is isolated and independently replaceable.

Current analyzers:

* Transcript Analyzer
* Metadata Analyzer
* Visual Analyzer

### Reporting Layer

Aggregates findings and generates final risk reports.
