from typing import List

from pydantic import BaseModel


# class ItemBase(BaseModel):
#     title: str
#     description: str = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True
#  ------------

class UserBase(BaseModel):
    name: str
    email: str
    phone: int

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

