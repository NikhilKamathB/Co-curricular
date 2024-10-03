####################################################################################################
# Define workspace here.
####################################################################################################

import pandas as pd
from textual import on
from typing import Tuple
from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.widgets import Static, Button, Input
from textual.containers import Vertical, VerticalScroll
from eyepopai.core.pop import EyePop as pop
from eyepopai.core.constants import FileTypes
from eyepopai.components.query import FileInputQuery
from eyepopai.core.utils import get_file_type, view_video, view_image
from eyepopai.components.table import BaseAnalyticsTable, PandasDataFrameTable


class Workspace(Static):

    """A workspace widget that serves as the main work area interface."""

    BORDER_TITLE = "Workspace"
    INITIAL_DISPLAY_TEXT = "Your analysis will appear here.\nProcessing can take some time...\nYou can hit `q` to close any preview windows that pop up.\nTo close the CLI hit `ctrl+c`."
    INITIAL_DISPLAY_WIDGET = Static(
        INITIAL_DISPLAY_TEXT, id="workspace_inital_display")
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pop = pop()

    def _clear_and_return_msg_text_area(self) -> str:
        """Clear the text area and return the text in that area."""
        workspace_query_area = self.query_one("#workspace_query_area", Input)
        value = workspace_query_area.value
        workspace_query_area.value = ""
        return value
    
    def _process_file(self, file_path: str) -> Tuple[dict, pd.DataFrame]:
        """
            Process a file.
            Input:
                file_path (str): The path to the file.
            Returns:
                Tuple[dict, pd.DataFrame]: A tuple containing the stats and the detailed stats for frames.
        """
        file_type = get_file_type(file_path)
        pd_stats = None
        if file_type == FileTypes.VIDEO.value:
            res, pd_stats, stats = self.pop.process_video(file_path=file_path)
            view_video(file_path=res)
        elif file_type == FileTypes.IMAGE.value:
            res, stats = self.pop.process_image(file_path=file_path)
            view_image(file_path=res)
        stats["File Type"] = file_type
        stats["Output path"] = res
        return stats, pd_stats

    def _submit(self) -> None:
        """Submit a workspace query."""
        user_input = self._clear_and_return_msg_text_area()
        if not user_input:
            return
        workspace_display_area = self.query_one("#workspace_display_area", VerticalScroll)
        workspace_display_area.remove_children()
        workspace_display_area.styles.align = ("center", "middle")
        try:
            stats, pd_stats = self._process_file(file_path=user_input)
            if pd_stats is not None:
                res = VerticalScroll(
                    BaseAnalyticsTable(table_data=stats),
                    PandasDataFrameTable(df=pd_stats)
                )
            else:
                res = VerticalScroll(
                    BaseAnalyticsTable(table_data=stats),
                )
        except FileNotFoundError as fnfe:
            res = Static(str(fnfe))
        except RuntimeError as re:
            res = Static(str(re))
        except Exception as e:
            res = Static(str(e))
        workspace_display_area.mount(res)
    
    def _reset(self) -> None:
        """Reset the workspace."""
        try:
            _ = self.query_one("#workspace_inital_display", Static)
            self._clear_and_return_msg_text_area()
            return
        except NoMatches:
            pass
        workspace_display_area = self.query_one(
            "#workspace_display_area", VerticalScroll)
        workspace_display_area.remove_children()
        workspace_display_area.styles.align = ("center", "middle")
        workspace_display_area.mount(self.INITIAL_DISPLAY_WIDGET)

    def compose(self) -> ComposeResult:
        yield Vertical(
            VerticalScroll(
                self.INITIAL_DISPLAY_WIDGET,
                id="workspace_display_area"
            ),
            FileInputQuery()
        )
        
    @on(Button.Pressed, "#workspace_submit_button")
    def submit_button_pressed(self, event: Button.Pressed) -> None:
        self._submit()
    
    @on(Button.Pressed, "#workspace_clear_button")
    def clear_button_pressed(self, event: Button.Pressed) -> None:
        self._reset()