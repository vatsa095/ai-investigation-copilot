from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


# -----------------------------
# PERSON
# -----------------------------

class PersonBase(BaseModel):
    full_name: str
    alias: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None


class PersonCreate(PersonBase):
    pass


class PersonResponse(PersonBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# PHONE
# -----------------------------

class PhoneBase(BaseModel):
    phone_number: str
    person_id: int


class PhoneCreate(PhoneBase):
    pass


class PhoneResponse(PhoneBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# VEHICLE
# -----------------------------

class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_type: Optional[str] = None
    person_id: int


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# CASE CREATE
# -----------------------------

class CaseBase(BaseModel):
    case_number: str
    crime_type: str
    status: str
    location: str
    incident_date: date
    summary: str


class CaseCreate(BaseModel):
    crime_type: str
    suspect_name: str
    phone_number: str
    vehicle_number: Optional[str] = None
    location: str
    incident_date: date
    evidence: str
    summary: str


# -----------------------------
# EVIDENCE
# -----------------------------

class EvidenceBase(BaseModel):
    evidence_type: str
    description: str
    case_id: int


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceResponse(EvidenceBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# CASE PERSON
# -----------------------------

class CasePersonResponse(BaseModel):
    id: int
    full_name: str
    role: str
    phones: list[PhoneResponse] = []
    vehicles: list[VehicleResponse] = []

    class Config:
        from_attributes = True


# -----------------------------
# INVESTIGATION NOTE
# -----------------------------

class InvestigationResponse(BaseModel):
    id: int
    case_id: int
    officer_name: str
    notes: str
    next_step: str

    class Config:
        from_attributes = True


# -----------------------------
# TIMELINE
# -----------------------------

class TimelineResponse(BaseModel):
    id: int
    case_id: int
    event_time: datetime
    event: str

    class Config:
        from_attributes = True


# -----------------------------
# COMPLETE CASE RESPONSE
# -----------------------------

class CaseResponse(BaseModel):
    id: int
    case_number: str
    crime_type: str
    status: str
    location: str
    incident_date: date
    summary: str
    created_at: datetime

    persons: list[CasePersonResponse] = []
    evidence: list[EvidenceResponse] = []
    investigations: list[InvestigationResponse] = []
    timeline: list[TimelineResponse] = []

    class Config:
        from_attributes = True