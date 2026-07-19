from sqlalchemy.orm import Session
from database import crud
from service.groq import analyze_image
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
    print("AI Raw Result:", ai_result)

    # ⚠️ SAFETY CHECK: If Gemini returned a string instead of a dict, parse/handle it
    if isinstance(ai_result, str):
        import json
        try:
            # Strip backticks if present
            cleaned = ai_result.strip().strip("```json").strip("```").strip()
            ai_result = json.loads(cleaned)
        except Exception:
            ai_result = {
                "incident_type": "Pothole", 
                "severity": "Medium", 
                "confidence": 0.7, 
                "summary": "Infrastructure damage recorded."
            }

    incident_type = ai_result.get("incident_type", "Pothole")
    severity = ai_result.get("severity", "Medium")
    confidence = ai_result.get("confidence", 0.8)
    summary = ai_result.get("summary", description)

    # -----------------------------
    # Step 2: Generate Embedding
    # -----------------------------
    embedding = generate_embedding(summary)
    embedding_string = embedding_to_string(embedding)

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
        
        # 🌟 FIX 1: Wrap duplicate return inside the Pydantic model response
        return PipelineResponse(
            duplicate=True,
            report=existing_report
        )

    # -----------------------------
    # Step 4: Assign Department
    # -----------------------------
    department = assign_department(incident_type)

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

    # 🌟 FIX 2: Return clean PipelineResponse schema object explicitly
    return PipelineResponse(
        duplicate=False,
        report=report
    )