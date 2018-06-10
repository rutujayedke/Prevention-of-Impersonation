from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

	url(r'^$', views.index, name = 'index'),
	url(r'^contact/', views.contact, name= 'contact'),	
	url(r'^success/', views.success, name= 'success'),
	url(r'^center_list/', views.center_list, name = 'center_list'),
	url(r'^login/', views.login, name='login'),
	url(r'^studentdetails/', views.studentdetails, name = 'studentdetails'),
	url(r'^showdetails/', views.showdetails, name = 'showdetails'),

]
