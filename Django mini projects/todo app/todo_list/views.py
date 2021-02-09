from django.shortcuts import render, redirect
from .models import TodoList as table
from .forms import ListForm
from django.contrib import messages
# Create your views here.


def home(request):

    def renderScreen():
        all_items = table.objects.all
        return render(request, 'home.html', {'all_items': all_items})

    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your item has been added to the list.')
            return renderScreen()
    else:
        return renderScreen()


def about(request):
    return render(request, 'about.html', {})


def delete(request, list_id):
    item = table.objects.get(pk=list_id)
    item.delete()
    messages.success(request, 'Your item has been deleted.')
    return redirect('home')


def cross(request, list_id):
    item = table.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')


def uncross(request, list_id):
    item = table.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')


def edit(request, list_id):
    def renderScreen():
        item = table.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item': item})

    if request.method == 'POST':
        item = table.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your item has been edited.')
            return redirect('home')
    else:
        return renderScreen()
