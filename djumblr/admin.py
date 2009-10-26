from django.contrib import admin

from djumblr.models import Regular, Photo, Quote, Link, Conversation, Video, Audio, TumbleItem


class TumbleItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('tumblr_id', 'pub_date', 'user', 'content_type')


admin.site.register(TumbleItem, TumbleItemAdmin)
admin.site.register(Regular)
admin.site.register(Photo)
admin.site.register(Quote)
admin.site.register(Link)
admin.site.register(Conversation)
admin.site.register(Video)
admin.site.register(Audio)
