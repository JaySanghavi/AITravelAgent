from services.storage import read_bookings


async def get_pnr_status(pnr: str):

    bookings = await read_bookings()

    for booking in bookings:
        if booking["pnr"] == pnr:
            return booking

    return None
