from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base


# ============================================================
# PERSON TABLE
# ============================================================

class Person(Base):

    __tablename__ = "persons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    alias = Column(String)

    gender = Column(String)

    dob = Column(Date)

    address = Column(Text)

    phones = relationship(
        "Phone",
        back_populates="person"
    )

    vehicles = relationship(
        "Vehicle",
        back_populates="person"
    )

    cases = relationship(
        "PersonCase",
        back_populates="person"
    )


# ============================================================
# PHONE TABLE
# ============================================================

class Phone(Base):

    __tablename__ = "phones"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    phone_number = Column(
        String,
        unique=True,
        nullable=False
    )

    person_id = Column(
        Integer,
        ForeignKey("persons.id")
    )

    person = relationship(
        "Person",
        back_populates="phones"
    )


# ============================================================
# VEHICLE TABLE
# ============================================================

class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_number = Column(
        String,
        unique=True
    )

    vehicle_type = Column(String)

    # Existing owner/person.
    # We KEEP this so existing data is not broken.
    person_id = Column(
        Integer,
        ForeignKey("persons.id")
    )

    person = relationship(
        "Person",
        back_populates="vehicles"
    )

    # NEW:
    # Allows the same vehicle to be connected
    # to multiple cases.
    case_links = relationship(
        "CaseVehicle",
        back_populates="vehicle"
    )


# ============================================================
# CASE TABLE
# ============================================================

class Case(Base):

    __tablename__ = "cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    case_number = Column(
        String,
        unique=True
    )

    crime_type = Column(String)

    status = Column(String)

    location = Column(String)

    incident_date = Column(Date)

    summary = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    persons = relationship(
        "PersonCase",
        back_populates="case"
    )

    evidences = relationship(
        "Evidence",
        back_populates="case"
    )

    # NEW:
    # Cases can now be linked to vehicles.
    vehicles = relationship(
        "CaseVehicle",
        back_populates="case"
    )


# ============================================================
# PERSON <-> CASE LINK TABLE
# ============================================================

class PersonCase(Base):

    __tablename__ = "person_case"

    id = Column(
        Integer,
        primary_key=True
    )

    person_id = Column(
        Integer,
        ForeignKey("persons.id")
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id")
    )

    role = Column(
        String
    )  # Suspect / Victim / Witness

    person = relationship(
        "Person",
        back_populates="cases"
    )

    case = relationship(
        "Case",
        back_populates="persons"
    )


# ============================================================
# EVIDENCE TABLE
# ============================================================

class Evidence(Base):

    __tablename__ = "evidence"

    id = Column(
        Integer,
        primary_key=True
    )

    evidence_type = Column(String)

    description = Column(Text)

    case_id = Column(
        Integer,
        ForeignKey("cases.id")
    )

    case = relationship(
        "Case",
        back_populates="evidences"
    )


# ============================================================
# CASE <-> VEHICLE LINK TABLE
# ============================================================
#
# THIS IS THE NEW PART.
#
# Example:
#
# Vehicle KA03MN4521
#       |
#       +---- CASE053
#       |       |
#       |       +---- Person A
#       |
#       +---- CASE054
#       |       |
#       |       +---- Person B
#       |
#       +---- CASE055
#               |
#               +---- Person C
#
# This allows different people to use the same vehicle
# in different cases.
# ============================================================

class CaseVehicle(Base):

    __tablename__ = "case_vehicle"

    id = Column(
        Integer,
        primary_key=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id")
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    case = relationship(
        "Case",
        back_populates="vehicles"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="case_links"
    )


# ============================================================
# ASSOCIATES TABLE
# ============================================================

class Associate(Base):

    __tablename__ = "associates"

    id = Column(
        Integer,
        primary_key=True
    )

    person1_id = Column(
        Integer,
        ForeignKey("persons.id")
    )

    person2_id = Column(
        Integer,
        ForeignKey("persons.id")
    )

    relationship_type = Column(String)


# ============================================================
# TIMELINE TABLE
# ============================================================

class Timeline(Base):

    __tablename__ = "timeline"

    id = Column(
        Integer,
        primary_key=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id")
    )

    event_time = Column(DateTime)

    event = Column(Text)


# ============================================================
# INVESTIGATION NOTES
# ============================================================

class Investigation(Base):

    __tablename__ = "investigation"

    id = Column(
        Integer,
        primary_key=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id")
    )

    officer_name = Column(String)

    notes = Column(Text)

    next_step = Column(Text)