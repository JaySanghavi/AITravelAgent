import uuid
import time
from services.storage import read_bookings, write_bookings


def generate_id(length=12):
    return uuid.uuid4().hex[:length]


async def book_ticket(request_data: dict):

    bookings = await read_bookings()

    # Ensure unique PNR
    existing_pnrs = {b["pnr"] for b in bookings}

    pnr = generate_id(8)
    while pnr in existing_pnrs:
        pnr = generate_id(8)

    booking = {
        "id": generate_id(12),
        "pnr": pnr,
        "from": request_data["from_city"],
        "to": request_data["to_city"],
        "date": request_data["date"],
        "passengers": request_data["passengers"],
        "timestamp": time.time(),
        "status": "confirmed"
    }

    bookings.append(booking)
    await write_bookings(bookings)

    return booking


async def get_booking_by_id(booking_id: str):

    bookings = await read_bookings()

    return next(
        (b for b in bookings if b["id"] == booking_id),
        None
    )

async def get_booking_by_pnr(booking_id: str):

    bookings = await read_bookings()

    return next(
        (b for b in bookings if b["pnr"] == booking_id),
        None
    )