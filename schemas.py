from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleType(str, Enum):
    patient = "patient"
    physician = "physician"
    pharmacist = "pharmacist"

class ReferralType(str, Enum):
    EAP = "EAP"
    CT = "CT"

class StageType(str, Enum):
    lead = "lead"
    patient = "patient"
    referral = "referral"

# MedicalCondition Schemas
class MedicalConditionBase(BaseModel):
    name: str
    abbreviation: str

class MedicalConditionCreate(MedicalConditionBase):
    pass

class MedicalCondition(MedicalConditionBase):
    medical_condition_id: int

    class Config:
        from_attributes = True

# Person Schemas
class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_type: RoleType

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class Person(PersonBase):
    person_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Appointment Schemas
class AppointmentBase(BaseModel):
    appointment_time: datetime
    outcome: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    person_id: int

class Appointment(AppointmentBase):
    appointment_id: int
    person: Person

    class Config:
        from_attributes = True

# PatientJourney Schemas
class PatientJourneyBase(BaseModel):
    stage: StageType
    created_at: datetime

class PatientJourneyCreate(PatientJourneyBase):
    person_id: int
    medical_condition_id: int
    referral_id: Optional[int] = None

class PatientJourney(PatientJourneyBase):
    journey_id: int
    person: Person
    medical_condition: MedicalCondition
    referral: Optional['Referral'] = None

    class Config:
        from_attributes = True

# Referral Schemas
class ReferralBase(BaseModel):
    type: ReferralType
    details: str
    start_date: datetime
    end_date: datetime

class ReferralCreate(ReferralBase):
    pass

class Referral(ReferralBase):
    referral_id: int
    patient_journeys: List[PatientJourney] = []

    class Config:
        from_attributes = True

# PhysicianDetails Schemas
class PhysicianDetailsBase(BaseModel):
    medical_license_number: str
    hospital_id: int

class PhysicianDetailsCreate(PhysicianDetailsBase):
    person_id: int

class PhysicianDetails(PhysicianDetailsBase):
    physician_details_id: int
    person: Person

    class Config:
        from_attributes = True

# Hospital Schemas
class HospitalBase(BaseModel):
    name: str
    city: str

class HospitalCreate(HospitalBase):
    pass

class Hospital(HospitalBase):
    hospital_id: int
    physician_details: List[PhysicianDetails] = []

    class Config:
        from_attributes = True

# To allow forward references (for recursive models), update Referral's schema to recognize PatientJourney
Referral.update_forward_refs()
