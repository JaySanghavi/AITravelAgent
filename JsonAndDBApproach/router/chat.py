from fastapi import APIRouter
from services.ai_engine import handle_message

router = APIRouter(tags=['Chat'])

@router.post("/")
async def chat(message: dict):
    response = await handle_message(message["text"])
    return {"reply": response}
