####################################################################################################
# Define all types of tables here.
####################################################################################################

from textual.widgets import DataTable


class BaseAnalyticsTable(DataTable):
    
    """A table to display Base analytics."""

    def __init__(self, *args, **kwargs) -> None:
        self.table_data = kwargs.get("table_data", {})
        kwargs.pop("table_data", None)
        super().__init__(*args, **kwargs)
        self.populate_table()

    def populate_table(self) -> None:
        """Populate the table with the table data."""
        self.add_columns("Key", "Value")
        for key, value in self.table_data.items():
            self.add_row(key, value)
        self.border_title = "Base Analytics"


class PandasDataFrameTable(DataTable):
    
    """A table to display a pandas DataFrame."""

    def __init__(self, *args, **kwargs) -> None:
        self.df = kwargs.get("df", None)
        kwargs.pop("df", None)
        super().__init__(*args, **kwargs)
        self.populate_table()
    
    def populate_table(self) -> None:
        """Populate the table with the table data."""
        self.add_columns(*self.df.columns)
        for _, row in self.df.iterrows():
            self.add_row(*row.values)
        self.border_title = "Analytics"
    
    
