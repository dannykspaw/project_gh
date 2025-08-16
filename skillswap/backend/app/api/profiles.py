from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models, schemas
from ..security import get_current_user_id

router = APIRouter(prefix="/profiles", tags=["profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=schemas.ProfileOut)
def me(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    prof = db.query(models.Profile).filter(models.Profile.user_id==user_id).first()
    if not prof:
        raise HTTPException(404, "Profile not found")
    return prof

@router.put("/me", response_model=schemas.ProfileOut)
def update_me(payload: schemas.ProfileIn, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    prof = db.query(models.Profile).filter(models.Profile.user_id==user_id).first()
    if not prof:
        raise HTTPException(404, "Profile not found")
    for k, v in payload.model_dump().items():
        if hasattr(prof, k) and v is not None and k not in ("skills",):
            setattr(prof, k, v)
    # skills
    if payload.skills is not None:
        # ensure skills exist
        skill_objs = []
        for name in payload.skills:
            s = db.query(models.Skill).filter(models.Skill.name.ilike(name)).first()
            if not s:
                s = models.Skill(name=name)
                db.add(s)
                db.flush()
            skill_objs.append(s)
        prof.skills = skill_objs
    db.commit()
    db.refresh(prof)
    return prof
