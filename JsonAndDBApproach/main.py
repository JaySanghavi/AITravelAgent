from fastapi import FastAPI
from routers import chat, booking, pnr

app = FastAPI(title="FlyHigh AI Travel Assistant")

app.include_router(chat.router, prefix="/chat")
app.include_router(booking.router, prefix="/booking")
app.include_router(pnr.router, prefix="/pnr")
