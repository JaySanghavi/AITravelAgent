import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from services.booking_service import book_ticket, get_booking_by_pnr, get_booking_by_id

from services.flights_service import get_flight_schedule

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("data/faq.json") as f:
    FAQ = json.load(f)


tools = [
    {
        "type": "function",
        "function": {
            "name": "book_ticket",
            "description": "Book a flight ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_city": {"type": "string"},
                    "to_city": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": ["from_city", "to_city", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_by_pnr",
            "description": "Get booking details by PNR",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {"type": "string"}
                },
                "required": ["pnr"]
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "get_booking_by_id",
            "description": "Get booking details by Booking ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"}
                },
                "required": ["id"]
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "get_flight_schedule",
            "description": "Fetch flight schedule from Amadeus",
            "parameters": {
                "type": "object",
                "properties": {
                    "carrierCode": {"type": "string"},
                    "flightNumber": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": [
                    "carrierCode",
                    "flightNumber",
                    "date"
                ]
            }
        }
    }
]


async def handle_message(message: str):

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": "You are FlyHigh, an airline booking assistant."
            },
            {"role": "user", "content": message}
        ],
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:

        tool = msg.tool_calls[0]
        args = json.loads(tool.function.arguments)

        if tool.function.name == "book_ticket":
            result = await book_ticket(args)
        elif tool.function.name == "get_booking_by_id":
            result = await get_booking_by_id(args["id"])
        elif tool.function.name == "get_booking_by_pnr":
            result = await get_booking_by_pnr(args["pnr"])
        else tool.function.name == "get_flight_schedule":
            result = await get_flight_schedule(args["carrierCode"],args["flightNumber"],args["date"])

        return result

    # fallback to FAQ
    for item in FAQ:
        if item["question"] in message.lower():
            return item["answer"]

    return msg.content
