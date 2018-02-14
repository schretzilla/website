from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^sacm/$', views.sacm, name='sacm'),
    url(r'^self-help/$', views.self_help, name='self-help'),
    url(r'^smart-egg/$', views.smart_egg, name='smart-egg'),
    
    url(r'^projects/$', views.projects, name='projects'),
    
    #Custom directives
    url(r'^percent/$', views.percent, name='percent'),

]