from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models, schemas
from ..security import get_current_user_id

router = APIRouter(prefix="/ratings", tags=["ratings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def rate(payload: schemas.RatingIn, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    if payload.ratee_id == user_id:
        raise HTTPException(400, "Cannot rate yourself")
    rating = models.Rating(rater_id=user_id, ratee_id=payload.ratee_id, stars=payload.stars, comment=payload.comment)
    db.add(rating)
    db.commit()
    return {"ok": True}
