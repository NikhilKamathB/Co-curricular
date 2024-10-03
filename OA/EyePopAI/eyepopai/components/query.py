####################################################################################################
# Define all types of query widgets here.
####################################################################################################

import logging
from textual.app import ComposeResult
from textual.widgets import Static, Button, Input
from textual.containers import Horizontal, Vertical


logger = logging.getLogger(__name__)


class FileInputQuery(Static):

    """A file input widget that takes file path from the user."""

    BORDER_TITLE = "Enter your file path here..."
    UPLOAD_TYPE_OPTIONS = [("Local", "Local"), ("Web", "Web")]
    SELECTED_UPLOAD_TYPE = UPLOAD_TYPE_OPTIONS[0][0]
    __LOG_PREFIX__ = "FileInputQuery"

    def __init__(self, *args, **kwargs):
        """Initialize the file input query."""
        logger.info(f"{self.__LOG_PREFIX__}: Initializing file input query.")
        super().__init__(*args, **kwargs)
        self.selected_upload_type = self.SELECTED_UPLOAD_TYPE

    def compose(self) -> ComposeResult:
        logger.info(f"{self.__LOG_PREFIX__}: Composing file input query.")
        self.workspace_query_area = Input(id="workspace_query_area", placeholder="../data/videos/demo.mp4")
        yield Vertical(
            Horizontal(
                self.workspace_query_area,
            ),
            Horizontal(
                Button("Clear", id="workspace_clear_button"),
                Button("Submit", id="workspace_submit_button")
            )
        )
    
    def on_mount(self) -> None:
        logger.info(f"{self.__LOG_PREFIX__}: Mounting file input query.")
        self.workspace_query_area.border_title = self.BORDER_TITLE
