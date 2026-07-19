from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from database.db import get_db
from database import crud
from schemas.report import (ReportCreate, ReportResponse, DepartmentUpdate, AIPredictionUpdate, ReportUpdate)
from service.gemini import analyze_image
from fastapi import UploadFile, File, Form
import os
import uuid
import shutil

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

    extension = image.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    image_path = os.path.join(
        upload_dir,
        filename
    )

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    result = process_report(
        db=db,
        image_path=image_path,
        latitude=latitude,
        longitude=longitude,
        address=address,
        description=description
    )

    return result

# get all reports
@router.get("/",response_model=ReportResponse)
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