from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
#    path('$', views.index, name = 'index')
    url(r'^$', views.hello, name = 'hello'),	
    url(r'^index/$', views.index, name = 'index'),	#127.0.0.1:8000/webapp/index ->shows	
]
