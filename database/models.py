from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)
from datetime import datetime

from database.db import Base


class Report(Base):
    __tablename__ = "reports"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Image
    image_path = Column(String, nullable=False)

    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)

    # AI Prediction
    incident_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    Summary = Column(String, nullable=True)

    embedding = Column(Text, nullable=True)

    # User Input
    description = Column(Text, nullable=True)

    # Complaint Status
    status = Column(String, default="Pending")

    # Assigned Department
    department = Column(String, nullable=True)

    # Duplicate Reports
    duplicate_count = Column(Integer, default=1)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )