from .tasks import *
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.schemas.openapi import AutoSchema


class AccountsJaeger1ViewSet(viewsets.ModelViewSet):

    schema = AutoSchema(tags=['accounts-jaeger-1'], operation_id_base='AccountsJaeger1ViewSet')
    queryset = User.objects.all()
    http_method_names = ['get'] 
    
    def get_serializer_class(self):
        return UserSerializer
    
    def list(self, request, *args, **kwargs):
        delay_1(request)
        delay_2(request)
        return super().list(request, *args, **kwargs)


class AccountsJaeger2ViewSet(viewsets.ModelViewSet):

    schema = AutoSchema(tags=['accounts-jaeger-2'], operation_id_base='AccountsJaeger2ViewSet')
    queryset = User.objects.all()
    http_method_names = ['get'] 
    
    def get_serializer_class(self):
        return UserSerializer
    
    def list(self, request, *args, **kwargs):
        delay_3(request)
        delay_4(request)
        return super().list(request, *args, **kwargs)