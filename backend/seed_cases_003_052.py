import json
from datetime import date
from pathlib import Path

from app.database import SessionLocal
from app.models import Case, Person, Phone, Vehicle, PersonCase, Evidence


DATA_FILE = Path(__file__).with_name("demo_cases_CASE053_CASE102.json")


def seed():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()

    try:
        created_cases = 0
        created_persons = set()
        created_phones = set()
        created_vehicles = set()
        created_evidence = 0
        created_links = 0

        for item in data:

            case_number = item["case_id"]

            # -----------------------------
            # SKIP EXISTING CASE
            # -----------------------------

            existing_case = (
                db.query(Case)
                .filter(Case.case_number == case_number)
                .first()
            )

            if existing_case:
                print(f"Skipping {case_number} - already exists")
                continue

            # -----------------------------
            # PERSON
            # -----------------------------

            person = (
                db.query(Person)
                .filter(Person.full_name == item["suspect_name"])
                .first()
            )

            if not person:
                person = Person(
                    full_name=item["suspect_name"]
                )
                db.add(person)
                db.flush()
                created_persons.add(person.full_name)

            # -----------------------------
            # PHONE
            # -----------------------------

            phone = (
                db.query(Phone)
                .filter(
                    Phone.phone_number == item["phone_number"]
                )
                .first()
            )

            if not phone:
                phone = Phone(
                    phone_number=item["phone_number"],
                    person_id=person.id
                )
                db.add(phone)
                db.flush()
                created_phones.add(phone.phone_number)

            elif phone.person_id != person.id:
                print(
                    f"WARNING: phone {phone.phone_number} "
                    f"already belongs to another person. "
                    f"Keeping existing owner."
                )

            # -----------------------------
            # VEHICLE
            # -----------------------------

            vehicle = (
                db.query(Vehicle)
                .filter(
                    Vehicle.vehicle_number ==
                    item["vehicle_number"]
                )
                .first()
            )

            if not vehicle:
                vehicle = Vehicle(
                    vehicle_number=item["vehicle_number"],
                    person_id=person.id
                )
                db.add(vehicle)
                db.flush()
                created_vehicles.add(
                    vehicle.vehicle_number
                )

            elif vehicle.person_id != person.id:
                print(
                    f"SHARED VEHICLE: "
                    f"{vehicle.vehicle_number} "
                    f"is also used in {case_number} "
                    f"by {person.full_name}. "
                    f"Keeping existing vehicle owner."
                )

            # -----------------------------
            # CASE
            # -----------------------------

            new_case = Case(
                case_number=case_number,
                crime_type=item["crime_type"],
                status="Open",
                location=item["location"],
                incident_date=date.fromisoformat(
                    item["incident_date"]
                ),
                summary=item["summary"]
            )

            db.add(new_case)
            db.flush()
            created_cases += 1

            # -----------------------------
            # PERSON <-> CASE
            # -----------------------------

            db.add(
                PersonCase(
                    person_id=person.id,
                    case_id=new_case.id,
                    role="Suspect"
                )
            )

            created_links += 1

            # -----------------------------
            # EVIDENCE
            # -----------------------------

            db.add(
                Evidence(
                    evidence_type=item["evidence"],
                    description=item["summary"],
                    case_id=new_case.id
                )
            )

            created_evidence += 1

        db.commit()

        print("\n========================================")
        print("CASE053-CASE102 IMPORT COMPLETE")
        print("========================================")
        print(f"Cases created      : {created_cases}")
        print(f"Persons created    : {len(created_persons)}")
        print(f"Phones created     : {len(created_phones)}")
        print(f"Vehicles created   : {len(created_vehicles)}")
        print(f"Evidence created   : {created_evidence}")
        print(f"Case links created : {created_links}")
        print("========================================")
        print("\nExisting cases were not modified.")

    except Exception as e:
        db.rollback()
        print("\nSEED FAILED:")
        print(e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()