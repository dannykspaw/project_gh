from sqlalchemy import text
from sqlalchemy.orm import Session

# Uses PostGIS if available (ST_DWithin); falls back to Haversine if not.

def nearby_profiles(db: Session, lat: float, lon: float, radius_km: float = 50.0, skill: str | None = None):
    try:
        # PostGIS path
        query = '''
        SELECT p.*, u.id as user_id FROM profiles p
        JOIN users u ON u.id = p.user_id
        {skill_join}
        WHERE p.lat IS NOT NULL AND p.lon IS NOT NULL
        AND ST_DWithin(
            ST_SetSRID(ST_MakePoint(p.lon, p.lat), 4326)::geography,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
            :meters
        )
        '''
        skill_join = ""
        params = {"lat": lat, "lon": lon, "meters": radius_km*1000}
        if skill:
            skill_join = "JOIN user_skills us ON us.user_id = u.id JOIN skills s ON s.id = us.skill_id AND LOWER(s.name)=LOWER(:skill)"
            query = query.format(skill_join=skill_join)
            params["skill"] = skill
        else:
            query = query.format(skill_join="")
        res = db.execute(text(query), params)
        return [dict(r._mapping) for r in res]
    except Exception:
        # Fallback Haversine
        haversine = '''
        SELECT p.*, u.id as user_id,
        6371 * acos(
            cos(radians(:lat)) * cos(radians(p.lat)) * cos(radians(p.lon) - radians(:lon)) +
            sin(radians(:lat)) * sin(radians(p.lat))
        ) AS distance_km
        FROM profiles p
        JOIN users u ON u.id = p.user_id
        {skill_join}
        WHERE p.lat IS NOT NULL AND p.lon IS NOT NULL
        HAVING distance_km < :radius
        ORDER BY distance_km ASC
        '''
        skill_join = ""
        params = {"lat": lat, "lon": lon, "radius": radius_km}
        if skill:
            skill_join = "JOIN user_skills us ON us.user_id = u.id JOIN skills s ON s.id = us.skill_id AND LOWER(s.name)=LOWER(:skill)"
            haversine = haversine.format(skill_join=skill_join)
            params["skill"] = skill
        else:
            haversine = haversine.format(skill_join="")
        res = db.execute(text(haversine), params)
        return [dict(r._mapping) for r in res]
