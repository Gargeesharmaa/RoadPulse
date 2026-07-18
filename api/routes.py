from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from database.db import get_db
from database import crud
from schemas.report import (ReportCreate, ReportResponse, DepartmentUpdate, AIPredictionUpdate, ReportUpdate)

router = APIRouter(
    prefix="/reports",
    tags=['RoadPulse Report']
)

# create a report
@router.post("/", response_model=ReportResponse)
def create_new_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    return crud.create_report(db, report.model_dump())

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
        prediction.confidence
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