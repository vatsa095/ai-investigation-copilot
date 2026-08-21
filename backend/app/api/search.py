from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Person,
    Phone,
    Vehicle,
    Case,
    PersonCase,
    Evidence
)

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def universal_search(
    query: str,
    db: Session = Depends(get_db)
):

    query = query.strip()

    if not query:
        return {
            "query": query,
            "persons": [],
            "phones": [],
            "vehicles": [],
            "cases": [],
            "person_cases": [],
            "phone_cases": [],
            "vehicle_cases": []
        }

    search = f"%{query}%"

    # --------------------------------
    # DIRECT SEARCH
    # --------------------------------

    persons = db.query(Person).filter(
        Person.full_name.ilike(search)
    ).all()

    phones = db.query(Phone).filter(
        Phone.phone_number.ilike(search)
    ).all()

    vehicles = db.query(Vehicle).filter(
        Vehicle.vehicle_number.ilike(search)
    ).all()

    direct_cases = db.query(Case).filter(
        (Case.case_number.ilike(search)) |
        (Case.crime_type.ilike(search)) |
        (Case.location.ilike(search))
    ).all()

    # --------------------------------
    # FIND ALL RELATED PERSONS
    # --------------------------------

    person_ids = set()

    # Person matched directly
    for person in persons:
        person_ids.add(person.id)

    # Person matched through phone
    for phone in phones:
        if phone.person_id:
            person_ids.add(phone.person_id)

    # Person matched through vehicle
    for vehicle in vehicles:
        if vehicle.person_id:
            person_ids.add(vehicle.person_id)

    # --------------------------------
    # LOAD RELATED PERSONS
    # --------------------------------

    related_persons = []

    if person_ids:

        related_persons = db.query(Person).filter(
            Person.id.in_(person_ids)
        ).all()

    # --------------------------------
    # CASES CONNECTED TO PERSONS
    # --------------------------------

    person_cases = []

    related_case_ids = set()

    for person in related_persons:

        links = db.query(PersonCase).filter(
            PersonCase.person_id == person.id
        ).all()

        for link in links:

            case = db.query(Case).filter(
                Case.id == link.case_id
            ).first()

            if not case:
                continue

            related_case_ids.add(case.id)

            person_cases.append({
                "person": person.full_name,
                "person_id": person.id,
                "role": link.role,

                "case_id": case.id,
                "case_number": case.case_number,
                "crime_type": case.crime_type,
                "status": case.status,
                "location": case.location,
                "incident_date": case.incident_date,
                "summary": case.summary
            })

    # --------------------------------
    # INCLUDE DIRECT CASE RESULTS
    # --------------------------------

    all_case_ids = set(related_case_ids)

    for case in direct_cases:
        all_case_ids.add(case.id)

    all_cases = []

    if all_case_ids:

        all_cases = db.query(Case).filter(
            Case.id.in_(all_case_ids)
        ).order_by(Case.id).all()

    # --------------------------------
    # GET ALL PHONES FOR MATCHED PEOPLE
    # --------------------------------

    all_phones = []

    if person_ids:

        all_phones = db.query(Phone).filter(
            Phone.person_id.in_(person_ids)
        ).all()

    # --------------------------------
    # GET ALL VEHICLES FOR MATCHED PEOPLE
    # --------------------------------

    all_vehicles = []

    if person_ids:

        all_vehicles = db.query(Vehicle).filter(
            Vehicle.person_id.in_(person_ids)
        ).all()

    # --------------------------------
    # PHONE → CASE CONNECTIONS
    # --------------------------------

    phone_cases = []

    for phone in all_phones:

        if not phone.person_id:
            continue

        links = db.query(PersonCase).filter(
            PersonCase.person_id == phone.person_id
        ).all()

        person = db.query(Person).filter(
            Person.id == phone.person_id
        ).first()

        for link in links:

            case = db.query(Case).filter(
                Case.id == link.case_id
            ).first()

            if case:

                phone_cases.append({
                    "phone_number": phone.phone_number,
                    "person": person.full_name if person else None,
                    "person_id": phone.person_id,

                    "role": link.role,

                    "case_id": case.id,
                    "case_number": case.case_number,
                    "crime_type": case.crime_type,
                    "status": case.status,
                    "location": case.location,
                    "incident_date": case.incident_date,
                    "summary": case.summary
                })

    # --------------------------------
    # VEHICLE → CASE CONNECTIONS
    # --------------------------------

    vehicle_cases = []

    for vehicle in all_vehicles:

        if not vehicle.person_id:
            continue

        links = db.query(PersonCase).filter(
            PersonCase.person_id == vehicle.person_id
        ).all()

        person = db.query(Person).filter(
            Person.id == vehicle.person_id
        ).first()

        for link in links:

            case = db.query(Case).filter(
                Case.id == link.case_id
            ).first()

            if case:

                vehicle_cases.append({
                    "vehicle_number": vehicle.vehicle_number,
                    "vehicle_type": vehicle.vehicle_type,

                    "person": person.full_name
                    if person else None,

                    "person_id": vehicle.person_id,

                    "role": link.role,

                    "case_id": case.id,
                    "case_number": case.case_number,
                    "crime_type": case.crime_type,
                    "status": case.status,
                    "location": case.location,
                    "incident_date": case.incident_date,
                    "summary": case.summary
                })

    # --------------------------------
    # RETURN COMPLETE SEARCH RESULT
    # --------------------------------

    return {

        "query": query,

        # People involved
        "persons": [
            {
                "id": person.id,
                "full_name": person.full_name,
                "alias": person.alias,
                "gender": person.gender,
                "dob": person.dob,
                "address": person.address
            }
            for person in related_persons
        ],

        # All phones belonging to matched people
        "phones": [
            {
                "id": phone.id,
                "phone_number": phone.phone_number,
                "person_id": phone.person_id
            }
            for phone in all_phones
        ],

        # All vehicles belonging to matched people
        "vehicles": [
            {
                "id": vehicle.id,
                "vehicle_number": vehicle.vehicle_number,
                "vehicle_type": vehicle.vehicle_type,
                "person_id": vehicle.person_id
            }
            for vehicle in all_vehicles
        ],

        # All relevant cases
"cases": [
    {
        "id": case.id,
        "case_number": case.case_number,

        # Get person connected to this case
        "suspect_name": (
            db.query(Person.full_name)
            .join(PersonCase, PersonCase.person_id == Person.id)
            .filter(PersonCase.case_id == case.id)
            .first()[0]
            if db.query(PersonCase)
                .filter(PersonCase.case_id == case.id)
                .first()
            else None
        ),

        "crime_type": case.crime_type,
        "status": case.status,
        "location": case.location,
        "incident_date": case.incident_date,
        "summary": case.summary
    }
    for case in all_cases
],
        # Person → Case
        "person_cases": person_cases,

        # Phone → Person → Case
        "phone_cases": phone_cases,

        # Vehicle → Person → Case
        "vehicle_cases": vehicle_cases
    }