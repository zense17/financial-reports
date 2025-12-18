from sqlalchemy import Column, Integer, String, Float, Date
from db import Base

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    description = Column(String)
    amount = Column(Float)

class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Float)
