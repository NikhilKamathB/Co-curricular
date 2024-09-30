####################################################################################################
# Define all types of query widgets here.
####################################################################################################

from textual.app import ComposeResult
from textual.widgets import Static, Button, Input
from textual.containers import Horizontal, Vertical


class FileInputQuery(Static):

    """A file input widget that takes file path from the user."""

    BORDER_TITLE = "Enter your file path here..."

    def on_mount(self) -> None:
        self.workspace_query_area.border_title = self.BORDER_TITLE

    def compose(self) -> ComposeResult:
        self.workspace_query_area = Input(id="workspace_query_area", placeholder="./data/videos/demo.mp4")
        yield Vertical(
            self.workspace_query_area,
            Horizontal(
                Button("Clear", id="workspace_clear_button"),
                Button("Submit", id="workspace_submit_button")
            )
        )
