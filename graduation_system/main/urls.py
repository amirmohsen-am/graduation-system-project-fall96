# Amirmohsen Ahanchi

from django.conf.urls import url
from django.contrib.auth import views as auth_views







from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', auth_views.login, name='login'),
    url(r'^login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^designer$', views.designer_view, name='designer-view'),
    url(r'^process/(?P<process_id>\d+)$', views.process_view, name='process-view'),
    url(r'^task/(?P<task_id>\d+)$', views.task_view, name='task-view'),
    url(r'^task_add/(?P<process_id>\d+)$', views.task_add, name='task-add'),
    url(r'^process_add/', views.process_add, name='process-add'),
    url(r'^process_select/(?P<process_id>\d+)$', views.process_select, name='process-select'),
    url(r'^student_view/', views.student_view, name='student-view'),
    url(r'^task_graph/(?P<process_id>\d+)$', views.task_graph, name='task-graph'),
    url(r'^staff$', views.staff_view, name='staff-view'),
    url(r'^process_instance/(?P<p_id>\d+)$', views.process_instance_view, name='process-instance-view'),
    url(r'^task_instance/(?P<t_id>\d+)$', views., name='task-instance-view'),
    url(r'^account/$', views.account_view, name='account-view'),
]