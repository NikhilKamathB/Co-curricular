from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock
import requests
import json


# Create your views here.
def home(request, company=None):

    def renderScreen(company='aapl'):
        # API -> pk_944cb869fc15484bae68155ac04dbfea
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + company + "/quote?token=pk_944cb869fc15484bae68155ac04dbfea")
        try:
            api = json.loads(api_request.content)
        except Exception:
            api = 'Error'
        return render(request, 'home.html', {'api': api})

    if company is None:
        if request.method == 'POST':
            _company = request.POST['quote']
            return renderScreen(_company)
        elif request.method == 'GET':
            return renderScreen()
    else:
        return renderScreen(company)


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your stock quote has been added."))
            return redirect('add_stock')
    elif request.method == 'GET':
        quote = Stock.objects.all()
        return render(request, 'add_stock.html', {'quote': quote})


def delete(request, list_id):
    item = Stock.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ("Your stock quote has been deleted."))
    return redirect('add_stock')
