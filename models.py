from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class RoleType(enum.Enum):
    patient = "patient"
    physician = "physician"
    pharmacist = "pharmacist"


class ReferralType(enum.Enum):
    EAP = "EAP"
    CT = "CT"


class StageType(enum.Enum):
    lead = "lead"
    patient = "patient"
    referral = "referral"


class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role_type = Column(Enum(RoleType))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="person")
    patient_journeys = relationship("PatientJourney", back_populates="person")
    physician_details = relationship("PhysicianDetails", uselist=False, back_populates="person")


class MedicalCondition(Base):
    __tablename__ = "medical_condition"
    medical_condition_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    abbreviation = Column(String, index=True)

    patient_journeys = relationship("PatientJourney", back_populates="medical_condition")


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    appointment_time = Column(DateTime, index=True)
    outcome = Column(Text)
    notes = Column(Text)

    person = relationship("Person", back_populates="appointments")


class PatientJourney(Base):
    __tablename__ = "patient_journey"
    journey_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    medical_condition_id = Column(Integer, ForeignKey("medical_condition.medical_condition_id"))
    stage = Column(Enum(StageType))
    referral_id = Column(Integer, ForeignKey("referral.referral_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship("Person", back_populates="patient_journeys")
    medical_condition = relationship("MedicalCondition", back_populates="patient_journeys")
    referral = relationship("Referral", back_populates="patient_journeys")


class Referral(Base):
    __tablename__ = "referral"
    referral_id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ReferralType))
    details = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    patient_journeys = relationship("PatientJourney", back_populates="referral")


class PhysicianDetails(Base):
    __tablename__ = "physician_details"
    physician_details_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    medical_license_number = Column(String, index=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id"))

    person = relationship("Person", back_populates="physician_details")
    hospital = relationship("Hospital", back_populates="physician_details")


class Hospital(Base):
    __tablename__ = "hospital"
    hospital_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)

    physician_details = relationship("PhysicianDetails", back_populates="hospital")
