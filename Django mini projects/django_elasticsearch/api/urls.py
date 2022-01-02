import accounts.urls
from django.urls import path, include
from rest_framework.schemas import get_schema_view


app_name = 'api'

urlpatterns = [
    path("v1/", include(accounts.urls)),
    path('schema/', get_schema_view(title="Insureka ML Server", description="App to demonstrate elasticsearch.", version="1.0.0"), name='openapi-schema'),
]

handler500 =  'rest_framework.exceptions.server_error'