import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from .models import *
from django.contrib import admin


class BostonHousePriceDatasetAdmin(admin.ModelAdmin):
    
    list_display = ["id", "crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "price"]

    def changelist_view(self, request, extra_context=None):
        df = pd.DataFrame.from_records(BostonHousePriceDataset.objects.all().values_list("crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "price", "created_at"))
        df.columns = self.list_display[1: ] + ["created_at"]
        df.drop("created_at", inplace=True, axis=1)
        corr = df.drop("price", axis=1).corr()

        fig = make_subplots(
                rows=1,
                cols=2,
                specs=[
                        [{"colspan": 1}, {"colspan": 1}]
                    ],
                subplot_titles=("Price Distribution", "Correlation between attributes")
            )
        fig.add_trace(go.Histogram(x=df["price"]), row=1, col=1)
        fig.add_trace(go.Heatmap({'x': corr.index.values, 'y': corr.columns.values, 'z': corr.values}), row=1, col=2)

        fig.update_layout(height=500, title_text="EDA on Boston House Price Prediction Dataset")
        plot = pio.to_html(fig, full_html=False)
        extra_context = extra_context or {"plot": plot}
        return super().changelist_view(request, extra_context=extra_context)



admin.site.register(BostonHousePriceDataset, BostonHousePriceDatasetAdmin)