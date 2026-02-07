import json
import asyncio
from pathlib import Path

BOOKINGS_FILE = Path("data/bookings.json")

# Prevent race conditions
lock = asyncio.Lock()


async def read_bookings():
    async with lock:
        if not BOOKINGS_FILE.exists():
            return []

        with open(BOOKINGS_FILE, "r") as f:
            return json.load(f)


async def write_bookings(data):
    async with lock:
        with open(BOOKINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
