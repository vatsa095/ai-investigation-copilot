from sqlalchemy.orm import Session

from app.models import (
    Case,
    Person,
    Phone,
    Vehicle,
    PersonCase,
    Evidence,
    CaseVehicle
)


def get_ai_cases(db: Session):

    results = []

    links = db.query(PersonCase).all()

    for link in links:

        # --------------------------------
        # PERSON
        # --------------------------------

        person = db.query(Person).filter(
            Person.id == link.person_id
        ).first()

        # --------------------------------
        # CASE
        # --------------------------------

        case = db.query(Case).filter(
            Case.id == link.case_id
        ).first()

        if not person or not case:
            continue

        # --------------------------------
        # PHONE
        # --------------------------------

        phone = db.query(Phone).filter(
            Phone.person_id == person.id
        ).first()

        # --------------------------------
        # VEHICLES
        # --------------------------------
        # First use the new CASE <-> VEHICLE
        # relationship.

        case_vehicle_links = db.query(
            CaseVehicle
        ).filter(
            CaseVehicle.case_id == case.id
        ).all()

        vehicles = []

        for case_vehicle in case_vehicle_links:

            vehicle = db.query(Vehicle).filter(
                Vehicle.id == case_vehicle.vehicle_id
            ).first()

            if vehicle:
                vehicles.append(
                    vehicle.vehicle_number
                )

        # --------------------------------
        # FALLBACK
        # --------------------------------
        # Keep compatibility with your
        # existing CASE001-CASE052 data.

        if not vehicles:

            vehicle = db.query(Vehicle).filter(
                Vehicle.person_id == person.id
            ).first()

            if vehicle:
                vehicles.append(
                    vehicle.vehicle_number
                )

        # --------------------------------
        # EVIDENCE
        # --------------------------------

        evidence = db.query(Evidence).filter(
            Evidence.case_id == case.id
        ).first()

        # --------------------------------
        # RESULT
        # --------------------------------

        results.append({

            "case_id": case.id,

            "case_number": case.case_number,

            "suspect_name": person.full_name,

            "phone_number":
                phone.phone_number
                if phone
                else "",

            "vehicle_number":
                vehicles[0]
                if vehicles
                else "",

            "vehicle_numbers":
                vehicles,

            "crime_type":
                case.crime_type,

            "location":
                case.location.strip()
                if case.location
                else "",

            "evidence":
                evidence.evidence_type
                if evidence
                else ""

        })

    return results