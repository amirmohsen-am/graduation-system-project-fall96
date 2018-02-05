# Amirmohsen Ahanchi

from django import template

register = template.Library()


@register.simple_tag
def is_active(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).view_name == view_name else ""
    except Resolver404:
        return ""
