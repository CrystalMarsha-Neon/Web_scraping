from typing import  List
from datetime import date
from pydantic import BaseModel

class RequestNo(BaseModel):
    page: int = None

class Record(BaseModel):
    no: int = None
    title: str = None
    author: str = None
    date: str = None
    content: str = None
    link_picture: str  = None
    url: str = None
    
    class Config:
        orm_mode = True
