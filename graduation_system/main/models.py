from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_year = models.IntegerField()


class Process(models.Model):
    name = models.CharField(max_length=100, blank=False)
    task_start = models.ForeignKey('Task', blank=True, null=True, related_name='+')
    task_end = models.ForeignKey('Task', blank=True, null=True, related_name='+')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False)
    process = models.ForeignKey(Process, blank=False)
    description = models.CharField(max_length=1000, blank=False)

    next_task_success = models.ForeignKey('self', blank=True, null=True, related_name='+')
    next_task_fail = models.ForeignKey('self', blank=True, null=True, related_name='+')

    def __str__(self):
        return self.name


class ProcessInstance(models.Model):
    # make blank = false
    student = models.ForeignKey(Student, blank=True, null=True)
    process = models.ForeignKey(Process, blank=False)

    def __str__(self):
        return self.name + "-instance-" + self.id


class TaskInstance(models.Model):
    process_instance = models.ForeignKey(ProcessInstance, blank=False)
    task = models.ForeignKey(Task, blank=False)

    def __str__(self):
        return self.name + "instance-" + self.id


class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ['name']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
