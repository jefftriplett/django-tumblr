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
    (r'^latest/$',
        LatestTumbleItemFeed()),

    (r'^latest/audio/$',
        LatestAudioFeed()),

    (r'^latest/conversation/$',
        LatestConversationFeed()),

    (r'^latest/link/$',
        LatestLinkFeed()),

    (r'^latest/photo/$',
        LatestPhotoFeed()),

    (r'^latest/quote/$',
        LatestQuoteFeed()),

    (r'^latest/regular/$',
        LatestRegularFeed()),

    (r'^latest/video/$',
        LatestVideoFeed()),
)
