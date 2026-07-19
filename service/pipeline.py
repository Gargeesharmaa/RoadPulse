from sqlalchemy.orm import Session

from database import crud

from service.gemini import analyze_image
from service.embedding import (
    generate_embedding,
    embedding_to_string
)
from service.duplicate import find_duplicate
from service.routing import assign_department
from schemas.report import PipelineResponse


def process_report(
    db: Session,
    image_path: str,
    latitude: float,
    longitude: float,
    address: str,
    description: str
):
    """
    Complete AI pipeline for a new road report.
    """

    # -----------------------------
    # Step 1: Analyze Image
    # -----------------------------
    ai_result = analyze_image(image_path)

    incident_type = ai_result["incident_type"]
    severity = ai_result["severity"]
    confidence = ai_result["confidence"]
    summary = ai_result["summary"]

    # -----------------------------
    # Step 2: Generate Embedding
    # -----------------------------
    embedding = generate_embedding(summary)

    embedding_string = embedding_to_string(
        embedding
    )

    # -----------------------------
    # Step 3: Check Duplicate
    # -----------------------------
    reports = crud.get_all_reports(db)

    is_duplicate, existing_report = find_duplicate(
        summary=summary,
        latitude=latitude,
        longitude=longitude,
        incident_type=incident_type,
        existing_reports=reports
    )

    if is_duplicate:

        crud.update_duplicate_count(
            db,
            existing_report.id
        )

        return {
            "duplicate": True,
            "report": existing_report
        }

    # -----------------------------
    # Step 4: Assign Department
    # -----------------------------
    department = assign_department(
        incident_type
    )

    # -----------------------------
    # Step 5: Create Report
    # -----------------------------
    report_data = {

        "image_path": image_path,

        "latitude": latitude,
        "longitude": longitude,

        "address": address,

        "description": description,

        "incident_type": incident_type,
        "severity": severity,
        "confidence": confidence,

        "summary": summary,
        "embedding": embedding_string,

        "department": department,

        "status": "Pending",

        "duplicate_count": 1
    }

    report = crud.create_report(
        db,
        report_data
    )

    return PipelineResponse(
        duplicate=False,
        report= report
    )