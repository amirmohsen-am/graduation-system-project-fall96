from django.shortcuts import render, get_object_or_404

# Create your views here.
from main.models import Process


def index(request):
    return render(request, 'main/base.html')


def designer_view(request):
    processes = Process.objects.all()
    return render(request, 'main/designer.html', {'processes': processes})

def process_view(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    return render(request, 'main/process.html', {'process': process})