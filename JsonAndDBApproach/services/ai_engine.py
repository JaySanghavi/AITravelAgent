from services.booking_service import book_ticket, get_booking_by_id
from services.pnr_service import get_pnr_status
import re
import json

with open("data/faq.json") as f:
    FAQ = json.load(f)

def search_faq(message: str):

    message = message.lower()

    for item in FAQ:
        for q in item["questions"]:
            if q in message:
                return item["answer"]

    return None

async def handle_message(message: str):

    message = message.lower()

    if "book" in message:
        return await book_ticket(message)

    if any(word in message for word in ["booking_id", "bookingid"]):
        match = re.search(r"\b[a-zA-Z0-9]{6,}\b", message)
        if match:
            return await get_booking_by_id(match.group())

    if "pnr" in message:
        pnr = message.split()[-1]
        return await get_pnr_status(pnr)

    response = search_faq(message)

    return "Hi! I'm FlyHigh ✈️ How can I help you today?" if response is None else response
