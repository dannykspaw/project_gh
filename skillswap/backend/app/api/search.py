from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..services.geo import nearby_profiles
from ..security import get_current_user_id
from typing import Optional

router = APIRouter(prefix="/search", tags=["search"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/nearby")
def nearby(lat: float, lon: float, radius_km: float = 50.0, skill: Optional[str] = None, db: Session = Depends(get_db)):
    return nearby_profiles(db, lat, lon, radius_km, skill)
