''''
This is used to create the database.
'''
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL =  "sqlite:///C:/Users/kalya/OneDrive/Desktop/Crayon Data/src/app/ticket_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    ticket_id = Column(String(10), primary_key=True)
    customer_id = Column(String(10))
    date_created = Column(String(10))
    category = Column(String(50))
    subcategory = Column(String(50))
    priority = Column(String(10))
    issue_description = Column(Text)
    resolution = Column(Text)
    resolution_time_hours = Column(String(10))
    customer_satisfaction = Column(String(10))
    agent_id = Column(String(10))

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewTicket(Base):
    __tablename__ = "new_tickets"
    ticket_id = Column(String(10), primary_key=True)
    issue_description = Column(Text)
    category = Column(String(50))
    confirmed_category = Column(String, nullable=True)
    status = Column(String(20), default="Pending")
    draft_resolution = Column(Text)
    final_resolution = Column(Text)
    resolution_time_hours = Column(String(10))
    submission_time = Column(DateTime, default=datetime.now)  # Add submission time

# Create tables
Base.metadata.create_all(bind=engine)