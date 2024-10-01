####################################################################################################
# Define all types of query widgets here.
####################################################################################################

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, Input, Select


class FileInputQuery(Static):

    """A file input widget that takes file path from the user."""

    BORDER_TITLE = "Enter your file path here..."
    UPLOAD_TYPE_OPTIONS = [("Local", "Local"), ("Web", "Web")]
    SELECTED_UPLOAD_TYPE = UPLOAD_TYPE_OPTIONS[0][0]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_upload_type = self.SELECTED_UPLOAD_TYPE

    def compose(self) -> ComposeResult:
        self.workspace_query_area = Input(id="workspace_query_area", placeholder="./data/videos/demo.mp4")
        self.upload_type_select = Select(id="upload_type_select", options=self.UPLOAD_TYPE_OPTIONS, allow_blank=False, value=self.SELECTED_UPLOAD_TYPE)
        yield Vertical(
            Horizontal(
                self.workspace_query_area,
                self.upload_type_select,
            ),
            Horizontal(
                Button("Clear", id="workspace_clear_button"),
                Button("Submit", id="workspace_submit_button")
            )
        )
    
    def on_mount(self) -> None:
        self.workspace_query_area.border_title = self.BORDER_TITLE
    
    @on(Select.Changed, "#upload_type_select")
    def select_changed(self, event: Select.Changed) -> None:
        self.selected_upload_type = event.value