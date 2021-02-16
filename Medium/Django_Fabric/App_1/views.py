from django.shortcuts import render


def home(request):
    return render(request, 'App_1/home.html', {})
