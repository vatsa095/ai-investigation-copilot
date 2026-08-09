from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Case, Person, Evidence

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics(db: Session = Depends(get_db)):

    # Total cases
    total_cases = db.query(Case).count()

    # Open cases
    open_cases = db.query(Case).filter(
        Case.status == "Open"
    ).count()

    # Closed cases
    closed_cases = db.query(Case).filter(
        Case.status == "Closed"
    ).count()

    # Total suspects/persons
    total_persons = db.query(Person).count()

    # Total evidence
    total_evidence = db.query(Evidence).count()

    # Crime distribution
    crime_data = db.query(
        Case.crime_type,
        func.count(Case.id)
    ).group_by(
        Case.crime_type
    ).all()

    crime_distribution = [
        {
            "crime_type": crime,
            "count": count
        }
        for crime, count in crime_data
    ]

    # Location distribution
    location_data = db.query(
        Case.location,
        func.count(Case.id)
    ).group_by(
        Case.location
    ).all()

    location_distribution = [
        {
            "location": location,
            "count": count
        }
        for location, count in location_data
    ]

    # Recent cases
    recent_cases = db.query(Case).order_by(
        Case.id.desc()
    ).limit(5).all()

    recent_cases_data = [
        {
            "id": case.id,
            "case_number": case.case_number,
            "crime_type": case.crime_type,
            "status": case.status,
            "location": case.location,
            "incident_date": case.incident_date
        }
        for case in recent_cases
    ]

    return {
        "total_cases": total_cases,
        "open_cases": open_cases,
        "closed_cases": closed_cases,
        "total_persons": total_persons,
        "total_evidence": total_evidence,
        "crime_distribution": crime_distribution,
        "location_distribution": location_distribution,
        "recent_cases": recent_cases_data
    }