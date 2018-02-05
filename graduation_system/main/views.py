
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from main.models import ProcessForm
from main.models import Process

def index(request):
    return render(request, 'main/base.html')


def designer_view(request):
    processes = Process.objects.all()
    return render(request, 'main/designer.html', {'processes': processes})


def process_view(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    form = ProcessForm(instance=process)
    return render(request, 'main/process.html', {'process': process, 'form': form})



