import datetime
import logging
import optparse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from djumblr.models import Regular, Photo, Quote, Link, Conversation, Audio, Video, ConversationLine, TumbleItem
from tumblr import Api


class Command(BaseCommand):
    help = ""
    option_list = BaseCommand.option_list + (
        optparse.make_option(
            "-u", "--user", 
            dest="user", 
            action="store", 
            help="Sync tumblr with a given username"
        ),
    )

    def handle(self, *args, **options):
        level = {
            '0': logging.WARN, 
            '1': logging.INFO, 
            '2': logging.DEBUG
        }[options.get('verbosity', '0')]
        logging.basicConfig(level=level, format="%(name)s: %(levelname)s: %(message)s")
        self.log = logging.getLogger('djumblr.management.commands.sync_tumblr')
        self.populate_all()

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

            self.log.debug('%s (%s)' % (tumblr_id, tumbl['type']))

            try:
                TumbleItem.objects.get(tumblr_id=tumblr_id)

            except TumbleItem.DoesNotExist:
                try:
                    # 'Regular' objects.
                    if tumbl['type'] == "regular":
                        title = tumbl.get('regular-title', '')
                        body = tumbl['regular-body']
                        m = Regular(tumblr_id=tumblr_id, pub_date=pub_date, user=user, title=title, body=body)

                    # 'Photo' objects.
                    elif tumbl['type'] == "photo":
                        source = tumbl['photo-url-250']
                        caption = tumbl.get('photo-caption', '')
                        m = Photo(tumblr_id=tumblr_id, pub_date=pub_date, user=user, source=source, caption=caption)

                    # 'Quote' objects.
                    elif tumbl['type'] == "quote":
                        quote = tumbl.get('quote-text', '')
                        m = Quote(tumblr_id=tumblr_id, pub_date=pub_date, user=user, quote=quote, source=source)

                    # 'Link' objects.
                    elif tumbl['type'] == "link":
                        name = tumbl.get('link-text', '')
                        url = tumbl['link-url']
                        description = tumbl.get('link-description', '')
                        m = Link(tumblr_id=tumblr_id, pub_date=pub_date, user=user, name=name, url=url, description=description)

                    # 'Conversation' objects.
                    elif tumbl['type'] == "conversation":
                        title = tumbl.get('conversation-title', '')
                        m = Conversation(tumblr_id=tumblr_id, pub_date=pub_date, user=user, title=title, conversation_text=tumbl['conversation-text'])
                        #m.save()

                    # 'Video' objects.
                    elif tumbl['type'] == "video":
                        embed = tumbl['video-player']
                        caption = tumbl.get('video-caption', '')
                        m = Video(tumblr_id=tumblr_id, pub_date=pub_date, user=user, embed=embed, caption=caption)

                    # 'Audio' objects.
                    elif tumbl['type'] == "audio":
                        embed = tumbl['audio-player']
                        caption = tumbl.get('audio-caption', '')
                        m = Audio(tumblr_id=tumblr_id, pub_date=pub_date, user=user, embed=embed, caption=caption)

                    # TODO: Raise error.
                    else:
                        self.log.error('Type does not exist: %s' % (tumbl['type']))

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
            self.populate_models(tumblr_info['tumblr_user'], user)
