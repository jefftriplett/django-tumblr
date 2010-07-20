import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from taggit.managers import TaggableManager

from djumblr.signals import tumbleitem_saved, tumbleitem_deleted
from djumblr.callbacks import tumbleitem_saved_callback, tumbleitem_deleted_callback


class TumbleItem(models.Model):
    FORMAT_CHOICES = (
        ('html', 'HTML'),
        ('markdown', 'Markdown'),
    )

    tumblr_id = models.CharField(max_length=64, editable=False, null=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='html')
    tags = TaggableManager()

    # this is for magic later and makes doing lookups both easier and lazier.
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    object_id = models.PositiveIntegerField(db_index=True, editable=False, null=True)
    object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")

    class Meta:
        ordering = ['-pub_date']

    def save(self, **kwargs):
        created = True if self.pk else False
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base(**kwargs)
        tumbleitem_saved.send(sender=TumbleItem, instance=self, created=created)

    def __unicode__(self):
        if self.content_type:
            return u"TumbleItem (%s)" % (self.content_type)
        else:
            return u"TumbleItem"

    def get_absolute_url(self):
        view_name = 'djumblr_detail' % (self.content_type)
        return (view_name, (), { 'year': self.pub_date.strftime("%Y"),
                                 'month': self.pub_date.strftime("%b").lower(),
                                 'day': self.pub_date.strftime("%d"),
                                 'tumblr_id': self.tumblr_id })
    get_absolute_url = models.permalink(get_absolute_url)

    def get_content_type_url(self):
        view_name = 'djumblr_content_type_detail' % (self.content_type)
        return (view_name, (), { 'content_type': self.content_type.name,
                                 'year': self.pub_date.strftime("%Y"),
                                 'month': self.pub_date.strftime("%b").lower(),
                                 'day': self.pub_date.strftime("%d"),
                                 'tumblr_id': self.tumblr_id })
    get_content_type_url = models.permalink(get_content_type_url)


class Audio(TumbleItem):
    data = models.FileField(upload_to='audio/', blank=True)
    embed = models.TextField(blank=True)
    caption = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Audio"

    def __unicode__(self):
        return u"Audio"


class Conversation(TumbleItem):
    title = models.CharField(max_length=500, blank=True)
    conversation_text = models.TextField()

    def save(self, **kwargs):
        super(Conversation, self).save(**kwargs)

        try:
            self.conversationline_set.all().delete()
        except:
            pass

        lines = self.conversation_text.split('\n')
        for line in lines:
            c = ConversationLine(conversation=self, line=line)
            c.save()

    def __unicode__(self):
        if self.title:
            return u"%s (Conversation)" % self.title
        else:
            return u"Conversation"


class ConversationLine(models.Model):
    line = models.CharField(max_length=1000)
    conversation = models.ForeignKey(Conversation)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.line


class Link(TumbleItem):
    name = models.CharField(max_length=500, blank=True)
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)

    def __unicode__(self):
        if self.name:
            return u"%s (link)" % self.name
        else:
            return u"Link"


class Photo(TumbleItem):
    source = models.URLField(blank=True)
    photo = models.ImageField(upload_to="photos/", blank=True)
    caption = models.TextField(blank=True)
    click_through_url = models.URLField(blank=True)

    def __unicode__(self):
        return u"Photo"


class Quote(TumbleItem):
    quote_text = models.TextField()
    source = models.TextField(blank=True)

    def __unicode__(self):
        return u"Quote"


class Regular(TumbleItem):
    title = models.CharField(max_length=250, blank=True)
    body = models.TextField()

    class Meta:
        verbose_name_plural = "Regular"

    def __unicode__(self):
        if self.title:
            return u"%s (regular)" % self.title
        else:
            return u"Regular"


class Video(TumbleItem):
    embed = models.TextField(blank=True)
    data = models.FileField(blank=True, upload_to='videos/')
    title = models.CharField(blank=True, max_length=250)
    caption = models.TextField(blank=True)

    def __unicode__(self):
        if self.title:
            return u"%s (video)" % self.title
        else:
            return u"Video"


tumbleitem_saved.connect(tumbleitem_saved_callback, sender=TumbleItem)
tumbleitem_deleted.connect(tumbleitem_deleted_callback, sender=TumbleItem)
