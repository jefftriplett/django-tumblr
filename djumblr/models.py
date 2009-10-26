import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import loader, Context
from tumblr import Api


def get_user_api(username):
    user = settings.TUMBLR_USERS[username]
    if user.has_key('email') and user.has_key('password'):
        return Api(user['tumblr_user'] + ".tumblr.com",
                   user['email'],
                   user['password']
                   )
    else:
        return False


def display_tumbl(object, template):
    t = loader.get_template(template)
    c = Context({"object": object})
    return t.render(c)


class TumbleItem(models.Model):
    tumblr_id = models.CharField(max_length=64, editable=False, null=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)

    # this is for magic later and makes doing lookups both easier and lazier.
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    content_id = models.IntegerField(db_index=True, editable=False, null=True)
    object = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    class Meta:
        ordering = ['-pub_date']

    def save(self, **kwargs):
        created = True if self.pk else False
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base(**kwargs)
        #tumble_save.send(sender=TumbleItem, instance=self, created=created)

    def __unicode__(self):
        if self.content_type:
            return u"TumbleItem (%s)" % (self.content_type)
        else:
            return u"TumbleItem"

    def shared_display(self):
        templates = [
            "djumblr/display/%s.html" % (self.content_type),
            "djumblr/display/generic.html",
        ]
        template = loader.select_template(templates)
        return display_tumbl(self, template.name)

    def get_absolute_url(self):
        view_name = 'djumblr_detail' % (self.content_type)
        return (view_name, (), { 'year': self.pub_date.strftime("%Y"),
                                 'month': self.pub_date.strftime("%b").lower(),
                                 'day': self.pub_date.strftime("%d"),
                                 'object_id': self.tumblr_id })
    get_absolute_url = models.permalink(get_absolute_url)


class Regular(TumbleItem):
    title = models.CharField(max_length=250, blank=True)
    body = models.TextField()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Regular"

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_regular(title=self.title, body=self.body)
                self.tumblr_id = post['id']
        super(Regular, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Regular, self).save()

    def __unicode__(self):
        if self.title:
            return u"%s (regular)" % self.title
        else:
            return u"Regular"


class Photo(TumbleItem):
    source = models.URLField(blank=True)
    photo = models.ImageField(upload_to="/photos", blank=True)
    caption = models.TextField(blank=True)
    click_through_url = models.URLField(blank=True)

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                if self.source:
                    post = api.write_photo(source=self.source, caption=self.caption, click_through_url=self.click_through_url)
                elif self.photo:
                    post = api.write_photo(data=open(self.photo), caption=self.caption, click_through_url=self.click_through_url)
                self.tumblr_id = post['id']
        super(Photo, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Photo, self).save()

    def __unicode__(self):
        return u"Photo"


class Quote(TumbleItem):
    quote = models.TextField()
    source = models.TextField(blank=True)

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_quote(quote=self.quote, source=self.source)
                self.tumblr_id = post['id']
        super(Quote, self).save()

    def __unicode__(self):
        return u"Quote"


class Link(TumbleItem):
    name = models.CharField(max_length=500, blank=True)
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_link(name=self.name, url=self.url, description=self.description)
                self.tumblr_id = post['id']
        super(Link, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Link, self).save()

    def __unicode__(self):
        if self.name:
            return u"%s (link)" % self.name
        else:
            return u"Link"


class Conversation(TumbleItem):
    title = models.CharField(max_length=500, blank=True)
    conversation_text = models.TextField()

    def save(self):
        try:
            self.conversationline_set.all().delete()
        except:
            pass
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_conversation(title=self.title, conversation=self.conversation_text)
                self.tumblr_id = post['id']
        super(Conversation, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Conversation, self).save()

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


class Video(TumbleItem):
    embed = models.TextField(blank=True)
    data = models.FileField(blank=True, upload_to='/videos')
    title = models.CharField(blank=True, max_length=250)
    caption = models.TextField(blank=True)

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_video(name=self.name, url=self.url, description=self.description)
                self.tumblr_id = post['id']
        super(Video, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Video, self).save()

    def __unicode__(self):
        return u"Video"


class Audio(TumbleItem):
    data = models.FileField(upload_to='/audio', blank=True)
    embed = models.TextField(blank=True)
    caption = models.TextField(blank=True)

    class Meta: #(TumbleItem.Meta):
        ordering = ['-pub_date']
        verbose_name_plural = "Audio"

    def save(self):
        api = get_user_api(self.user.username)
        if api:
            if not self.tumblr_id:
                post = api.write_audio(name=self.name, url=self.url, description=self.description)
                self.tumblr_id = post['id']
        super(Audio, self).save()

        if not self.content_id:
            self.content_id = self.pk
            super(Audio, self).save()

    def __unicode__(self):
        return u"Audio"
