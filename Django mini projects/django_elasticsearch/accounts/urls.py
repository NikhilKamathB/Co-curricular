from .views import *
from rest_framework import routers
from django.urls import path, include


app_name = "accounts"

router = routers.DefaultRouter() 
router.register(r'accounts-jaeger-1', AccountsJaeger1ViewSet)
router.register(r'accounts-jaeger-2', AccountsJaeger2ViewSet)

urlpatterns = [
    path("accounts-jaejer/", include(router.urls)),
]