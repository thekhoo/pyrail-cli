import asyncio

from pyrail_uk.NationalRail import NationalRailClient
from textual.app import App, ComposeResult, RenderResult
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Footer, Header

import app.service.environment as env
from app.components import DeparturesInfo, DeparturesTable

DEPARTURE_STATION = "RDG"
ARRIVAL_STATION = "OXF"


class PyrailApp(App):
    BINDINGS = [
        ("o", "set_origin", "Set the Origin Station"),
        ("d", "set_destination", "Set the Destination Station"),
        ("r", "refresh", "Refresh the departure data"),
        ("q", "quit", "Quit the Application"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DeparturesInfo()
        yield Footer()


def run():
    app = PyrailApp()
    app.run()


if __name__ == "__main__":
    app = PyrailApp()
    app.run()
