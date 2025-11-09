import asyncio

from pyrail_uk.NationalRail import NationalRailClient
from pyrail_uk.service.types import TrainService, TrainStatus
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Label, Static
from textual.widgets._data_table import DataTable

import app.service.environment as env
from app.components.DeparturesTable import DeparturesTable
from app.components.shared.art import PYRAIL_LOGO
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


class LabelGroup(Horizontal):
    DEFAULT_CSS = """
    LabelGroup {
        width: 100%;
        height: 2;
        grid-size: 2 1;
        grid-rows: 40% 60%;
        text-wrap: wrap;
        text-overflow: fold
    }
    
    Label {
        text-wrap: wrap;
    }
    """

    def __init__(self, groupkey: str, label: str, value: str | None = None):
        super().__init__()
        self.groupkey = groupkey
        self.label = label
        self.value = value

    def compose(self):
        label_text = t(f"{self.groupkey}.{self.label}").upper()
        self.labelobj = Label(f"{label_text} : ", id=f"{self.groupkey}-{self.label}-label")
        self.labelobj.styles.text_style = "bold"
        yield self.labelobj

        yield Label(id=f"{self.groupkey}-{self.label}", shrink=True)


class TrainServiceSummaryBox(Vertical):
    DEFAULT_CSS = """
    TrainServiceSummaryBox {
        width: 100%;
        height: 100%;
        content-align: left top;
        border: solid yellow;
        padding: 2 5;
        margin: 2 2;
    }
    """

    def compose(self):
        groupkey = "trainSummary"
        yield LabelGroup(groupkey, "operator")
        yield LabelGroup(groupkey, "train-destination")
        yield LabelGroup(groupkey, "train-status")
        yield LabelGroup(groupkey, "train-status-reason")
        yield LabelGroup(groupkey, "train-departure-time")
        yield LabelGroup(groupkey, "train-arrival-time")


class DepartureInfoTableGroup(Horizontal):
    DEFAULT_CSS = """
    DepartureInfoTableGroup {
        width: 100%;
        layout: grid;
        grid-size: 1 3;
        grid-rows: 5% 20% 75%;
        padding: 3;
    }
    """

    def compose(self):
        self.table_header = DepartureInfoTableHeader()
        self.summary = TrainServiceSummaryBox()
        yield self.table_header
        yield DeparturesTable()
        yield self.summary

    def update_train_data(self, services: list[TrainService]):
        table = self.query_one(DeparturesTable)
        table.service_data = services

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        row = event.cursor_row
        table = self.query_one(DeparturesTable)
        service = table.service_data[row]

        self.query_one("#trainSummary-operator", Label).update(
            f"{service.operator} ({service.operator_code})"
        )
        self.query_one("#trainSummary-train-destination", Label).update(
            f"{service.train_destination} ({service.train_destination_crs})"
        )
        self.query_one("#trainSummary-train-status", Label).update(
            t(f"trainStatus.{service.status.value}").upper()
        )
        self.query_one("#trainSummary-train-status-reason", Label).update(
            service.status_reason or "No reason provided", layout=True
        )

        std = service.std
        std_suffix = (
            f" (Expected: {service.etd})"
            if service.etd not in ["On time", "Cancelled", "Delayed"]
            else f" ({service.etd})"
        )

        sta = service.sta or "N/A"
        sta_suffix = (
            f" (+ {service.arrival_mins_delayed} mins)" if service.arrival_mins_delayed else ""
        )

        self.query_one("#trainSummary-train-departure-time", Label).update(
            "Cancelled" if service.status == TrainStatus.CANCELLED else std + std_suffix
        )
        self.query_one("#trainSummary-train-arrival-time", Label).update(
            "Cancelled" if service.status == TrainStatus.CANCELLED else sta + sta_suffix
        )


class PyrailLogoWrapper(Vertical):
    DEFAULT_CSS = """
    PyrailLogoWrapper {
        width: 100%;
        height: auto;
        align-horizontal: center;
        align-vertical: middle;
        margin: 3;
    }
    """

    def compose(self):
        yield Static(PYRAIL_LOGO)
        yield Label("Copyright (C) of Christopher Khoo 2025")


class DepartureInfoRightWindow(Vertical):
    DEFAULT_CSS = """
    DepartureInfoRightWindow {
        width: 100%;
        layout: grid;
        grid-size: 1 2;
        grid-rows: 40% 60%;
        padding: 3;
    }
    """

    def compose(self):
        yield PyrailLogoWrapper()


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
        yield DepartureInfoRightWindow()

    async def on_mount(self):
        await self.load_train_data()
        self.set_interval(60, self.load_train_data)

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
