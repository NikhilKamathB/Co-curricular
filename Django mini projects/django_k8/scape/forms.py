from .models import *
from django import forms


class ScapeForm(forms.ModelForm):
    class Meta:
        model = ScapeModel
        fields = '__all__'