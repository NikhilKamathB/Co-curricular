from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'App_1/home.html', context)

def face_mesh(request):
    context = {}
    return render(request, 'App_1/face_mesh.html', context)
