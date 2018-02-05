from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from main.models import Process, Task


@login_required(login_url='/login/')
def index(request):
    return render(request, 'main/base.html')


@login_required(login_url='/login/')
def designer_view(request):
    processes = Process.objects.all()
    return render(request, 'main/designer.html', {'processes': processes})


@login_required(login_url='/login/')
def process_view(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    return render(request, 'main/process.html', {'process': process})


@login_required(login_url='/login/')
def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'main/task.html', {'task': task})
