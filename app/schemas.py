from typing import List, Optional
from pydantic import BaseModel, HttpUrl

from typing import Dict, Any

class VideoAskRequest(BaseModel):
    question: str

class VideoAskResponse(BaseModel):
    video_id: str
    question: str
    answer: str

class VideoArtifactsResponse(BaseModel):
    video_id: str
    artifacts: Dict[str, Any]

class VideoCreateRequest(BaseModel):
    video_url: HttpUrl


class VideoCreateResponse(BaseModel):
    video_id: str
    status: str


class VideoStatusResponse(BaseModel):
    video_id: str
    status: str
    overall_risk: str
    error_message: Optional[str] = None


class FindingResponse(BaseModel):
    start_time: float
    end_time: float
    category: str
    severity: str
    confidence: float
    evidence: str
    source: str


class VideoReportResponse(BaseModel):
    video_id: str
    status: str
    overall_risk: str
    findings: List[FindingResponse]