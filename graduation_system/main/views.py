from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from main.models import Process, Task, ProcessForm , TaskForm
from django.urls import reverse

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
    if request.method == 'POST':
        form = ProcessForm(request.POST, instance=process)
        if form.is_valid():
            form.save()
            messages.success(request, 'Process was successfully edited')
            # return redirect(reverse('process-view'))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ProcessForm(instance=process)

    return render(request, 'main/process.html', {'process': process, 'form': form})


@login_required(login_url='/login/')
def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task was successfully edited')
            return redirect(reverse('task-view'))
    else:
        form = TaskForm(instance=task)

    return render(request, 'main/task.html', {'task': task, 'form': form})


@login_required(login_url='/login/')
def task_add(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task has been created')
            return redirect(reverse('process-view', args=[process_id]))
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = TaskForm()
    form.fields["process"].initial = process
    form.fields['process'].widget.attrs['readonly'] = True
    return render(request, 'main/task_add.html', {'form': form})

@login_required(login_url='/login/')
def process_add(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Process has been created')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ProcessForm()
    return render(request, 'main/process_add.html', {'form': form})