import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from .models import *
from django.contrib import admin
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error


class BostonHousePriceDatasetAdmin(admin.ModelAdmin):
    
    test_size = 0.2
    random_state = 42
    list_display = ["id", "crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "price"]

    def changelist_view(self, request, extra_context=None):
        df = pd.DataFrame.from_records(BostonHousePriceDataset.objects.all().values_list("crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "price", "created_at"))
        df.columns = self.list_display[1: ] + ["created_at"]
        df.drop("created_at", inplace=True, axis=1)
        corr = df.drop("price", axis=1).corr()
        rad_df = df.groupby("rad").crim.agg("count").to_frame("count").reset_index()
        chas_df = df.groupby("chas").crim.agg("count").to_frame("count").reset_index()

        fig = make_subplots(
                rows=4,
                cols=2,
                specs=[
                        [{}, {}],
                        [{}, {}],
                        [{}, {}],
                        [{"colspan": 2}, None],
                    ],
                subplot_titles=("Price Distribution", "Correlation between attributes",
                                "Count of Rad values", "Count of Chas feature",
                                "Distribution of housing prices w.r.t LSTAT", "Distribution of housing prices w.r.t RM",
                                "Actual value vs predicted value over average number of rooms per dwelling",
                                "Actual value vs predicted value over all attributes")
            )
        fig.add_trace(go.Histogram(x=df["price"], marker=dict(color="cornflowerblue")), row=1, col=1)
        fig.add_trace(go.Heatmap({'x': corr.index.values, 'y': corr.columns.values, 'z': corr.values}, colorbar=dict(y=.92,len=.2), colorscale=[[0, "cornflowerblue"], [1, "white"]]), row=1, col=2)
        fig.add_trace(go.Bar(x=rad_df["rad"], y=rad_df["count"], marker=dict(color="cornflowerblue")), row=2, col=1)
        fig.add_trace(go.Bar(x=chas_df["chas"], y=chas_df["count"], marker=dict(color="cornflowerblue")), row=2, col=2)
        fig.add_trace(go.Scatter(x=df["lstat"], y=df["price"], mode = "markers", marker=dict(color="cornflowerblue")), row=3, col=1)
        fig.add_trace(go.Scatter(x=df["rm"], y=df["price"], mode = "markers", marker=dict(color="cornflowerblue")), row=3, col=2)

        X = df.drop("price", axis = 1)
        Y = df["price"]
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=self.test_size, random_state=self.random_state)
        lr = LinearRegression()
        lr.fit(X_train, Y_train)
        Y_train_predict = lr.predict(X_train)
        rmse = round((np.sqrt(mean_squared_error(Y_train, Y_train_predict))), 2)
        r2 = round(lr.score(X_train, Y_train), 2)
        Y_pred = lr.predict(X_test)
        rmse_test = round((np.sqrt(mean_squared_error(Y_test, Y_pred))), 2)
        r2_test = round(lr.score(X_test, Y_test), 2)
        fig.add_trace(go.Scatter(x=Y_test, y=Y_pred, mode = "markers", marker=dict(color="red")), row=4, col=1)

        fig["layout"]["xaxis"]["title"]="Price"
        fig["layout"]["xaxis3"]["title"]="Rad"
        fig["layout"]["xaxis4"]["title"]="Chas"
        fig["layout"]["xaxis5"]["title"]="LSTAT"
        fig["layout"]["xaxis6"]["title"]="RM"
        fig["layout"]["xaxis7"]["title"]=f"Actual value (Price)\tR-Sq error = {r2} (Train); {r2_test} (Test)\tRMSE = {rmse} (Train); {rmse_test} (Test)"
        fig["layout"]["yaxis"]["title"]="Count"
        fig["layout"]["yaxis3"]["title"]="Count"
        fig["layout"]["yaxis4"]["title"]="Count"
        fig["layout"]["yaxis5"]["title"]="House prices in $1000"
        fig["layout"]["yaxis6"]["title"]="House prices in $1000"
        fig["layout"]["yaxis7"]["title"]="Predicted value (Price)"
        fig.update_traces(colorbar_thickness=10, selector=dict(type="heatmap"))
        fig.update_layout(height=1500, title_text="EDA on Boston House Price Prediction Dataset", bargap=0.30, showlegend=False)
        plot = pio.to_html(fig, full_html=False)

        extra_context = extra_context or {"plot": plot}
        return super().changelist_view(request, extra_context=extra_context)



admin.site.register(BostonHousePriceDataset, BostonHousePriceDatasetAdmin)