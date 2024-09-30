####################################################################################################
# Define workspace here.
####################################################################################################

from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.widgets import Static, Button, Input
from textual.containers import Vertical, VerticalScroll
from src.components.query import FileInputQuery


class Workspace(Static):

    """A workspace widget that serves as the main work area interface."""

    BORDER_TITLE = "Workspace"
    INITIAL_DISPLAY_TEXT = "Your analysis will appear here."
    INITIAL_DISPLAY_WIDGET = Static(
        INITIAL_DISPLAY_TEXT, id="workspace_inital_display")

    def _clear_and_return_msg_text_area(self) -> str:
        """Clear the text area and return the text in that area."""
        workspace_query_area = self.query_one("#workspace_query_area", Input)
        value = workspace_query_area.value
        workspace_query_area.value = ""
        return value
    
    def _submit(self) -> None:
        """Submit a workspace query."""
        user_input = self._clear_and_return_msg_text_area()
        if not user_input:
            return
        workspace_display_area = self.query_one(
            "#workspace_display_area", VerticalScroll)
        workspace_display_area.remove_children()
        workspace_display_area.styles.align = ("center", "middle")
        workspace_display_area.mount(
            Static(user_input)
        )
    
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "workspace_clear_button":
            self._reset()
        elif event.button.id == "workspace_submit_button":
            self._submit()