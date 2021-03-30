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
        rad_df = df.groupby("rad").crim.agg("count").to_frame("count").reset_index()
        chas_df = df.groupby("chas").crim.agg("count").to_frame("count").reset_index()

        fig = make_subplots(
                rows=3,
                cols=2,
                specs=[
                        [{}, {}],
                        [{}, {}],
                        [{}, {}]
                    ],
                subplot_titles=("Price Distribution", "Correlation between attributes",
                                "Count of Rad values", "Count of Chas feature",
                                "Distribution of housing prices w.r.t LSTAT", "Distribution of housing prices w.r.t RM")
            )
        fig.add_trace(go.Histogram(x=df["price"], marker=dict(color="cornflowerblue")), row=1, col=1)
        fig.add_trace(go.Heatmap({'x': corr.index.values, 'y': corr.columns.values, 'z': corr.values}, colorbar=dict(y=.9,len=.3), colorscale=[[0, 'cornflowerblue'], [1, 'white']]), row=1, col=2)
        fig.add_trace(go.Bar(x=rad_df["rad"], y=rad_df["count"], marker=dict(color="cornflowerblue")), row=2, col=1)
        fig.add_trace(go.Bar(x=chas_df["chas"], y=chas_df["count"], marker=dict(color="cornflowerblue")), row=2, col=2)
        fig.add_trace(go.Scatter(x=df["lstat"], y=df["price"], mode = 'markers', marker=dict(color="cornflowerblue")), row=3, col=1)
        fig.add_trace(go.Scatter(x=df["rm"], y=df["price"], mode = 'markers', marker=dict(color="cornflowerblue")), row=3, col=2)

        fig['layout']['xaxis']['title']='Price'
        fig['layout']['xaxis3']['title']='Rad'
        fig['layout']['xaxis4']['title']='Chas'
        fig['layout']['xaxis5']['title']='LSTAT'
        fig['layout']['xaxis6']['title']='RM'
        fig['layout']['yaxis']['title']='Count'
        fig['layout']['yaxis3']['title']='Count'
        fig['layout']['yaxis4']['title']='Count'
        fig['layout']['yaxis5']['title']='House prices in $1000'
        fig['layout']['yaxis6']['title']='House prices in $1000'
        fig.update_traces(colorbar_thickness=10, selector=dict(type='heatmap'))
        fig.update_layout(height=1000, title_text="EDA on Boston House Price Prediction Dataset", bargap=0.30, showlegend=False)
        plot = pio.to_html(fig, full_html=False)

        extra_context = extra_context or {"plot": plot}
        return super().changelist_view(request, extra_context=extra_context)



admin.site.register(BostonHousePriceDataset, BostonHousePriceDatasetAdmin)