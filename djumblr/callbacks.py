from django.conf import settings
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


def tumbleitem_saved_callback(sender, **kwargs):
    instance = kwargs['instance']

    if not instance.object_id:
        instance.object_id = instance.pk
        instance.save()

    if not instance.tumblr_id:
        content_type = instance.content_type.name.lower()
        post = None
        api = get_user_api(instance.user.username)

        if api:
            if content_type == 'regular':
                post = api.write_regular(title=instance.title, body=instance.body)
            elif content_type == 'photo':
                if instance.source:
                    post = api.write_photo(source=instance.source, caption=instance.caption, click_through_url=instance.click_through_url)
                elif instance.photo:
                    post = api.write_photo(data=open(instance.photo), caption=instance.caption, click_through_url=instance.click_through_url)
            elif content_type == 'quote':
                post = api.write_quote(quote=instance.quote_text, source=instance.source)
            elif content_type == 'link':
                post = api.write_link(name=instance.name, url=instance.url, description=instance.description)
            elif content_type == 'conversation':
                post = api.write_conversation(title=instance.title, conversation=instance.conversation_text)
            elif content_type == 'video':
                post = api.write_video(name=instance.name, url=instance.url, description=instance.description)
            elif content_type == 'audio':
                post = api.write_audio(name=instance.name, url=instance.url, description=instance.description)

            if post:
                instance.tumblr_id = post['id']
                instance.save()


def tumbleitem_deleted_callback(sender, **kwargs):
    instance = kwargs['instance']
    print 'tumbleitem_deleted_callback'
    print instance
    print instance.content_type
