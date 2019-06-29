from sqlalchemy.orm import Session

from . import models, schemas

def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventBase):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.EventBase):
    db_event = get_event(db, event_id)
    db_new_event_details = models.Event(**event, participants=db_event.participants, id=event_id)

    db.delete(db_event)
    db.add(db_new_event_details)
    db.commit()
    db.refresh(db_new_event_details)
    return db_new_event_details

def add_user_to_event(db: Session, user_id: int, event_id: int):
    db_entry = models.EventInterest(event_id=event_id, user_id=user_id)
    
    # add new user/event pair to association table
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # return the updated event
    db_event = get_event(db, event_id)
    return db_event





