from django import forms
from .models import Snippet


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(label='Email')
    category = forms.ChoiceField(choices=[('questions', 'Question'), ('others', 'Others')])
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('name_model', 'body_model')
