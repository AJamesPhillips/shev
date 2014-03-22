from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import roster

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^roster/', include('roster.urls'))
)
