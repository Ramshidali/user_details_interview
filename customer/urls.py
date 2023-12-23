from django.urls import path,re_path
from dal import autocomplete
from . import views

app_name = 'customer'

urlpatterns = [
    re_path(r'login/$', views.signin, name='signin'),
    re_path(r'index/$', views.index, name='index'),
    re_path(r'sign-up/$', views.sign_up, name='sign_up'),
]