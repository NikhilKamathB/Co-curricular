####################################################################################################
# Define all types of tables here.
####################################################################################################

import logging
from textual.widgets import DataTable


logger = logging.getLogger(__name__)


class BaseAnalyticsTable(DataTable):
    
    """A table to display Base analytics."""

    __LOG_PREFIX__ = "BaseAnalyticsTable"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the base analytics table."""
        logger.info(f"{self.__LOG_PREFIX__}: Initializing base analytics table.")
        self.table_data = kwargs.get("table_data", {})
        kwargs.pop("table_data", None)
        super().__init__(*args, **kwargs)
        self.populate_table()

    def populate_table(self) -> None:
        """Populate the table with the table data."""
        logger.info(f"{self.__LOG_PREFIX__}: Populating base analytics table.")
        self.add_columns("Key", "Value")
        for key, value in self.table_data.items():
            self.add_row(key, value)
        self.border_title = "Base Analytics"


class PandasDataFrameTable(DataTable):
    
    """A table to display a pandas DataFrame."""

    __LOG_PREFIX__ = "PandasDataFrameTable"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the pandas DataFrame table."""
        logger.info(f"{self.__LOG_PREFIX__}: Initializing pandas DataFrame table.")
        self.df = kwargs.get("df", None)
        kwargs.pop("df", None)
        super().__init__(*args, **kwargs)
        self.populate_table()
    
    def populate_table(self) -> None:
        """Populate the table with the table data."""
        logger.info(f"{self.__LOG_PREFIX__}: Populating pandas DataFrame table.")
        self.add_columns(*self.df.columns)
        for _, row in self.df.iterrows():
            self.add_row(*row.values)
        self.border_title = "Analytics"
    
    
