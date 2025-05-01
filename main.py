from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

app = FastAPI()
engine = create_engine("sqlite:///travel.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Association Tables
itinerary_activity = Table('itinerary_activity', Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('itineraries.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)
itinerary_transfer = Table('itinerary_transfer', Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('itineraries.id')),
    Column('transfer_id', Integer, ForeignKey('transfers.id'))
)

# Models
class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

class Transfer(Base):
    __tablename__ = 'transfers'
    id = Column(Integer, primary_key=True)
    from_location = Column(String)
    to_location = Column(String)

class Itinerary(Base):
    __tablename__ = 'itineraries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nights = Column(Integer)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    hotel = relationship("Hotel")
    activities = relationship("Activity", secondary=itinerary_activity)
    transfers = relationship("Transfer", secondary=itinerary_transfer)

Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    if not db.query(Hotel).first():
        db.add_all([
            Hotel(name="Goa Beach Resort", location="Goa"),
            Hotel(name="Manali Mountain Retreat", location="Manali")
        ])
        activities = [
            Activity(name="Scuba Diving", location="Goa"),
            Activity(name="Paragliding", location="Manali")
        ]
        transfers = [
            Transfer(from_location="Goa", to_location="Manali"),
            Transfer(from_location="Manali", to_location="Goa")
        ]
        db.add_all(activities)
        db.add_all(transfers)
        db.commit()
    db.close()
seed_db()

# Pydantic Schemas
class ItineraryCreate(BaseModel):
    name: str
    nights: int
    hotel_id: int
    activity_ids: List[int]
    transfer_ids: List[int]

class ItineraryOut(BaseModel):
    id: int
    name: str
    nights: int
    hotel: str
    activities: List[str]
    transfers: List[str]

    class Config:
        orm_mode = True

@app.post("/itineraries/", response_model=ItineraryOut)
def create_itinerary(data: ItineraryCreate):
    db = SessionLocal()
    hotel = db.get(Hotel, data.hotel_id)
    if not hotel:
        db.close()
        raise HTTPException(status_code=404, detail="Hotel not found")
    activities = db.query(Activity).filter(Activity.id.in_(data.activity_ids)).all()
    transfers = db.query(Transfer).filter(Transfer.id.in_(data.transfer_ids)).all()
    itinerary = Itinerary(
        name=data.name, nights=data.nights, hotel=hotel,
        activities=activities, transfers=transfers
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)
    result = ItineraryOut(
        id=itinerary.id,
        name=itinerary.name,
        nights=itinerary.nights,
        hotel=itinerary.hotel.name,
        activities=[a.name for a in itinerary.activities],
        transfers=[f"{t.from_location} -> {t.to_location}" for t in itinerary.transfers]
    )
    db.close()
    return result

@app.get("/itineraries/", response_model=List[ItineraryOut])
def get_itineraries():
    db = SessionLocal()
    itineraries = db.query(Itinerary).all()
    results = [
        ItineraryOut(
            id=i.id,
            name=i.name,
            nights=i.nights,
            hotel=i.hotel.name,
            activities=[a.name for a in i.activities],
            transfers=[f"{t.from_location} -> {t.to_location}" for t in i.transfers]
        ) for i in itineraries
    ]
    db.close()
    return results

@app.get("/mcp/{nights}", response_model=List[ItineraryOut])
def recommended_itineraries(nights: int):
    db = SessionLocal()
    itineraries = db.query(Itinerary).filter(Itinerary.nights == nights).all()
    results = [
        ItineraryOut(
            id=i.id,
            name=i.name,
            nights=i.nights,
            hotel=i.hotel.name,
            activities=[a.name for a in i.activities],
            transfers=[f"{t.from_location} -> {t.to_location}" for t in i.transfers]
        ) for i in itineraries
    ]
    db.close()
    return results
