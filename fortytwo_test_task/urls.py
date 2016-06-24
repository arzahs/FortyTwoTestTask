from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from apps.bio.views import AboutMe, RequestList, EditPersonView
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', AboutMe.as_view(), name='about_me'),
    url(r'^edit_form/$', EditPersonView.as_view(), name='edit_form'),
    url(r'requests_list/$', RequestList.as_view(), name='requests_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()
