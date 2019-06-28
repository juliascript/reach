from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ensures a single database session is used 
# through all the request, and then closed afterwards
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

'''
The parameter db is actually of type SessionLocal, but this class (created with sessionmaker()) is a "proxy" of a SQLAlchemy Session, so, the editor doesn't really know what methods are provided.

But by declaring the type as Session, the editor now can know the available methods (.add(), .query(), .commit(), etc) and can provide better support (like completion). The type declaration doesn't affect the actual object.
'''

# Dependency
def get_db(request: Request):
    return request.state.db

@app.put("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get('/users/', response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.put("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventBase, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None: 
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.put('/events/{event_id}', response_model=schemas.Event)
async def update_event(event_id: int, event: schemas.EventBase, db: Session = Depends(get_db)):
    print(event)
    update_event_encoded = jsonable_encoder(event)
    db_event = crud.update_event(db, event_id=event_id, event=update_event_encoded)
    return db_event


# this functionality would be written in other parts of the app (ex: a button is clicked that would trigger this code)
# just creating this endpoint because I want to add users to events arbitrarily to test the app right now 
@app.get('/addusertoevent', response_model=schemas.Event)
async def add_user_to_event(user_id:int, event_id: int, db: Session = Depends(get_db)):
    db_event = crud.add_user_to_event(db, event_id=event_id, user_id=user_id)
    return db_event
