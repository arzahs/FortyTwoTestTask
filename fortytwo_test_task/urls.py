from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from apps.bio.views import AboutMe
urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', AboutMe.as_view(), name='about_me'),
    url(r'^admin/', include(admin.site.urls)),
)
