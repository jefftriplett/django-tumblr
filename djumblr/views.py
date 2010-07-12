from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import date_based, list_detail
from django.template import RequestContext

from djumblr.models import TumbleItem
from djumblr.models import Audio, Conversation, Link, Photo, Quote, Regular, Video
from djumblr.forms import AudioForm, ConversationForm, LinkForm, PhotoForm, QuoteForm, RegularForm, VideoForm


def tumble_object_list(request, page=0, content_type=None, template_name='djumblr/generic.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.filter(content_type__name=content_type)

    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 20,
        page = page,
        template_name = template_name,
        **kwargs
    )


def tumble_archive_index(request, page=0, content_type=None, template_name='djumblr/tumbleitem_archive.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.filter(content_type__name=content_type)

    return date_based.archive_index(
        request,
        date_field = 'pub_date',
        queryset = queryset,
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_year(request, year, content_type=None, template_name='djumblr/tumbleitem_archive_year.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.filter(content_type__name=content_type)

    return date_based.archive_year(
        request,
        year = year,
        date_field = 'pub_date',
        queryset = queryset,
        make_object_list = True,
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_month(request, year, month, content_type=None, template_name='djumblr/generic.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.filter(content_type__name=content_type)

    return date_based.archive_month(
        request,
        year = year,
        month = month,
        date_field = 'pub_date',
        queryset = queryset,
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_day(request, year, month, day, content_type=None, template_name='djumblr/generic.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.objects.filter(content_type__name=content_type)

    return date_based.archive_day(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'pub_date',
        queryset = queryset,
        template_name = template_name,
        **kwargs
    )


def tumble_item_detail(request, year, month, day, tumblr_id, content_type=None, template_name='djumblr/generic_detail.html', **kwargs):
    queryset = TumbleItem.objects.all()
    if content_type:
        queryset = queryset.filter(content_type__name=content_type)

    return date_based.object_detail(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'pub_date',
        slug_field = 'tumblr_id',
        slug = tumblr_id,
        queryset = queryset,
        template_name = template_name,
        **kwargs
    )


@login_required
def tumble_item_form(request):
    audio_form = AudioForm()
    conversation_form = ConversationForm()
    link_form = LinkForm()
    photo_form = PhotoForm()
    quote_form = QuoteForm()
    regular_form = RegularForm()
    video_form = VideoForm()

    if request.method == 'POST':
        new_data = request.POST.copy()
        our_forms = ('audio-form', 'conversation-form', 'link-form', 'photo-form', 'quote-form', 'regular-form', 'video-form')
        delete_forms = tuple('delete-%s' % x for x in our_forms)

        # Add forms
        if any(x in new_data for x in our_forms):
            if new_data.get('audio-form'):
                form = AudioForm(new_data)
                audio_form = form
            elif new_data.get('conversation-form'):
                form = form
                conversation_form = ConversationForm()
            elif new_data.get('link-form'):
                form = LinkForm(new_data)
                link_form = form
            elif new_data.get('photo-form'):
                form = PhotoForm(new_data)
                photo_form = form
            elif new_data.get('quote-form'):
                form = QuoteForm(new_data)
                quote_form = form
            elif new_data.get('regular-form'):
                form = RegularForm(new_data)
                regular_form = form
            elif new_data.get('video-form'):
                form = VideoForm(new_data)
                video_form = form

            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponseRedirect(request.path)

        # Delete forms
        elif any(x in new_data for x in delete_forms):
            delete_id = request.POST['delete_id']
            if new_data.get('delete-audio-form'):
                Audio.objects.get(id=delete_id).delete()
            elif new_data.get('delete-conversation-form'):
                Conversation.objects.get(id=delete_id).delete()
            elif new_data.get('delete-link-form'):
                Link.objects.get(id=delete_id).delete()
            elif new_data.get('delete-photo-form'):
                Photo.objects.get(id=delete_id).delete()
            elif new_data.get('delete-quote-form'):
                Quote.objects.get(id=delete_id).delete()
            elif new_data.get('delete-regular-form'):
                Regular.objects.get(id=delete_id).delete()
            elif new_data.get('delete-video-form'):
                Video.objects.get(id=delete_id).delete()

            return HttpResponseRedirect(request.path)

    return render_to_response('djumblr/tumbleitem_form.html', {
        'audio_form': audio_form,
        'conversation_form': conversation_form,
        'link_form': link_form,
        'photo_form': photo_form,
        'quote_form': quote_form,
        'regular_form': regular_form,
        'video_form': video_form,
    }, context_instance=RequestContext(request))
