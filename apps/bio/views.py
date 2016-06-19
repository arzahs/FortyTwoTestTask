# coding: utf-8
from datetime import date
from django.views.generic import View
from django.shortcuts import render_to_response
from apps.bio.models import Person


class AboutMe(View):

    def get(self, request, *args, **kwargs):
        person, _ = Person.objects.get_or_create(
            name="Sergey",
            last_name="Nelepa",
            contacts="+380664290126",
            birthday=date(1995, 07, 11),
            bio='Test data',
            email='nelepa1995@mail.ru',
            jabber='arzahs@jabber.ru',
            skype='skype',
            other_contacts='Test data',
        )
        return render_to_response("bio/about_me.html", {'person': person})


