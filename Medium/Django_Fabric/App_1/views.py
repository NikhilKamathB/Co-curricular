from django.shortcuts import render


def home(request):
    context = {'entries': range(1, 5)}
    return render(request, 'App_1/home.html', context)
