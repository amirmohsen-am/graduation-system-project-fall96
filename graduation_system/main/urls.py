# Amirmohsen Ahanchi

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', auth_views.login, name='login'),
    url(r'^login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^designer$', views.designer_view, name='designer-view'),
    url(r'^process/(?P<process_id>\d+)$', views.process_view, name='process-view')
]