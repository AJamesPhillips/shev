from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


from shev import roster
from shev.views import RedirectRoot


urlpatterns = patterns('',
    url(r'^/?$', RedirectRoot.as_view(), name='root'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^roster/', include('shev.roster.urls'))
)
