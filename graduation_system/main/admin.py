from django.contrib import admin

# Register your models here.
from main.models import Task
from .models import Process

admin.site.register(Process)
admin.site.register(Task)
