import typing as t

import cloup
from pyrail_uk.NationalRail import NationalRailClient


@cloup.group()
def pyrail():
    pass


@pyrail.command()
def hello():
    print("hello from pyrail cli!")


@pyrail.command(name="station")
def station():
    pass


@pyrail.command(name="trains")
def trains(departure_crs: str, arrival_crs: t.Optional[str] = None):
    client = NationalRailClient()
    client.get_trains()


@pyrail.command(name="departure-board")
def departure_board():
    pass
