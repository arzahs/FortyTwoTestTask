# coding: utf-8
from django.views.generic import TemplateView


class AboutMe(TemplateView):
    template_name = u"bio/about_me.html"

