"""Home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG, MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static
from Application.views import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/$', images_list, name='images'),
    url(r'^hidden/$', hidden_list, name='hidden'),
    url(r'^$', index, name='index'),
    url(r'^test/$', test, name='test'),
    url(r'^add_image/$', upload_image, name='add_image'),
    url(r'^get_json_images/$', images_json, name='json_images'),
    url(r'^register/$', create_user, name='create_user'),
    url(r'^login/$', login, name='login')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
