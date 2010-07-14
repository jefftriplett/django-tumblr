import datetime
from haystack import site
from haystack.indexes import *
from djumblr.models import Audio, Conversation, Link, Photo, Quote, Regular, Video


class TumbleItemIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='pub_date')


class AudioIndex(TumbleItemIndex):
    data = CharField(model_attr='data')
    embed = CharField(model_attr='embed')
    caption = CharField(model_attr='caption')


class ConversationIndex(TumbleItemIndex):
    title = CharField(model_attr='title')
    conversation_text = CharField(model_attr='conversation_text')


class LinkIndex(TumbleItemIndex):
    name = CharField(model_attr='name')
    url = CharField(model_attr='url')
    description = CharField(model_attr='description')


class PhotoIndex(TumbleItemIndex):
    source = CharField(model_attr='source')
    photo = CharField(model_attr='photo')
    caption = CharField(model_attr='caption')
    click_through_url = CharField(model_attr='click_through_url')


class QuoteIndex(TumbleItemIndex):
    quote_text = CharField(model_attr='quote_text')
    source = CharField(model_attr='source')


class RegularIndex(TumbleItemIndex):
    title = CharField(model_attr='title')
    body = CharField(model_attr='body')


class VideoIndex(TumbleItemIndex):
    embed = CharField(model_attr='embed')
    data = CharField(model_attr='data')
    title = CharField(model_attr='title')
    caption = CharField(model_attr='caption')


site.register(Audio, AudioIndex)
site.register(Conversation, ConversationIndex)
site.register(Link, LinkIndex)
site.register(Photo, PhotoIndex)
site.register(Quote, QuoteIndex)
site.register(Regular, RegularIndex)
site.register(Video, VideoIndex)
