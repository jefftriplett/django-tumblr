from django.contrib.syndication.views import Feed
from djumblr.models import TumbleItem, Audio, Conversation, Link, Photo, Quote, Regular, Video


class LatestTumbleItemFeed(Feed):
    title = 'Latest tumble items'
    link = '/tumblr/feeds/latest/'

    def items(self):
        return TumbleItem.objects.all().order_by('-pub_date')[:25]


class LatestAudioFeed(Feed):
    #data = models.FileField(upload_to='audio/', blank=True)
    #embed = models.TextField(blank=True)
    #caption = models.TextField(blank=True)

    title = 'Latest audio items'
    link = '/tumblr/feeds/latest/audio/'
    description_template = 'feeds/audio_description.html'

    def items(self):
        return Audio.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body


class LatestConversationFeed(Feed):
    title = 'Latest conversation items'
    link = '/tumblr/feeds/latest/conversation/'

    def items(self):
        return Conversation.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.conversation_text


class LatestLinkFeed(Feed):
    title = 'Latest link items'
    link = '/tumblr/feeds/latest/link/'

    def items(self):
        return Link.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.name
    
    def item_description(self, item):
        return item.description


class LatestPhotoFeed(Feed):
    title = 'Latest photo items'
    link = '/tumblr/feeds/latest/photo/'
    description_template = 'feeds/photo_description.html'

    def items(self):
        return Photo.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.caption


class LatestQuoteFeed(Feed):
    title = 'Latest quote items'
    link = '/tumblr/feeds/latest/quote/'

    def items(self):
        return Quote.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.quote_text

    def item_description(self, item):
        return item.source


class LatestRegularFeed(Feed):
    title = 'Latest regular items'
    link = '/tumblr/feeds/latest/regular/'

    def items(self):
        return Regular.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body


class LatestVideoFeed(Feed):
    #embed = models.TextField(blank=True)
    #data = models.FileField(blank=True, upload_to='videos/')
    #caption = models.TextField(blank=True)

    title = 'Latest video items'
    link = '/tumblr/feeds/latest/video/'
    description_template = 'feeds/video_description.html'

    def items(self):
        return Video.objects.all().order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    #def item_description(self, item):
    #    return item.caption
