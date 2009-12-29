from django import template
from django.db import models
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType


Item = models.get_model("djumblr", "tumbleitem")
register = template.Library()


def tumblr_render(parser, token):
    bits = token.split_contents()    
    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r tag takes at least one argument" % bits[0])

    item = bits[1]
    args = {}

    # Parse out extra clauses if given
    if len(bits) > 2:
        biter = iter(bits[2:])
        for bit in biter:
            if bit == "using":
                args["using"] = biter.next()
            elif bit == "as":
                args["asvar"] = biter.next()
            else:
                raise template.TemplateSyntaxError("%r tag got an unknown argument: %r" % (bits[0], bit))

    return TumblrRenderNode(item, **args)

tumblr_render = register.tag(tumblr_render)


class TumblrRenderNode(template.Node):
    def __init__(self, item, using=None, asvar=None):
        self.item = item
        self.using = using
        self.asvar = asvar

    def render(self, context):
        try:
            item = template.resolve_variable(self.item, context)
        except template.VariableDoesNotExist:
            return ""

        if isinstance(item, Item):
            object = item

        # If the item isn't an Item, try to look one up.
        else:
            object = item
            ct = ContentType.objects.get_for_model(item)
            try:
                item = Item.objects.get(content_type=ct, object_id=object._get_pk_val())
            except Item.DoesNotExist:
                return ""

        # Figure out which templates to use
        template_list = [
            "djumblr/display/%s.html" % item.content_type.name,
            "djumblr/display/generic.html"
        ]
        if self.using:
            try:
                using = template.resolve_variable(self.using, context)
            except template.VariableDoesNotExist:
                pass
            else:
                template_list.insert(0, using)

        # Render content, and save to self.asvar if requested
        context.push()
        context.update({
            "item" : item,
            "object" : object
        })
        rendered = render_to_string(template_list, context)
        context.pop()
        if self.asvar:
            context[self.asvar] = rendered
            return ""
        else:
            return rendered
