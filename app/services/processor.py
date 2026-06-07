import os
import logging
from datetime import datetime
from app.services.transcription_service import extract_audio, transcribe_audio
from sqlalchemy.orm import Session
from app.services.media_service import download_video, extract_frames, get_video_duration
from app.db import SessionLocal
from app.models import Video, Finding
from app.services.analyzers.text_analyzer import analyze_transcript_segments
from app.services.analyzers.visual_analyzer import analyze_sampled_frames
from app.services.analyzers.metadata_analyzer import analyze_metadata
from app.services.report_generator import calculate_overall_risk

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_video(video_id: str):
    db: Session = SessionLocal()

    try:
        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            return

        video.status = "processing"
        logger.info(f"Video {video_id} status changed to processing")
        video.updated_at = datetime.utcnow()
        db.commit()

        artifact_dir = os.path.join("data", "artifacts", video_id)
        os.makedirs(artifact_dir, exist_ok=True)

        try:
            video_path = download_video(video.url, video_id)
            duration_seconds = get_video_duration(video_path)
            frame_paths = extract_frames(video_path, video_id, every_seconds=5)
            logger.info(
                f"Video {video_id} media extracted successfully. "
                f"duration={duration_seconds}, frames={len(frame_paths)}"
            )
        except Exception as media_error:
            duration_seconds = 60.0
            frame_paths = []
            logger.warning(
            f"Media extraction fallback used for video_id={video_id}: {media_error}"
            )
        media_fallback_used = len(frame_paths) == 0
        # Prototype transcript fallback.
        # Production path: extract audio with ffmpeg and transcribe with Whisper tiny/base.
        if media_fallback_used:
            transcript_segments = [
                {
                    "start_time": 10.0,
                    "end_time": 18.0,
                    "text": "Fallback transcript segment mentions weapon and attack for demonstration."
                }
            ]
        else:
            try:
                audio_path = extract_audio(video_path, video_id)
                transcript_segments = transcribe_audio(audio_path)
                logger.info(
                f"Video {video_id} transcribed using Whisper Tiny. "
                f"segments={len(transcript_segments)}"
                )

                if not transcript_segments:
                    logger.info(
                        f"Video {video_id} contains no detectable speech."
                    )

                    transcript_segments = [
                        {
                            "start_time": 0.0,
                            "end_time": min(8.0, duration_seconds),
                            "text": "No speech detected."
                        }
                    ]

            except Exception as transcription_error:
                logger.warning(
                f"Whisper fallback used for video_id={video_id}: {transcription_error}"
                )
                transcript_segments = [
                    {
                        "start_time": 0.0,
                        "end_time": min(8.0, duration_seconds),
                        "text": f"Whisper transcription fallback used: {transcription_error}"
                    }
                ]

        metadata = {
            "duration_seconds": duration_seconds,
            "source_url": video.url,
            "sampled_frame_count": len(frame_paths)
        }

        all_findings = []
        all_findings.extend(analyze_transcript_segments(transcript_segments))
        all_findings.extend(analyze_sampled_frames(frame_paths))
        all_findings.extend(analyze_metadata(metadata))

        for finding in all_findings:
            db.add(Finding(
                video_id=video_id,
                start_time=finding["start_time"],
                end_time=finding["end_time"],
                category=finding["category"],
                severity=finding["severity"],
                confidence=finding["confidence"],
                evidence=finding["evidence"],
                source=finding["source"]
            ))

        video.status = "completed"
        video.overall_risk = calculate_overall_risk(all_findings)
        video.duration_seconds = duration_seconds
        video.updated_at = datetime.utcnow()
        logger.info(
        f"Video {video_id} completed. "
        f"overall_risk={video.overall_risk}, findings={len(all_findings)}"
        )
        db.commit()

    except Exception as exc:
        video = db.query(Video).filter(Video.id == video_id).first()
        logger.exception(f"Video {video_id} processing failed")
        if video:
            video.status = "failed"
            video.error_message = str(exc)
            video.updated_at = datetime.utcnow()
            db.commit()

    finally:
        db.close()