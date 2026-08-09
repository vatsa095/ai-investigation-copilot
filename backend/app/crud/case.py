from sqlalchemy.orm import Session
from app.models import Case, Person, Phone, Vehicle, Evidence, PersonCase


# -----------------------------
# CREATE CASE
# -----------------------------

def create_case(db: Session, case):

    # 1. CREATE CASE
    new_case = Case(
        crime_type=case.crime_type,
        status="Open",
        location=case.location,
        incident_date=case.incident_date,
        summary=case.summary
    )

    db.add(new_case)
    db.flush()

    # Automatically generate case number
    new_case.case_number = f"CASE{new_case.id:03d}"

    # 2. FIND OR CREATE SUSPECT
    person = db.query(Person).filter(
        Person.full_name == case.suspect_name
    ).first()

    if not person:
        person = Person(
            full_name=case.suspect_name
        )

        db.add(person)
        db.flush()

    # 3. PHONE
    if case.phone_number:

        phone = db.query(Phone).filter(
            Phone.phone_number == case.phone_number
        ).first()

        if not phone:
            phone = Phone(
                phone_number=case.phone_number,
                person_id=person.id
            )

            db.add(phone)

    # 4. VEHICLE
    if case.vehicle_number:

        vehicle = db.query(Vehicle).filter(
            Vehicle.vehicle_number == case.vehicle_number
        ).first()

        if not vehicle:
            vehicle = Vehicle(
                vehicle_number=case.vehicle_number,
                person_id=person.id
            )

            db.add(vehicle)

    # 5. LINK SUSPECT TO CASE
    person_case = PersonCase(
        person_id=person.id,
        case_id=new_case.id,
        role="Suspect"
    )

    db.add(person_case)

    # 6. EVIDENCE
    evidence = Evidence(
        evidence_type=case.evidence,
        description=case.summary,
        case_id=new_case.id
    )

    db.add(evidence)

    # 7. SAVE
    db.commit()
    db.refresh(new_case)

    return new_case

# -----------------------------
# GET CASE BY ID
# -----------------------------
def get_case_by_id(db: Session, case_id: int):

    return db.query(Case).filter(
        Case.id == case_id
    ).first()


# -----------------------------
# GET CASE NUMBER
# -----------------------------
def get_case_number(db: Session, case_number: str):

    return db.query(Case).filter(
        Case.case_number == case_number
    ).first()


# -----------------------------
# GET ALL CASES
# -----------------------------
def get_all_cases(db: Session):

    return db.query(Case).all()


# -----------------------------
# SEARCH CASES
# -----------------------------
def search_cases(db: Session, keyword: str):

    return db.query(Case).filter(

        (Case.case_number.ilike(f"%{keyword}%")) |
        (Case.crime_type.ilike(f"%{keyword}%")) |
        (Case.location.ilike(f"%{keyword}%"))

    ).all()


# -----------------------------
# UPDATE CASE
# -----------------------------
def update_case(db: Session, case_id: int, data):

    case = get_case_by_id(db, case_id)

    if not case:
        return None

    case.case_number = data.case_number
    case.crime_type = data.crime_type
    case.status = data.status
    case.location = data.location
    case.incident_date = data.incident_date
    case.summary = data.summary

    db.commit()
    db.refresh(case)

    return case


# -----------------------------
# DELETE CASE
# -----------------------------
def delete_case(db: Session, case_id: int):

    case = get_case_by_id(db, case_id)

    if not case:
        return False

    db.delete(case)
    db.commit()

    return True