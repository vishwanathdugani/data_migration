# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import SessionLocal, engine
import crud
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/persons/", response_model=schemas.PersonRead)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db=db, person=person)


@app.get("/persons/{person_id}", response_model=schemas.PersonRead)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.put("/persons/{person_id}", response_model=schemas.PersonRead)
def update_person(person_id: int, person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    return crud.update_person(db=db, person_id=person_id, person=person)


@app.delete("/persons/{person_id}", response_model=dict)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    crud.delete_person(db, person_id=person_id)
    return {"ok": True}
