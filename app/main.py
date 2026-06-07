import uuid
import os

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from app.services.processor import process_video
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import Video, Finding
from app.schemas import (
    VideoAskRequest,
    VideoAskResponse,
    VideoArtifactsResponse,
    VideoCreateRequest,
    VideoCreateResponse,
    VideoStatusResponse,
    VideoReportResponse,
    FindingResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Problematic Video Segment Detection",
    version="1.0.0"
)


@app.get("/")
def health():
    return {
        "status": "healthy",
        "service": "video-risk-detection"
    }


@app.post("/videos", response_model=VideoCreateResponse)
def submit_video(
    request: VideoCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    video_id = str(uuid.uuid4())

    video = Video(
        id=video_id,
        url=str(request.video_url),
        status="queued",
        overall_risk="unknown"
    )

    db.add(video)
    db.commit()

    background_tasks.add_task(process_video, video_id)

    return VideoCreateResponse(
        video_id=video_id,
        status="queued"
    )


@app.get("/videos/{video_id}/status", response_model=VideoStatusResponse)
def get_video_status(
    video_id: str,
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return VideoStatusResponse(
        video_id=video.id,
        status=video.status,
        overall_risk=video.overall_risk,
        error_message=video.error_message
    )


@app.get("/videos/{video_id}/report", response_model=VideoReportResponse)
def get_video_report(
    video_id: str,
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    findings = db.query(Finding).filter(Finding.video_id == video_id).all()

    return VideoReportResponse(
        video_id=video.id,
        status=video.status,
        overall_risk=video.overall_risk,
        findings=[
            FindingResponse(
                start_time=f.start_time,
                end_time=f.end_time,
                category=f.category,
                severity=f.severity,
                confidence=f.confidence,
                evidence=f.evidence,
                source=f.source
            )
            for f in findings
        ]
    )

@app.get("/videos/{video_id}/artifacts", response_model=VideoArtifactsResponse)
def get_video_artifacts(
    video_id: str,
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    artifact_dir = os.path.join("data", "artifacts", video_id)

    artifacts = {
        "artifact_dir": artifact_dir,
        "frame_extraction": "ffmpeg frame extraction",
        "audio_extraction": "ffmpeg audio extraction",
        "transcription": "OpenAI Whisper Tiny",
        "notes": "Artifacts are persisted under data/artifacts/{video_id}"
    }

    return VideoArtifactsResponse(
        video_id=video_id,
        artifacts=artifacts
    )

@app.post("/videos/{video_id}/ask", response_model=VideoAskResponse)
def ask_video_question(
    video_id: str,
    request: VideoAskRequest,
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    findings = db.query(Finding).filter(Finding.video_id == video_id).all()

    if not findings:
        answer = (
            f"No problematic findings are currently available for this video. "
            f"The processing status is '{video.status}' and the overall risk is '{video.overall_risk}'."
        )
    else:
        finding_summary = "; ".join(
            [
                f"{f.category} from {f.start_time:.1f}s to {f.end_time:.1f}s "
                f"with {f.severity} severity based on {f.source}: {f.evidence}"
                for f in findings
            ]
        )

        answer = (
            f"The video is marked as {video.overall_risk} risk. "
            f"The main findings are: {finding_summary}"
        )

    return VideoAskResponse(
        video_id=video_id,
        question=request.question,
        answer=answer
    )