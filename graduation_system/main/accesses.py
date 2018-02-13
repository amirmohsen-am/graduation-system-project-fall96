from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from main.models import Process, Task, ProcessForm, TaskForm, ProcessInstance, TaskInstance, UserForm, Comment
from django.urls import reverse


def student_check(user):
    return user.student

def staff_check(user):
    return user.is_staff
