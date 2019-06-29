from typing import List

from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    phone: str

class User(UserBase):
    id: int
    # events: List[Event] = []

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    name: str
    location: str
    date: str #change to datetime 
    time: str #change to datetime 
    description: str

class Event(EventBase):
    id: int
    participants: List[User] = []

    class Config:
        orm_mode = True

