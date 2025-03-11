from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import HouseModel

app = FastAPI()


class House(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: float
    median_house_value: float
    ocean_proximity: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/houses")
def get_houses(db: Session = Depends(get_db)):
    houses = db.query(HouseModel).all()
    return houses

@app.post("/houses")
def add_house(house: House, db: Session = Depends(get_db)):
    new_house = HouseModel(
        longitude=house.longitude,
        latitude=house.latitude,
        housing_median_age=house.housing_median_age,
        total_rooms=house.total_rooms,
        total_bedrooms=house.total_bedrooms,
        population=house.population,
        households=house.households,
        median_income=house.median_income,
        median_house_value=house.median_house_value,
        ocean_proximity=house.ocean_proximity
    )
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return {"message": "House added", "house": new_house}