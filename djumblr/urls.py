from django.conf.urls.defaults import patterns, url
from djumblr import views
from djumblr.feeds import LatestTumbleItemFeed
from djumblr.feeds import LatestAudioFeed
from djumblr.feeds import LatestConversationFeed
from djumblr.feeds import LatestLinkFeed
from djumblr.feeds import LatestPhotoFeed
from djumblr.feeds import LatestQuoteFeed
from djumblr.feeds import LatestRegularFeed
from djumblr.feeds import LatestVideoFeed


feeds = {
    'latest': LatestTumbleItemFeed,
    'latest/audio': LatestAudioFeed,
    'latest/conversation': LatestConversationFeed,
    'latest/link': LatestLinkFeed,
    'latest/photo': LatestPhotoFeed,
    'latest/quote': LatestQuoteFeed,
    'latest/regular': LatestRegularFeed,
    'latest/video': LatestVideoFeed,
}


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

    url(r'^(?P<content_type>[-\w]+)/tags/(?P<slug>(.*))/$',
        views.tumble_tag_detail,
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

    url(r'^tags/(?P<slug>(.*))/$',
        views.tumble_tag_detail,
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

    # the feeds section will be changed once the feeds2 section works
    (r'^feeds/latest/$',
        LatestTumbleItemFeed()),
    (r'^feeds/latest/audio/$',
        LatestAudioFeed()),
    (r'^feeds/latest/conversation/$',
        LatestConversationFeed()),
    (r'^feeds/latest/link/$',
        LatestLinkFeed()),
    (r'^feeds/latest/photo/$',
        LatestPhotoFeed()),
    (r'^feeds/latest/quote/$',
        LatestQuoteFeed()),
    (r'^feeds/latest/regular/$',
        LatestRegularFeed()),
    (r'^feeds/latest/video/$',
        LatestVideoFeed()),
    (r'^feeds2/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

    url(r'^(?P<content_type>[-\w]+)/$',
        views.tumble_object_list,
        name='djumblr_content_type_object_list'),

    url(r'^$',
        views.tumble_object_list,
        name='djumblr_object_list'),
)
