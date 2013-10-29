from django.conf.urls import patterns, url
from quicklinks.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^(\d+)$', external_redirect, name='redirect'),
    url(r'^create/$', create, name='create'),
)
