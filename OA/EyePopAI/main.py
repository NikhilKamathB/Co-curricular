####################################################################################################
# This file serves as the starting point for the application - drive code
# How to run the application: `python -m main`
####################################################################################################

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from src.components.workspace import Workspace


class EyePopAI(App):
     
    """
    EyePopAI is the drive class for the application.
    This application allows you to process a video feed and give statistics about differnet objects in the video feed.
    """

    TITLE = "EyePopAI"
    CSS_PATH = "./tcss/eyepopai.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Workspace()
        yield Footer()

if __name__ == "__main__":
    EyePopAI().run()