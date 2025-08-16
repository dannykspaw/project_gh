from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..security import get_current_user_id, auth_scheme
from typing import Dict, Set
import jwt
from ..core.config import settings

router = APIRouter()

active: Dict[int, Set[WebSocket]] = {}

def decode_user_id(token: str) -> int:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return int(payload["sub"])

@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close()
        return
    try:
        user_id = decode_user_id(token)
    except Exception:
        await websocket.close()
        return
    await websocket.accept()
    active.setdefault(user_id, set()).add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            to = int(data.get("to"))
            msg = data.get("message", "")
            # relay to receiver if connected
            if to in active:
                for ws in list(active[to]):
                    await ws.send_json({"from": user_id, "message": msg})
    except WebSocketDisconnect:
        pass
    finally:
        active[user_id].discard(websocket)
