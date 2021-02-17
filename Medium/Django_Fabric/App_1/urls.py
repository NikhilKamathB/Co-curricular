from django.urls import path
from . import views


app_name = 'app_1'

urlpatterns = [
    path('', views.home, name='home'),
    path('face-mesh/', views.face_mesh, name='face_mesh'),
    path('hands/', views.hands, name='hands'),
    path('pose/', views.pose, name='pose'),
    path('holistic/', views.holistic, name='holistic'),
]
