from django.conf.urls import patterns, include, url


urlpatterns = patterns('shev.roster.views',
    url(r'^about/', 'about', name='about'),
    url(r'^day/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'day', name='day'),
# future:
#    url(r'^month/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'month', name='month'),
#    url(r'^day/(?P<year>\d{4})/$', 'year', name='year'),
    url(r'^$', 'home', name='home')
)
