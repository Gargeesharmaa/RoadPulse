from sqlalchemy.orm import Session
from .models import Report


# Create a new report
def create_report(db: Session, report_data: dict):
    # Get all valid column names from your Report database model
    valid_columns = {c.key for c in Report.__table__.columns}
    
    # If your database uses 'description' instead of 'summary', we can map it:
    if 'summary' in report_data and 'description' in valid_columns and not report_data.get('description'):
        report_data['description'] = report_data.pop('summary')
        
    # Filter out any extra keys (like 'summary' or anything else the AI added)
    filtered_data = {k: v for k, v in report_data.items() if k in valid_columns}
    
    # Create the instance safely
    report = Report(**filtered_data)
    
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# Get all reports
def get_all_reports(db: Session):
    return db.query(Report).all()


# Get report by ID
def get_report_by_id(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()


# Update report status
def update_report_status(db: Session, report_id: int, status: str):
    report = db.query(Report).filter(Report.id == report_id).first()

    if report:
        report.status = status
        db.commit()
        db.refresh(report)

    return report


# Update assigned department
def update_department(db: Session, report_id: int, department: str):
    report = db.query(Report).filter(Report.id == report_id).first()

    if report:
        report.department = department
        db.commit()
        db.refresh(report)

    return report


# Update duplicate count
def update_duplicate_count(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()

    if report:
        report.duplicate_count += 1
        db.commit()
        db.refresh(report)

    return report


# Update AI prediction
def update_ai_prediction(
    db: Session,
    report_id: int,
    incident_type: str,
    severity: str,
    confidence: float,
    summary: str,
    embedding: str
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if report:
        report.incident_type = incident_type
        report.severity = severity
        report.confidence = confidence
        report.summary = summary
        report.embedding = embedding

        
        db.commit()
        db.refresh(report)

    return report


# Delete report
def delete_report(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()

    if report:
        db.delete(report)
        db.commit()

    return report
