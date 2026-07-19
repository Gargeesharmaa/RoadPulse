from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from typing import List

from database.db import get_db
from database import crud
from schemas.report import (ReportCreate, ReportResponse, DepartmentUpdate, AIPredictionUpdate, ReportUpdate)
from service.groq import analyze_image
from fastapi import UploadFile, File, Form
import os
import uuid
import shutil
from database.db import get_db
from service.pipeline import process_report

router = APIRouter(
    prefix="/reports",
    tags=['RoadPulse Report']
)


# create a report
@router.post("/")
async def create_new_report(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # 🌟 CRITICAL FIX 1: Ensure safe file extension extraction
    # Fallback to 'jpeg' if the uploaded filename has no proper extension split
    filename_parts = image.filename.split(".")
    extension = filename_parts[-1].lower() if len(filename_parts) > 1 else "jpeg"
    
    # Just in case it's an atypical extension format from streamlit
    if extension not in ["jpg", "jpeg", "png"]:
        extension = "jpeg"

    filename = f"{uuid.uuid4()}.{extension}"
    image_path = os.path.join(upload_dir, filename)

    await image.seek(0)

    # Read the full file contents asynchronously to prevent empty/corrupted files
    contents = await image.read()
    
    # Write the complete byte stream to disk safely
    with open(image_path, "wb") as buffer:
        buffer.write(contents)
    file_size = os.path.getsize(image_path)
    print(f"=== DIAGNOSTIC: Saved image size: {file_size} bytes ===")
    print(f"=== DIAGNOSTIC: First 20 bytes: {contents[:20]} ===")
    # Close the internal spooled file to clean up resources
    await image.close()

    # Pass the fully written image path to your processing pipeline
    result = process_report(
        db=db,
        image_path=image_path,
        latitude=latitude,
        longitude=longitude,
        address=address,
        description=description
    )

    # ... (Keep your existing code above this line) ...

    # Pass the fully written image path to your processing pipeline
    result = process_report(
        db=db,
        image_path=image_path,
        latitude=latitude,
        longitude=longitude,
        address=address,
        description=description
    )

    # 🌟 NEW FIX: Safely convert the output to plain JSON format
    if isinstance(result, dict):
        return result
    
    # If the pipeline returned a database model object, extract its fields
    if hasattr(result, "__dict__"):
        # If your SQLAlchemy model has a helper method like .to_dict() or .json(), use that:
        if hasattr(result, "to_dict"):
            return result.to_dict()
        return {key: value for key, value in vars(result).items() if not key.startswith('_')}

    # Fallback to prevent any crash
    return {"status": "success", "data": str(result)}


# get all reports
@router.get("/",response_model=List[ReportResponse])
def get_reports(
    db: Session = Depends(get_db)
):
    return crud.get_all_reports(db)

#get report by id
@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = crud.get_report_by_id(db, report_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="report not found"
        )
    return report

#update report status
@router.patch("/{report_id}/status", response_model=ReportResponse)
def update_status(report_id: int, report: ReportUpdate, db: Session=Depends(get_db)):
    Updated = crud.update_report_status(
        db,
        report_id,
        report.status
    )

    if Updated is None :
        raise HTTPException(
            status_code=404,
            detail = "report not found"
        )
    return Updated

#UPDATE REPORT DEPARTMENT
@router.patch(
        
        "/{report_id}/department",
        response_model=ReportResponse
        )
def update_department(
    report_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_department(
        db,
        report_id,
        department.department
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return updated

#AI PREDICTION UPDATE
@router.patch("/{report_id}/prediction",
              response_model=ReportResponse)
def update_prediction(
    report_id: int,
    prediction: AIPredictionUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_ai_prediction(
        db,
        report_id,
        prediction.incident_type,
        prediction.severity,
        prediction.confidence,
        prediction.summary,
        prediction.embedding
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return updated


#DELETE REPORT
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_report(
        db,
        report_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "message": "Report deleted successfully"
    }