# coding: utf-8
import json
from PIL import Image
from datetime import date
from django.views.generic import View, FormView
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from apps.bio.models import Person, Request
from apps.bio.forms import EditPersonForm


class AboutMe(View):

    def get(self, request, *args, **kwargs):
        try:
            person = Person.objects.get(pk=1)
        except ObjectDoesNotExist:
            person = Person.objects.create(
                pk=1,
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

        if request.is_ajax():
            return HttpResponse(json.dumps({
                'name': person.name,
                'last_name': person.last_name,
                'contacts': person.contacts,
                'birthday': str(person.birthday),
                'bio': person.bio,
                'email': person.email,
                'jabber': person.jabber,
                'skype': person.skype,
                'other_contacts': person.other_contacts,
                'photo': person.photo.url

            }), mimetype="application/json")

        return render_to_response("bio/about_me.html",
                                  {'person': person},
                                  context_instance=RequestContext(request))


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


class EditPersonView(FormView):
    form_class = EditPersonForm
    template_name = "bio/edit_profile.html"

    # def get_initial(self, form_class):
    #     p = Person.objects.get(pk=1)
    #     form = form_class(initial=p)
    #     return form

    def post(self, request, *args, **kwargs):
        person = Person.objects.get(pk=1)
        form = EditPersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
        else:
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = e
                    print "bad request"
            return HttpResponseBadRequest(json.dumps(errors_dict))
        # if person.photo.url:
        #     image = Image.open(person.photo.path)
        #     size = (200, 200)
        #     image.thumbnail(size, Image.ANTIALIAS)
        #     image.save(person.photo.url)
        return redirect('about_me')
