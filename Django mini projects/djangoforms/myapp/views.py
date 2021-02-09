from django.shortcuts import render
from .forms import ContactForm, SnippetForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        model_form = SnippetForm(request.POST)
        if form.is_valid() and model_form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            category = form.cleaned_data['category']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            info = [name, email, category, subject, body]
            model_form.save()
            info_model = 'Valid'
            return render(request, 'home.html', {'form': form, 'info': info, 'model_form': model_form, 'info_model': info_model})
        else:
            form = ContactForm()
            model_form = SnippetForm()
            return render(request, 'home.html', {'form': form, 'info': 'N/A', 'model_form': model_form, 'info_model': 'N/A'})
    else:
        form = ContactForm()
        model_form = SnippetForm()
        return render(request, 'home.html', {'form': form, 'info': 'N/A', 'model_form': model_form, 'info_model': 'N/A'})
