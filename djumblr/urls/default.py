from django.conf.urls.defaults import *
from djumblr.models import TumbleItem


tumble_item_dict = {
    'queryset': TumbleItem.objects.all(),
    'date_field': 'pub_date',
}

tumble_item_generic_dict = dict(tumble_item_dict)
tumble_item_generic_detail_dict = dict(tumble_item_dict)
tumble_item_generic_dict['template_name'] = 'djumblr/generic.html'
tumble_item_generic_detail_dict['template_name'] = 'djumblr/generic_detail.html'


urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.date_based.archive_index',
        tumble_item_dict, 
        name='djumblr_archive_index'),
    url(r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year',
        tumble_item_dict,
        name='djumblr_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'django.views.generic.date_based.archive_month',
        tumble_item_generic_dict,
        name='djumblr_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        'django.views.generic.date_based.archive_day',
        tumble_item_generic_dict,
        name='djumblr_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<object_id>\d+)/$',
        'django.views.generic.date_based.object_detail',
        tumble_item_generic_detail_dict,
        name='djumblr_detail'),
    (r'regular/', include('djumblr.urls.regular')),
    (r'photo/', include('djumblr.urls.photo')),
    (r'quote/', include('djumblr.urls.quote')),
    (r'link/', include('djumblr.urls.link')),
    (r'conversation/', include('djumblr.urls.conversation')),
    (r'video/', include('djumblr.urls.video')),
    (r'audio/', include('djumblr.urls.audio')),
)
