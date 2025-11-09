import asyncio

from pyrail_uk.NationalRail import NationalRailClient
from pyrail_uk.service.types import TrainService, TrainStatus
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

import app.service.environment as env
from app.components.DeparturesTable import DeparturesTable
from app.locales.locales import t
from app.service.DepartureManager import DepartureManager


class DepartureInfoTableHeader(Static):
    DEFAULT_CSS = """
    DepartureInfoTableHeader {
        color: white;
        text-align: left;
        height: 3;             /* box height in rows */
        content-align: left middle; /* center text vertically, align left horizontally */
        text-style: bold;
        padding: 0 2;
        width: 100%;
    }
    """

    dep_crs = reactive("")
    arr_crs = reactive("")

    def __init__(self, **kwargs):
        super().__init__()

    def watch_dep_crs(self, value: str) -> None:
        """Called automatically when dep_crs changes."""
        self.update_message()

    def watch_arr_crs(self, value: str) -> None:
        """Called automatically when arr_crs changes."""
        self.update_message()

    def update_message(self):
        """Update the text content based on the current CRS values."""
        if self.dep_crs or self.arr_crs:
            self.update(f"🚄 Train services from {self.dep_crs} to {self.arr_crs}")
        else:
            self.update("🚄 Awaiting station info...")


class DepartureInfoTableGroup(Vertical):
    DEFAULT_CSS = """
    DepartureInfoTableGroup {
        padding: 3;
        height: auto;
    }
    """

    def compose(self):
        self.table_header = DepartureInfoTableHeader()
        yield self.table_header
        yield DeparturesTable()

    def update_train_data(self, services: list[TrainService]):
        table = self.query_one(DeparturesTable)
        table.service_data = services


class DeparturesInfoContent(Horizontal):
    DEFAULT_CSS = """
    DeparturesInfoContent {
        width: 100%;
        layout: grid;
        grid-size: 2 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.manager = DepartureManager()

    def compose(self):
        self.departure_info_table_group = DepartureInfoTableGroup()
        yield self.departure_info_table_group
        yield Static("Hello world!")

    async def on_mount(self):
        await self.load_train_data()
        self.set_interval(30, self.load_train_data)

    async def load_train_data(self):
        departure_data = await self.manager.get_departure_data()
        self.departure_info_table_group.update_train_data(departure_data.services)
        self.departure_info_table_group.table_header.dep_crs = self.manager.dep_crs or ""
        self.departure_info_table_group.table_header.arr_crs = self.manager.arr_crs or ""


class DeparturesInfo(Vertical):
    DEFAULT_CSS = """
    DeparturesInfo {
        width: 100%;
        height: 100%;
        align-horizontal: center;
        align-vertical: middle;
    }
    """

    def compose(self):
        yield DeparturesInfoContent()
