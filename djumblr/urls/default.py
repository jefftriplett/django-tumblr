from django.conf.urls.defaults import *
from djumblr import views


urlpatterns = patterns('',
    url(r'^$',
        views.tumble_archive_index,
        name='djumblr_archive_index'),
    url(r'^(?P<year>\d{4})/$',
        views.tumble_item_archive_year,
        name='djumblr_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        views.tumble_item_archive_month,
        name='djumblr_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        views.tumble_item_archive_day,
        name='djumblr_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<tumblr_id>[-\w]+)/$',
        views.tumble_item_detail,
        name='djumblr_detail'),
    (r'regular/', include('djumblr.urls.regular')),
    (r'photo/', include('djumblr.urls.photo')),
    (r'quote/', include('djumblr.urls.quote')),
    (r'link/', include('djumblr.urls.link')),
    (r'conversation/', include('djumblr.urls.conversation')),
    (r'video/', include('djumblr.urls.video')),
    (r'audio/', include('djumblr.urls.audio')),
)
