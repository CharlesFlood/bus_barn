from django.conf.urls import url

from . import views

app_name = 'vehicles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^vehicle/$', views.vehicle_list, name='vehicle_list'),
    url(r'^(?P<vehicle_id>[0-9]+)/$', views.vehicle_detail, name='vehicle_detail'),
    url(r'^(?P<vehicle_id>[0-9]+)/edit/$', views.vehicle_detail, name='vehicle_edit'),
    
    url(r'^mechanic/add/$', views.mechanic_add, name='mechanic_add'),
    url(r'^mechanic/$', views.mechanic_list, name='mechanic_list'),
    
    url(r'^issue/$', views.issue_list, name='issue_list'),
    url(r'^issue/(?P<issue_id>[0-9]+)/$', views.issue_detail, name='issue_detail'),
    url(r'^issue/(?P<issue_id>[0-9]+)/edit$', views.issue_edit, name='issue_edit'),
    url(r'^issue/add/$', views.issue_add, name='issue_add'),
    url(r'^issue/add/(?P<bus_id>[0-9]+)/$', views.issue_add, name='issue_add'),
    url(r'^issue/fixed$', views.issue_fixed, name='issue_fixed'),
    url(r'^issue/delete/(?P<issue_id>[0-9]+)/$', views.issue_delete, name='issue_delete'),
    
    url(r'^issue/print/$', views.issue_print, name='issue_print'),
]
