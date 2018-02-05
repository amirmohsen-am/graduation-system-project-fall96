from django.contrib import admin

# Register your models here.
from main.models import Task, Student
from .models import Process

admin.site.register(Process)
admin.site.register(Task)
admin.site.register(Student)
