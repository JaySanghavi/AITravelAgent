import requests
import os
import asyncio
from amadeus import Client, ResponseError
from auth_service import generate_token

load_dotenv()

amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)

BASE_URL = "https://test.api.amadeus.com"


def get_flight_schedule(carrier, number, date):

    url = f"{BASE_URL}/v2/schedule/flights"
    token = generate_token()
    params = {
        "carrierCode": carrier,
        "flightNumber": number,
        "scheduledDepartureDate": date
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/vnd.amadeus+json"
    }

    response = requests.get(url, params=params, headers=headers)

    return response.json()


async def search_emirates_flights(origin, destination, date):

    try:
        loop = asyncio.get_running_loop()

        response = await loop.run_in_executor(
            None,
            lambda: amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=date,
                adults=1
            )
        )

        flights = []

        for offer in response.data:
            airline = offer["validatingAirlineCodes"][0]
            if airline == "EK":
                segment = offer["itineraries"][0]["segments"][0]
                flights.append({
                    "flight": f"{segment['carrierCode']}{segment['number']}",
                    "departure": segment["departure"]["at"],
                    "arrival": segment["arrival"]["at"],
                    "price": offer["price"]["total"],
                    "route": f"{origin} → {destination}"
                })

        return flights or {"message": "No Emirates flights found"}

    except ResponseError as e:
        return {"error": str(e)}
