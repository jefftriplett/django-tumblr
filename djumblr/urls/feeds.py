from django.conf.urls.defaults import patterns, url
from djumblr.feeds import LatestTumbleItemFeed
from djumblr.feeds import LatestAudioFeed
from djumblr.feeds import LatestConversationFeed
from djumblr.feeds import LatestLinkFeed
from djumblr.feeds import LatestPhotoFeed
from djumblr.feeds import LatestQuoteFeed
from djumblr.feeds import LatestRegularFeed
from djumblr.feeds import LatestVideoFeed


urlpatterns = patterns('',
    url(r'^latest/$',
        LatestTumbleItemFeed(),
        name='djumblr_latest_feed'),

    url(r'^latest/audio/$',
        LatestAudioFeed(),
        name='djumblr_latest_audio_feed'),

    url(r'^latest/conversation/$',
        LatestConversationFeed(),
        name='djumblr_latest_conversation_feed'),

    url(r'^latest/link/$',
        LatestLinkFeed(),
        name='djumblr_latest_link_feed'),

    url(r'^latest/photo/$',
        LatestPhotoFeed(),
        name='djumblr_latest_photo_feed'),

    url(r'^latest/quote/$',
        LatestQuoteFeed(),
        name='djumblr_latest_quote_feed'),

    url(r'^latest/regular/$',
        LatestRegularFeed(),
        name='djumblr_latest_regular_feed'),

    url(r'^latest/video/$',
        LatestVideoFeed(),
        name='djumblr_latest_video_feed'),
)
