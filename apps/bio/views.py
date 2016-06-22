# coding: utf-8
import json
from datetime import date
from django.views.generic import View
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import HttpResponse
from apps.bio.models import Person, Request


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


class RequestList(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('id'):
            last_id = int(request.GET.get('id'))
            requests = Request.objects.filter(id__gt=last_id)
            if requests.count() > 0:
                data = serializers.serialize('json', requests)
                data = json.loads(data)
                requests = json.dumps(data)
                print requests
                return HttpResponse(requests, mimetype="application/json")
            return HttpResponse({}, mimetype="application/json")
        else:
            requests = Request.objects.all().order_by('-date')[:10]

        return render_to_response("bio/requests.html", {"requests": requests})
