from django.db import models


# Create your models here.

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

    def __str__(self):
        return self.name


class ProcessInstance(models.Model):
    process = models.ForeignKey(Process, blank=False)

    def __str__(self):
        return self.name + "-instance-" + self.id


class TaskInstance(models.Model):
    process_instance = models.ForeignKey(ProcessInstance, blank=False)

    def __str__(self):
        return self.name + "instance-" + self.id
