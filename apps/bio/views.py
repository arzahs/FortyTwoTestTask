# coding: utf-8
import json
import os
from PIL import Image
from django.conf import settings
from datetime import date
from django.views.generic import View, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
            if person.photo:
                url = person.photo.url
            else:
                url = ''
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
                'photo': url

            }), mimetype="application/json")

        return render_to_response("bio/about_me.html",
                                  {'person': person},
                                  context_instance=RequestContext(request))


class RequestList(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestList, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get('id'):
            last_id = int(request.GET.get('id'))
            if not request.GET.get('priority'):
                requests = Request.objects.filter(id__gt=last_id)
            elif request.GET.get('priority') == 'desc':
                requests = Request.objects.order_by('-priority')[:10]
            elif request.GET.get('priority') == 'asc':
                requests = Request.objects.order_by('priority')[:10]
            if requests.count() > 0:
                data = serializers.serialize('json', requests)
                data = json.loads(data)
                requests = json.dumps(data)
                return HttpResponse(requests, mimetype="application/json")
            return HttpResponse({}, mimetype="application/json")
        else:
            requests = Request.objects.all().order_by('-date')[:10]

        csrf = request.COOKIES.get('csrftoken')
        return render_to_response("bio/requests.html", {"requests": requests,
                                                        'csrf': csrf})

    def post(self, request, *args, **kwargs):
        if request.POST.get('id') and request.POST.get('priority'):
            request_id = request.POST.get('id')
            req = Request.objects.get(id=request_id)
            req.priority = int(request.POST.get('priority'))
            req.save()
            return HttpResponse({'status': 'ok'}, mimetype="application/json")

        return HttpResponseBadRequest(json.dumps({'status': 'error'}))


class EditPersonView(FormView):
    form_class = EditPersonForm
    template_name = "bio/edit_profile.html"

    @method_decorator(login_required)
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
            return HttpResponseBadRequest(json.dumps({'errors': errors_dict,
                                                      'result': 'error'}))
        if person.photo:
            path = os.path.join(settings.BASE_DIR, person.photo.path)
            img = Image.open(path)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            img.save(path)
        return redirect('about_me')
