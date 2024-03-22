from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas
import crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/people/", response_model=schemas.Person, status_code=status.HTTP_201_CREATED)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    """Create a new person and return the created person object."""
    return crud.create_person(db=db, person=person)

@app.get("/people/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    """Retrieve a person by ID or return 404 if not found."""
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.put("/people/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    """Update a person by ID with the provided update data."""
    return crud.update_person(db=db, person_id=person_id, update_data=person)

@app.delete("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    """Delete a person by ID and return a confirmation response."""
    crud.delete_person(db, person_id=person_id)
    return {"ok": True}

@app.post("/medical_conditions/", response_model=schemas.MedicalCondition, status_code=status.HTTP_201_CREATED)
def create_medical_condition(medical_condition: schemas.MedicalConditionCreate, db: Session = Depends(get_db)):
    return crud.create_medical_condition(db=db, medical_condition=medical_condition)

@app.get("/medical_conditions/{medical_condition_id}", response_model=schemas.MedicalCondition)
def read_medical_condition(medical_condition_id: int, db: Session = Depends(get_db)):
    db_medical_condition = crud.get_medical_condition(db, medical_condition_id=medical_condition_id)
    if db_medical_condition is None:
        raise HTTPException(status_code=404, detail="Medical condition not found")
    return db_medical_condition

@app.post("/appointments/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)

@app.get("/appointments/person/{person_id}", response_model=List[schemas.Appointment])
def read_appointments_for_person(person_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_for_person(db, person_id=person_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointments not found for the person")
    return appointments


# PatientJourney Endpoints
@app.post("/patient_journeys/", response_model=schemas.PatientJourney, status_code=status.HTTP_201_CREATED)
def create_patient_journey(journey: schemas.PatientJourneyCreate, db: Session = Depends(get_db)):
    # You might want to include additional logic here, like validating person or medical condition existence
    return crud.create_patient_journey(db=db, journey=journey)

@app.get("/patient_journeys/{journey_id}", response_model=schemas.PatientJourney)
def read_patient_journey(journey_id: int, db: Session = Depends(get_db)):
    db_journey = crud.get_patient_journey(db, journey_id=journey_id)
    if db_journey is None:
        raise HTTPException(status_code=404, detail="Patient journey not found")
    return db_journey

# Referral Endpoints
@app.post("/referrals/", response_model=schemas.Referral, status_code=status.HTTP_201_CREATED)
def create_referral(referral: schemas.ReferralCreate, db: Session = Depends(get_db)):
    return crud.create_referral(db=db, referral=referral)

@app.get("/referrals/{referral_id}", response_model=schemas.Referral)
def read_referral(referral_id: int, db: Session = Depends(get_db)):
    db_referral = crud.get_referral(db, referral_id=referral_id)
    if db_referral is None:
        raise HTTPException(status_code=404, detail="Referral not found")
    return db_referral

# PhysicianDetails Endpoints
@app.post("/physician_details/", response_model=schemas.PhysicianDetails, status_code=status.HTTP_201_CREATED)
def create_physician_details(details: schemas.PhysicianDetailsCreate, db: Session = Depends(get_db)):
    return crud.create_physician_details(db=db, details=details)

@app.get("/physician_details/{details_id}", response_model=schemas.PhysicianDetails)
def read_physician_details(details_id: int, db: Session = Depends(get_db)):
    db_details = crud.get_physician_details(db, details_id=details_id)
    if db_details is None:
        raise HTTPException(status_code=404, detail="Physician details not found")
    return db_details

# Hospital Endpoints
@app.post("/hospitals/", response_model=schemas.Hospital, status_code=status.HTTP_201_CREATED)
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    return crud.create_hospital(db=db, hospital=hospital)

@app.get("/hospitals/{hospital_id}", response_model=schemas.Hospital)
def read_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = crud.get_hospital(db, hospital_id=hospital_id)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital