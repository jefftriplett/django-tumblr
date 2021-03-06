from django.conf.urls.defaults import patterns, url
from djumblr import views


urlpatterns = patterns('',
    url(r'^(?P<content_type>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<tumblr_id>[-\w]+)/$',
        views.tumble_archive_object_detail,
        name='djumblr_content_type_detail'),

    url(r'^(?P<content_type>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        views.tumble_archive_day,
        name='djumblr_content_type_archive_day'),

    url(r'^(?P<content_type>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/$',
        views.tumble_archive_month,
        name='djumblr_content_type_archive_month'),

    url(r'^(?P<content_type>[-\w]+)/(?P<year>\d{4})/$',
        views.tumble_archive_year,
        name='djumblr_content_type_archive_year'),

    url(r'^(?P<content_type>[-\w]+)/tags/(?P<tag_slug>(.*))/$',
        views.tumble_object_list,
        name='djumblr_content_type_tag_detail',
    ),

    url(r'^(?P<content_type>[-\w]+)/tags/$',
        views.tumble_tag_list,
        name='djumblr_content_type_tag_list'
    ),

    url(r'^(?P<content_type>[-\w]+)/archive/$',
        views.tumble_archive_index,
        name='djumblr_content_type_archive_index'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<tumblr_id>[-\w]+)/$',
        views.tumble_archive_object_detail,
        name='djumblr_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        views.tumble_archive_day,
        name='djumblr_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        views.tumble_archive_month,
        name='djumblr_archive_month'),

    url(r'^(?P<year>\d{4})/$',
        views.tumble_archive_year,
        name='djumblr_archive_year'),

    url(r'^tags/(?P<tag_slug>(.*))/$',
        views.tumble_object_list,
        name='djumblr_tag_detail'),

    url(r'^tags/$',
        views.tumble_tag_list,
        name='djumblr_tag_list'),

    url(r'^archive/$',
        views.tumble_archive_index,
        name='djumblr_archive_index'),

    url(r'edit/$',
        views.tumble_item_form,
        name='tumble_form'),

    url(r'^(?P<content_type>[-\w]+)/$',
        views.tumble_object_list,
        name='djumblr_content_type_object_list'),

    url(r'^$',
        views.tumble_object_list,
        name='djumblr_object_list'),
)
