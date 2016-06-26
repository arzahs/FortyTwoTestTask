# coding: utf-8
from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
register = template.Library()

@register.simple_tag
def edit_link(object):
    url = reverse(u'admin:{0}_{1}_change'.format(object._meta.app_label, object._meta.module_name), args=[object.id] )
    return u'<a href="{0}">admin</a>'.format(url)
