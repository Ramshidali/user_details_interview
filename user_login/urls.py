from django.contrib import admin
from django.views.static import serve
from django.urls import  include, path, re_path
from django.conf import settings

urlpatterns = [
    path('',include(('customer.urls'),namespace='customer')),
    
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    
    path('api/user-details/', include(('api.user_details.urls','user_details'), namespace='api_user_details')),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
