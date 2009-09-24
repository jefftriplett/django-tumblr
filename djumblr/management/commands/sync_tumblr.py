import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from djumblr.models import Regular, Photo, Quote, Link, Conversation, Audio, Video, ConversationLine, TumbleItem
from tumblr import Api


LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.WARN
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Command(NoArgsCommand):
    help = ""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.log = logging.getLogger('djumblr.management.commands.sync_tumblr')

    def handle_noargs(self, **options):
        self.populate_all()

    def populate_models(self, tumblr_user, user):
        '''
        Takes a tumblr username (string), and a User model. Populates the tumblr models
        with data from 'tumblr_user'.tumblr.com, and associates the entries with 'user'.
        '''

        tumbls = Api(tumblr_user + ".tumblr.com")
        for tumbl in tumbls.read():
            # Common to all models
            tumblr_id = tumbl['id']
            pub_date = datetime.datetime.strptime(tumbl['date-gmt'], '%Y-%m-%d %H:%M:%S %Z')

            self.log.debug('%s' % (tumblr_id))

            try:
                TumbleItem.objects.get(tumblr_id=tumblr_id)

            except TumbleItem.DoesNotExist:
                try:
                    # 'Regular' objects.
                    if tumbl['type'] == "regular":
                        if tumbl['regular-title']:
                            title = tumbl['regular-title']
                        else:
                            title = ""
                        body = tumbl['regular-body']
                        m = Regular(tumblr_id=tumblr_id, pub_date=pub_date, user=user, title=title, body=body)

                    # 'Photo' objects.
                    elif tumbl['type'] == "photo":
                        source = tumbl['photo-url-250']
                        if tumbl['photo-caption']:
                            caption = tumbl['photo-caption']
                        else:
                            caption = ""
                        m = Photo(tumblr_id=tumblr_id, pub_date=pub_date, user=user, source=source, caption=caption)

                    # 'Quote' objects.
                    elif tumbl['type'] == "quote":
                        quote = tumbl['quote-text']
                        if tumbl['quote-source']:
                            source = tumbl['quote-source']
                        else:
                            source = ""
                        m = Quote(tumblr_id=tumblr_id, pub_date=pub_date, user=user, quote=quote, source=source)

                    # 'Link' objects.
                    elif tumbl['type'] == "link":
                        if tumbl['link-text']:
                            name = tumbl['link-text']
                        else:
                            name = ""
                        url = tumbl['link-url']
                        if tumbl['link-description']:
                            description = tumbl['link-description']
                        else:
                            description = ""
                        m = Link(tumblr_id=tumblr_id, pub_date=pub_date, user=user, name=name, url=url, description=description)

                    # 'Conversation' objects.
                    elif tumbl['type'] == "conversation":
                        if tumbl['conversation-title']:
                            title = tumbl['conversation-title']
                        else:
                            title = ""
                        m = Conversation(tumblr_id=tumblr_id, pub_date=pub_date, user=user, title=title, conversation_text=tumbl['conversation-text'])
                        #m.save()

                    # 'Video' objects.
                    elif tumbl['type'] == "video":
                        embed = tumbl['video-player']
                        if tumbl['video-caption']:
                            caption = tumbl['video-caption']
                        else:
                            caption = ""
                        m = Video(tumblr_id=tumblr_id, pub_date=pub_date, user=user, embed=embed, caption=caption)

                    # 'Audio' objects.
                    elif tumbl['type'] == "audio":
                        embed = tumbl['audio-player']
                        if tumbl['audio-caption']:
                            caption = tumbl['audio-caption']
                        else:
                            caption = ""
                        m = Audio(tumblr_id=tumblr_id, pub_date=pub_date, user=user, embed=embed, caption=caption)

                    # TODO: Raise error.
                    else:
                        print "ERROR!", tumbl
                        return ''

                    m.save()

                except Exception, e:
                    self.log.exception(e)

    def populate_all(self):
        '''
        Loops through all the users defined in TUMBLR_USERS in the main settings file.

        TUMBLR_USERS should be a dictionary of dictionaries, each with a django User.username
        as key, and at least a 'tumblr_user'. (Optionally, the tumblr user's 'email'' and 
        'password' can be included, but these are only used for posting.)

        Example:
        John has the username 'john' on his django website, but 'ignorantcarrot' on tumblr.
        His TUMBLR_USERS would be:

        TUMBLR_USERS = { 'john': 
                                { 'tumblr_user': 'ignorantcarrot', }
                       }

        If he wants to use the django site both for posting and syncing, he would have to 
        update the TUMBLR_USERS variable with the email address and password he uses to
        log in to tumblr.com:

        TUMBLR_USERS = { 'john': 
                                { 'tumblr_user': 'ignorantcarrot',
                                  'email': 'john.carrot@fullbladder.net',
                                  'password': 'secret',
                                }
                       }

        '''

        for username, tumblr_info in settings.TUMBLR_USERS.iteritems():
            user = User.objects.get(username__exact=username)

            populate_models(tumblr_info['tumblr_user'], user)
