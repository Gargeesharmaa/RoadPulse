from pydantic import BaseModel
from typing import  Optional
from datetime import datetime

#create report schema

class ReportCreate(BaseModel):
    image_path: str
    latitude: float
    longitude: float
    address: Optional[str] = None

    incident_type: str
    severity: str
    confidence: float

    description: Optional[str] = None

# Update Report Status
class ReportUpdate(BaseModel):
    status: str

class DepartmentUpdate(BaseModel):
    department: str


class AIPredictionUpdate(BaseModel):
    incident_type : str
    severity: str
    confidence: float
    summary: str
    embedding: str


class ReportResponse(BaseModel):
    id: int
    image_path: str
    latitude: float
    longitude: float
    address: Optional[str]

    incident_type: str
    severity: str
    confidence: float
    summary: str| None =None
    embedding: str| None= None

    status: str
    description: Optional[str] = None

    duplicate_count: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attribute =True

class PipelineResponse(BaseModel):
    duplicate: bool
    report: ReportResponse
