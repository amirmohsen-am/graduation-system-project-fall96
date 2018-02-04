from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'main/base.html')

def designer_view(request):
    return render(request, 'main/designer.html')
