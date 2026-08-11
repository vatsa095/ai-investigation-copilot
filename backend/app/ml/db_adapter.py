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

    # Get all person-case relationships
    links = db.query(PersonCase).all()

    for link in links:

        # =====================================================
        # PERSON
        # =====================================================

        person = db.query(Person).filter(
            Person.id == link.person_id
        ).first()

        if not person:
            continue

        # =====================================================
        # CASE
        # =====================================================

        case = db.query(Case).filter(
            Case.id == link.case_id
        ).first()

        if not case:
            continue

        # =====================================================
        # PHONE
        # =====================================================

        phone = db.query(Phone).filter(
            Phone.person_id == person.id
        ).first()

        phone_number = ""

        if phone:
            phone_number = str(
                phone.phone_number
            ).strip()

        # =====================================================
        # VEHICLES
        # =====================================================

        vehicles = []

        # First:
        # CASE -> VEHICLE relationship

        case_vehicle_links = db.query(
            CaseVehicle
        ).filter(
            CaseVehicle.case_id == case.id
        ).all()

        for case_vehicle in case_vehicle_links:

            vehicle = db.query(Vehicle).filter(
                Vehicle.id == case_vehicle.vehicle_id
            ).first()

            if vehicle:

                number = getattr(
                    vehicle,
                    "vehicle_number",
                    None
                )

                if number:

                    number = str(
                        number
                    ).strip()

                    if number not in vehicles:
                        vehicles.append(number)

        # =====================================================
        # VEHICLE FALLBACK
        # =====================================================

        # If the case does not have a CaseVehicle
        # relationship, use the person's vehicle.

        if not vehicles:

            person_vehicle = db.query(
                Vehicle
            ).filter(
                Vehicle.person_id == person.id
            ).first()

            if person_vehicle:

                number = getattr(
                    person_vehicle,
                    "vehicle_number",
                    None
                )

                if number:

                    number = str(
                        number
                    ).strip()

                    vehicles.append(number)

        # =====================================================
        # EVIDENCE
        # =====================================================

        evidence = db.query(
            Evidence
        ).filter(
            Evidence.case_id == case.id
        ).first()

        evidence_type = ""

        if evidence:

            evidence_type = str(
                getattr(
                    evidence,
                    "evidence_type",
                    ""
                )
            ).strip()

        # =====================================================
        # LOCATION
        # =====================================================

        location = ""

        if case.location:

            location = str(
                case.location
            ).strip()

        # =====================================================
        # CRIME TYPE
        # =====================================================

        crime_type = ""

        if case.crime_type:

            crime_type = str(
                case.crime_type
            ).strip()

        # =====================================================
        # CASE NUMBER
        # =====================================================

        case_number = ""

        if getattr(
            case,
            "case_number",
            None
        ):

            case_number = str(
                case.case_number
            ).strip()

        # =====================================================
        # RESULT
        # =====================================================

        results.append({

            "case_id":
                case.id,

            "case_number":
                case_number,

            "suspect_name":
                person.full_name,

            "phone_number":
                phone_number,

            "vehicle_number":
                vehicles[0]
                if vehicles
                else "",

            "vehicle_numbers":
                vehicles,

            "crime_type":
                crime_type,

            "location":
                location,

            "evidence":
                evidence_type
        })

    return results