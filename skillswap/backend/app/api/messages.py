from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models, schemas
from ..security import get_current_user_id

router = APIRouter(prefix="/messages", tags=["messages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def send_message(payload: schemas.MessageIn, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    msg = models.Message(sender_id=user_id, receiver_id=payload.receiver_id, content=payload.content)
    db.add(msg)
    db.commit()
    return {"ok": True}
