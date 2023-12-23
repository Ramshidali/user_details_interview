from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    re_path(r'', views.customer),
    re_path(r'^edit-profile/$', views.edit_profile, name='edit_profile'),

]