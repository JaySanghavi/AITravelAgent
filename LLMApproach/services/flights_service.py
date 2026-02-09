import requests
import os
from amadeus import Client, ResponseError
from auth_service import generate_token

amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)

BASE_URL = "https://test.api.amadeus.com"


def get_flight_schedule( carrier, number, date):

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


async def search_emirates_flights(origin, destination):

    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            adults=1
        )

        flights = []

        for offer in response.data:
            airline = offer["validatingAirlineCodes"][0]

            # Emirates airline code = EK
            if airline == "EK":
                flights.append({
                    "airline": airline,
                    "price": offer["price"]["total"],
                    "route": f"{origin} → {destination}"
                })

        return flights

    except ResponseError as e:
        return {"error": str(e)}
