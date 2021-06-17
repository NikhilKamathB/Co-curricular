import random
from .forms import *
from .models import *
from django.shortcuts import render


def home(request):
    context = None
    if request.method == 'POST':
        form = ScapeForm(request.POST, request.FILES)
        if form.is_valid():
            scape = form.save()
            context = {
                'scape': scape
            }
    else:
        scape = ScapeModel.objects.all()
        if scape.count() == 0:
            scape = None
        else:
            scape = random.choice(scape)
        context = {
            'scape': scape
        }
    return render(request, 'home.html', context)