from django.db import models


# Create your models here.

class Process(models.Model):
    name = models.CharField(max_length=100, blank=False)
    task_start = models.ForeignKey('Task', blank=True, null=True, related_name='+')
    task_end = models.ForeignKey('Task', blank=True, null=True, related_name='+')


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False)
    process = models.ForeignKey(Process, blank=False)
    description = models.CharField(max_length=1000, blank=False)


class ProcessInstance(models.Model):
    process = models.ForeignKey(Process, blank=False)


class TaskInstance(models.Model):
    process_instance = models.ForeignKey(ProcessInstance, blank=False)
