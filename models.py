from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class RoleType(enum.Enum):
    patient = "patient"
    physician = "physician"
    pharmacist = "pharmacist"
    patient_navigator = "patient_navigator"


class ReferralType(enum.Enum):
    EAP = "EAP"
    CT = "CT"


class StageType(enum.Enum):
    lead = "lead"
    patient = "patient"
    referral = "referral"


class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    role_type = Column(Enum(RoleType))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_returning = Column(Boolean, default=False)  # Flag to indicate a returning patient

    # Relationships
    appointments = relationship("Appointment", back_populates="person")
    patient_journeys = relationship("PatientJourney", back_populates="person")
    physician_details = relationship("PhysicianDetails", back_populates="person", uselist=False)


class Referral(Base):
    __tablename__ = "referral"
    referral_id = Column(Integer, primary_key=True)
    type = Column(Enum(ReferralType))
    details = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    ct_dossier = relationship("CTDossier", back_populates="referral", uselist=False)
    eap_dossier = relationship("EAPDossier", back_populates="referral", uselist=False)
    patient_journeys = relationship("PatientJourney", back_populates="referral")


class PatientJourney(Base):
    __tablename__ = "patient_journey"
    journey_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    medical_condition_id = Column(Integer, ForeignKey("medical_condition.medical_condition_id"))
    stage = Column(Enum(StageType))
    referral_id = Column(Integer, ForeignKey("referral.referral_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    physician_details_id = Column(Integer, ForeignKey("physician_details.physician_details_id"))

    # Relationships
    person = relationship("Person", back_populates="patient_journeys")
    referral = relationship("Referral", back_populates="patient_journeys")
    medical_condition = relationship("MedicalCondition", back_populates="patient_journeys")
    referring_physician = relationship("PhysicianDetails", backref="physician_details")


class Hospital(Base):
    __tablename__ = "hospital"
    hospital_id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    physician_details = relationship("PhysicianDetails", back_populates="hospital")


class PhysicianDetails(Base):
    __tablename__ = "physician_details"
    physician_details_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    medical_license_number = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id"))
    person = relationship("Person", back_populates="physician_details")
    hospital = relationship("Hospital", back_populates="physician_details")


class MedicalCondition(Base):
    __tablename__ = "medical_condition"
    medical_condition_id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
    patient_journeys = relationship("PatientJourney", back_populates="medical_condition")


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    appointment_time = Column(DateTime)
    outcome = Column(Text)
    notes = Column(Text)
    person = relationship("Person", back_populates="appointments")


class CTDossier(Base):
    __tablename__ = "ct_dossier"
    id = Column(Integer, primary_key=True)
    referral_id = Column(Integer, ForeignKey("referral.referral_id"))
    trial_id = Column(String)
    trial_name = Column(String)
    protocol_summary = Column(Text)
    referral = relationship("Referral", back_populates="ct_dossier")


class EAPDossier(Base):
    __tablename__ = "eap_dossier"
    id = Column(Integer, primary_key=True)
    referral_id = Column(Integer, ForeignKey("referral.referral_id"))
    eap_name = Column(String)
    eligibility_criteria = Column(Text)
    referral = relationship("Referral", back_populates="eap_dossier")
