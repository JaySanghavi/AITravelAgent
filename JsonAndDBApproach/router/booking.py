from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.booking_service import book_ticket, get_booking_by_pnr, get_booking_by_id

router = APIRouter(tags=["Booking"])


# -------- Request Models --------

class Passenger(BaseModel):
    name: str
    age: int


class BookingRequest(BaseModel):
    from_city: str
    to_city: str
    date: str
    passengers: list[Passenger]


# -------- Routes --------

@router.post("/create")
async def create_booking(request: BookingRequest):

    try:
        result = await book_ticket(request.dict())
        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/id/{booking_id}")
async def get_booking_details_by_id(booking_id: str):

    try:
        result = await get_booking_by_id(booking_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/pnr/{pnr}")
async def get_booking_details_by_pnr(pnr: str):

    try:
        result = await get_booking_by_pnr(pnr)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )