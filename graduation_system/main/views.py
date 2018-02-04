from django.shortcuts import render

# Create your views here.
from main.models import Process


def index(request):
    return render(request, 'main/base.html')


def designer_view(request):
    processes = Process.objects.all()
    return render(request, 'main/designer.html', {'processes': processes})
