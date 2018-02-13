from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserChangeForm

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import DeleteView

from main.utils import staff_check, student_check, user_is_student
from main.models import Process, Task, ProcessForm, TaskForm, ProcessInstance, TaskInstance, UserForm, Comment
from django.urls import reverse


@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
@user_passes_test(staff_check)
def designer_view(request):
    processes = Process.objects.all()
    return render(request, 'main/designer.html', {'processes': processes})


@login_required
@user_passes_test(student_check)
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


@login_required
@user_passes_test(student_check)
def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task was successfully edited')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = TaskForm(instance=task)

    return render(request, 'main/task.html', {'task': task, 'form': form})


@login_required
@user_passes_test(staff_check)
def task_add(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, process_custom=process)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task has been created')
            return redirect(reverse('process-view', args=[process_id]))
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = TaskForm(process_custom=process)
    form.fields["process"].initial = process
    form.fields['process'].widget.attrs['readonly'] = True
    # form.fields['process'].widget.attrs['disabled'] = True
    return render(request, 'main/task_add.html', {'form': form})

@login_required
@user_passes_test(staff_check)
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    messages.success(request, 'Task has been deleted')
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(staff_check)
def process_add(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Process has been created')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ProcessForm()
    form.fields['task_start'].widget = forms.HiddenInput()
    return render(request, 'main/process_add.html', {'form': form})


@login_required
@user_passes_test(staff_check)
def process_delete(request, process_id):
    process = get_object_or_404(Process, id=process_id)
    messages.success(request, 'Process has been deleted')
    process.delete()
    return redirect(request.META.get('HTTP_REFERER'))

# new instance of process
@login_required
@user_passes_test(student_check)
def process_select(request, process_id):
    user = request.user

    process = get_object_or_404(Process, id=process_id)
    instances = process.processinstance_set.filter(student=user.student)
    if len(instances) >= 1:
        messages.error(request, 'Student has selected this process before')
        return redirect(request.META.get('HTTP_REFERER'))

    if process.task_start is None:
        messages.error(request, 'Please specify starting task for this process')
        return redirect(request.META.get('HTTP_REFERER'))

    process_instance = ProcessInstance(student=user.student, process=process)
    process_instance.save()
    for task in process.task_set.all():
        TaskInstance.objects.create(process_instance=process_instance, task=task)
    process_instance.current_task = TaskInstance.objects.get(task=process.task_start, process_instance=process_instance)
    process_instance.save()
    messages.success(request, 'Process has been instantiated')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(student_check)
def student_view(request):
    user = request.user
    processes = Process.objects.all()
    return render(request, 'main/student_view.html', {'student': user.student, 'processes': processes})


@login_required
@user_passes_test(staff_check)
def staff_view(request):
    user = request.user
    # group_names = user.groups.values_list('name', flat=True)
    group_names = user.groups.all()
    if user.is_superuser:
        task_instances = TaskInstance.objects.all().filter()
    else:
        task_instances = TaskInstance.objects.all().filter(task__group__in=group_names)
    return render(request, 'main/staff-view.html', {'task_instances': task_instances})


@login_required
# @user_passes_test(staff_check)
def process_instance_delete(request, p_id):
    process_instance = get_object_or_404(ProcessInstance, id=p_id)
    messages.success(request, 'Process instance has been deleted')
    process_instance.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def process_instance_view(request, p_id):
    user = request.user
    process_instance = get_object_or_404(ProcessInstance, id=p_id)
    current_task = process_instance.current_task
    if request.method == 'POST':
        action = request.POST.get('action')
        if user.is_staff:
            if action == 'accept':
                if not current_task.task.end_task and current_task.task.next_task_accept is None:
                    messages.error(request, 'Task has no next_task_accept')
                else:
                    messages.success(request, 'Task successfully accepted')
                    process_instance.accept()
            if action == 'reject':
                if not current_task.task.end_task and current_task.task.next_task_reject is None:
                    messages.error(request, 'Task has no next_task_reject')
                else:
                    messages.success(request, 'Task successfully rejected')
                    process_instance.reject()
            # if action == 'staff_done':
            #     current_task.status = 'student_pending'
        if user_is_student(user):
            if action == 'student_done':
                current_task.status = 'staff_pending'
                current_task.save()
        text = request.POST.get('comment-text')
        if text is not None:
            Comment.objects.create(user=user, text=text, task_instance=current_task)

    ordered_task = []
    after_current = []
    p = process_instance.process
    t = TaskInstance.objects.get(task=p.task_start, process_instance=process_instance)
    b = 2
    while 1:
        if t == process_instance.current_task:
            b = 1
        if b == 2:
            ordered_task.append(t)
        if b == 0:
            after_current.append(t)
        if t is None:
            break
        if t.task.end_task == True:
            break
        if b == 1:
            b = 0
        next_task = t.task.next_task_accept
        if next_task is None:
            break
        t = TaskInstance.objects.get(task=next_task, process_instance=process_instance)

    process = process_instance.process
    form = ProcessForm(instance=process)

    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = True
    for field_name, field in form.fields.items():
        field.widget.attrs['disabled'] = True

    return render(request, 'main/process-instance.html',
                  {'process_instance': process_instance, 'form': form, 'ordered_task': ordered_task,
                   'cur': process_instance.current_task, 'after': after_current})


@login_required
def task_instance_view(request, t_id):
    user = request.user
    task_instance = get_object_or_404(TaskInstance, id=t_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if user_is_student(user):
            if action == 'student_done':
                task_instance.status = 'staff_pending'
                task_instance.save()
        # else:
        #     if action == 'staff_done':
        #         task_instance.status = 'student_pending'
        text = request.POST.get('comment-text')
        if text is not None:
            Comment.objects.create(user=user, text=text, task_instance=task_instance)
    form = TaskForm(instance=task_instance.task)

    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = True

    for field_name, field in form.fields.items():
        field.widget.attrs['disabled'] = True

    return render(request, 'main/task-instance.html', {'task_instance': task_instance, 'form': form})


@login_required
def account_view(request):
    form = UserForm(instance=request.user)
    return render(request, 'main/account.html', {'form': form})


@login_required
def contact_view(request):
    processes = Process.objects.all()
    return render(request, 'main/contact.html', {'processes': processes})

@login_required
def bank_view(request, t_id):
    processes = Process.objects.all()
    return render(request, 'main/bank.html', {'processes': processes})