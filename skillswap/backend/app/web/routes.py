from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..core.config import settings
from ..security import create_access_token
from ..db import SessionLocal
from .. import models
from ..services.geo import nearby_profiles

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="web/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/web/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/web/login")
def login(email: str = Form(...), password: str = Form(...)):
    # Demo: always issues a token (replace with real auth or call /auth/login)
    # WARNING: For demo only
    token = create_access_token("1")
    return {"token": token}

@router.get("/web/profile", response_class=HTMLResponse)
def profile_form(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.put("/web/profile")
def profile_update(
    display_name: str = Form(None),
    bio: str = Form(None),
    lat: float = Form(None),
    lon: float = Form(None),
    is_mentor: bool = Form(False),
    skills: str = Form(""),
):
    db = SessionLocal()
    try:
        user = db.query(models.User).first()
        if not user:
            user = models.User(email="demo@example.com", hashed_password="demo")
            db.add(user); db.commit(); db.refresh(user)
            prof = models.Profile(user_id=user.id)
            db.add(prof); db.commit()
        prof = db.query(models.Profile).filter(models.Profile.user_id==user.id).first()
        prof.display_name = display_name or prof.display_name
        prof.bio = bio or prof.bio
        prof.lat = lat or prof.lat
        prof.lon = lon or prof.lon
        prof.is_mentor = is_mentor
        # skills
        names = [s.strip() for s in (skills or "").split(",") if s.strip()]
        skill_objs = []
        for name in names:
            s = db.query(models.Skill).filter(models.Skill.name.ilike(name)).first()
            if not s:
                s = models.Skill(name=name)
                db.add(s); db.flush()
            skill_objs.append(s)
        if skill_objs:
            prof.skills = skill_objs
        db.commit()
        return {"ok": True}
    finally:
        db.close()

@router.get("/web/nearby", response_class=HTMLResponse)
def nearby(request: Request, lat: float = None, lon: float = None, radius_km: float = 50, skill: str | None = None):
    lat = lat or settings.MAP_DEFAULT_LAT
    lon = lon or settings.MAP_DEFAULT_LON
    db = SessionLocal()
    try:
        results = nearby_profiles(db, lat, lon, radius_km, skill)
    finally:
        db.close()
    return templates.TemplateResponse("nearby.html", {"request": request, "lat": lat, "lon": lon, "results": results})
