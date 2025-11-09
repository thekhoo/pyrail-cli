from typing import Iterable, Sequence

from pyrail_uk.service.types import TrainService, TrainStatus
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable

from app.locales.locales import t


class DeparturesTable(DataTable):
    DEFAULT_CSS = """
    DeparturesTable {
        width: 100%    
    }
    
    DataTable > .datatable--cell {
        padding-top: 1;
        padding-bottom: 1;
    }
    """

    service_data: reactive[list[TrainService]] = reactive([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_columns(
            "STD", "Status", "ETD", "Operator", "Destination", "Platform", "STA", "ETA"
        )

        self.zebra_stripes = True
        self.cursor_type = "row"
        self.focus()

    def watch_service_data(self, old_service_data, new_service_data):
        self.update_table()

    def parse_row(self, row: TrainService) -> list[str | None]:
        etd = row.std if row.status == TrainStatus.ON_TIME else row.etd
        etd_suffix = f" (+ {row.departure_mins_delayed} mins)" if row.departure_mins_delayed else ""

        eta = row.eta or ""
        eta_suffix = f" (+ {row.arrival_mins_delayed} mins)" if row.arrival_mins_delayed else ""

        return [
            row.std,
            t(f"trainStatus.{row.status.value}"),
            etd + etd_suffix,
            row.operator_code,
            row.train_destination,
            row.platform,
            row.sta,
            eta + eta_suffix,
        ]

    def update_table(self):
        self.clear()

        rows = [self.parse_row(service) for service in self.service_data]
        self.add_rows(rows)
