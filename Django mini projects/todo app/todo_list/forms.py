from django import forms
from .models import TodoList


class ListForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['item', 'completed']
