from lib2to3.pgen2.token import STRING
from sqlalchemy import Column, Integer, String
from apps.models.database import Base

class Record(Base):
    __tablename__ = "records"
    no = Column(Integer, primary_key=True, index=True)
    title =  Column(String)
    author = Column(String)
    date = Column(String)
    content = Column(String)
    link_picture = Column(String)
    url = Column(String)
    