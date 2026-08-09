from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas import CaseCreate, CaseResponse

from app.models import (
    Case,
    Person,
    PersonCase,
    Evidence,
    Investigation,
    Timeline
)

from app.crud.case import (
    create_case,
    get_case_by_id,
    get_all_cases,
    update_case,
    delete_case
)


router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)


# -----------------------------
# CREATE CASE
# -----------------------------

@router.post("/", response_model=CaseResponse)
def add_case(
    case: CaseCreate,
    db: Session = Depends(get_db)
):
    new_case = create_case(db, case)

    return read_case(
        new_case.id,
        db
    )


# -----------------------------
# GET ALL CASES
# -----------------------------

@router.get("/", response_model=list[CaseResponse])
def read_cases(
    db: Session = Depends(get_db)
):
    return get_all_cases(db)


# -----------------------------
# GET CASE BY ID
# -----------------------------

@router.get("/{case_id}", response_model=CaseResponse)
def read_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    # Find case
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    # -----------------------------
    # FIND PERSONS CONNECTED TO CASE
    # -----------------------------

    person_links = db.query(PersonCase).filter(
        PersonCase.case_id == case_id
    ).all()

    persons = []

    for link in person_links:

        person = db.query(Person).filter(
            Person.id == link.person_id
        ).first()

        if not person:
            continue

        persons.append({
            "id": person.id,
            "full_name": person.full_name,
            "role": link.role,
            "phones": person.phones,
            "vehicles": person.vehicles
        })

    # -----------------------------
    # FIND EVIDENCE
    # -----------------------------

    evidence = db.query(Evidence).filter(
        Evidence.case_id == case_id
    ).all()

    # -----------------------------
    # FIND INVESTIGATION NOTES
    # -----------------------------

    investigations = db.query(Investigation).filter(
        Investigation.case_id == case_id
    ).all()

    # -----------------------------
    # FIND TIMELINE
    # -----------------------------

    timeline = db.query(Timeline).filter(
        Timeline.case_id == case_id
    ).order_by(
        Timeline.event_time
    ).all()

    # -----------------------------
    # RETURN COMPLETE CASE
    # -----------------------------

    return {
        "id": case.id,
        "case_number": case.case_number,
        "crime_type": case.crime_type,
        "status": case.status,
        "location": case.location.strip(),
        "incident_date": case.incident_date,
        "summary": case.summary,
        "created_at": case.created_at,

        "persons": persons,

        "evidence": evidence,

        "investigations": investigations,

        "timeline": timeline
    }


# -----------------------------
# UPDATE CASE
# -----------------------------

@router.put("/{case_id}", response_model=CaseResponse)
def edit_case(
    case_id: int,
    case: CaseCreate,
    db: Session = Depends(get_db)
):

    updated_case = update_case(
        db,
        case_id,
        case
    )

    if not updated_case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return updated_case


# -----------------------------
# DELETE CASE
# -----------------------------

@router.delete("/{case_id}")
def remove_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    success = delete_case(
        db,
        case_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return {
        "message": "Case deleted successfully"
    }