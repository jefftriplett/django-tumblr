from django.views.generic import date_based, list_detail
from djumblr.models import TumbleItem


def tumble_object_list(request, page=0, **kwargs):
    return list_detail.object_list(
        request,
        queryset = TumbleItem.objects.all(),
        paginate_by = 20,
        page = page,
        template_name = template_name,
        **kwargs
    )


def tumble_archive_index(request, page=0, template_name='djumblr/tumbleitem_archive.html', **kwargs):
    return date_based.archive_index(
        request,
        date_field = 'pub_date',
        queryset = TumbleItem.objects.all(),
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_year(request, year, template_name='djumblr/tumbleitem_archive_year.html', **kwargs):
    return date_based.archive_year(
        request,
        year = year,
        date_field = 'pub_date',
        queryset = TumbleItem.objects.all(),
        make_object_list = True,
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_month(request, year, month, template_name='djumblr/generic.html', **kwargs):
    return date_based.archive_month(
        request,
        year = year,
        month = month,
        date_field = 'pub_date',
        queryset = TumbleItem.objects.all(),
        template_name = template_name,
        **kwargs
    )


def tumble_item_archive_day(request, year, month, day, template_name='djumblr/generic.html', **kwargs):
    return date_based.archive_day(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'pub_date',
        queryset = TumbleItem.objects.all(),
        template_name = template_name,
        **kwargs
    )


def tumble_item_detail(request, year, month, day, tumblr_id, template_name='djumblr/generic_detail.html', **kwargs):
    return date_based.object_detail(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'pub_date',
        slug_field = 'tumblr_id',
        slug = tumblr_id,
        queryset = TumbleItem.objects.all(),
        template_name = template_name,
        **kwargs
    )
