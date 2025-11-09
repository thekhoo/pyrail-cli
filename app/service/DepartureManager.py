import asyncio

from pyrail_uk import DepartureBoardClient
from pyrail_uk.NationalRail import NationalRailClient

import app.service.environment as env


class DepartureManager:
    def __init__(self):
        self.client = DepartureBoardClient(token=env.get_departure_token())  # pyrefly: ignore

        self.dep_crs = env.get_origin()
        self.arr_crs = env.get_destination()

    async def get_departure_data(self):
        return await asyncio.to_thread(
            self.client.get_trains,
            dep_crs=env.get_origin(),  # pyrefly: ignore
            arr_crs=env.get_destination(),
        )
