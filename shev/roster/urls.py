from django.conf.urls import patterns, include, url


urlpatterns = patterns('roster.views',
    url(r'^about/', 'about', name='about'),
    url(r'^$', 'home', name='home')
)
