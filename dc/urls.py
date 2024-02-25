from django.contrib import admin
from django.urls import path, include, re_path
from debug_toolbar.urls import urlpatterns as debug_toolbar_urls
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from main.urls import urlpatterns as main_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('' , include(main_urls))
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
