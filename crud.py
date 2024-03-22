from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

def create_person(db: Session, person: schemas.PersonCreate):
    """Creates a person entry in the database."""
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    """Retrieves a person by ID from the database."""
    return db.query(models.Person).filter(models.Person.person_id == person_id).first()

def update_person(db: Session, person_id: int, update_data: schemas.PersonUpdate):
    """Updates a person's information in the database."""
    db_person = db.query(models.Person).filter(models.Person.person_id == person_id).first()
    [setattr(db_person, key, value) for key, value in update_data.dict(exclude_unset=True).items()]
    db_person.updated_at = datetime.utcnow();
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    """Deletes a person from the database."""
    db_person = db.query(models.Person).filter(models.Person.person_id == person_id).first()
    db.delete(db_person)
    db.commit()
    return {"ok": True}

def create_medical_condition(db: Session, medical_condition: schemas.MedicalConditionCreate):
    """Creates a medical condition entry in the database."""
    db_medical_condition = models.MedicalCondition(**medical_condition.dict())
    db.add(db_medical_condition)
    db.commit()
    db.refresh(db_medical_condition)
    return db_medical_condition

def get_medical_condition(db: Session, medical_condition_id: int):
    """Retrieves a medical condition by ID from the database."""
    return db.query(models.MedicalCondition).\
        filter(models.MedicalCondition.medical_condition_id == medical_condition_id).first()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    """Creates an appointment entry in the database."""
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments_for_person(db: Session, person_id: int):
    """Retrieves all appointments for a specific person from the database."""
    return db.query(models.Appointment).filter(models.Appointment.person_id == person_id).all()

def create_patient_journey(db: Session, journey: schemas.PatientJourneyCreate):
    """Creates a patient journey entry in the database."""
    db_journey = models.PatientJourney(**journey.dict())
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)
    return db_journey

def get_patient_journey(db: Session, journey_id: int):
    """Retrieves a patient journey by ID from the database."""
    return db.query(models.PatientJourney).filter(models.PatientJourney.journey_id == journey_id).first()

def create_referral(db: Session, referral: schemas.ReferralCreate):
    """Creates a referral entry in the database."""
    db_referral = models.Referral(**referral.dict())
    db.add(db_referral)
    db.commit()
    db.refresh(db_referral)
    return db_referral

def get_referral(db: Session, referral_id: int):
    """Retrieves a referral by ID from the database."""
    return db.query(models.Referral).filter(models.Referral.referral_id == referral_id).first()

def create_physician_details(db: Session, details: schemas.PhysicianDetailsCreate):
    """Creates physician details entry in the database."""
    db_details = models.PhysicianDetails(**details.dict())
    db.add(db_details)
    db.commit()
    db.refresh(db_details)
    return db_details

def get_physician_details(db: Session, details_id: int):
    """Retrieves physician details by ID from the database."""
    return db.query(models.PhysicianDetails).filter(models.PhysicianDetails.physician_details_id == details_id).first()

def create_hospital(db: Session, hospital: schemas.HospitalCreate):
    """Creates a hospital entry in the database."""
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital(db: Session, hospital_id: int):
    """Retrieves a hospital by ID from the database."""
    return db.query(models.Hospital).filter(models.Hospital.hospital_id == hospital_id).first()
