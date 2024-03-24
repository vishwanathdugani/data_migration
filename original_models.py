from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contact'
    contact_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    contact_type = Column(String)
    medical_condition = Column(String)
    booking_date = Column(DateTime)
    reminder_date = Column(DateTime)
    no_show = Column(Boolean)
    job_title = Column(String)
    specialization = Column(String)
    medical_license_number = Column(String)
    hospital = Column(String)


class Patient(Base):
    __tablename__ = 'patient'
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    first_contact_date = Column(DateTime)
    initial_consult_date = Column(DateTime)
    medical_condition = Column(String)
    trial_id = Column(String)
    eligible = Column(String)
    ineligible_reason = Column(String)
    ct_referral_date = Column(DateTime)
    eap_enrollment_date = Column(DateTime)
    contact_record = Column(UUID(as_uuid=True), ForeignKey('contact.contact_id'))
    physician = Column(UUID(as_uuid=True))
    ct_outcome = Column(String)


class Hospital(Base):
    __tablename__ = 'hospital'
    hospital_id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)


class EAPDossier(Base):
    __tablename__ = 'eap_dossier'
    eap_dossier_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    eap_number = Column(String)
    patient = Column(UUID(as_uuid=True), ForeignKey('patient.patient_id'))
    product = Column(String)
    eap_enrollment_date = Column(DateTime)


class MedicalCondition(Base):
    __tablename__ = 'medical_condition'
    medical_condition_id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
