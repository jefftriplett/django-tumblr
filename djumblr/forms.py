from django import forms
from djumblr.models import Audio, Conversation, Link, Photo, Quote, Regular, Video


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('data', 'embed', 'caption', 'tags')

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ('title', 'conversation_text', 'tags')

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('name', 'url', 'description', 'tags')

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('source', 'photo', 'caption', 'click_through_url', 'tags')

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('quote_text', 'source', 'tags')

class RegularForm(forms.ModelForm):
    class Meta:
        model = Regular
        fields = ('title', 'body', 'tags')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('embed', 'data', 'title', 'caption', 'tags')
