from sqlalchemy.orm import Session
import models, schemas


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.person_id == person_id).first()


def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def update_person(db: Session, person_id: int, person: schemas.PersonUpdate):
    db_person = db.query(models.Person).get(person_id)
    if db_person:
        update_data = person.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_person, key, value)
        db.commit()
        db.refresh(db_person)
    return db_person


def delete_person(db: Session, person_id: int):
    db_person = db.query(models.Person).get(person_id)
    if db_person:
        db.delete(db_person)
        db.commit()
