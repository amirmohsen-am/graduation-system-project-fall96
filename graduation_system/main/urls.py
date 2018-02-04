# Amirmohsen Ahanchi

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^designer-view^$', views.designer_view, name='designer-view'),

]