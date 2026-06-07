from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from app.db import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    status = Column(String, default="queued", index=True)
    overall_risk = Column(String, default="unknown")
    error_message = Column(Text, nullable=True)

    duration_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_id = Column(String, index=True, nullable=False)

    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)

    evidence = Column(Text, nullable=False)
    source = Column(String, nullable=False)