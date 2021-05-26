from .views import *
from django.urls import path


app_name = "api"

urlpatterns = [
    path("", home, name="home"),
    path("digit-recognizer/", digit_recognizer, name="digit_recognizer"),
]