from django.contrib import admin
from apps.bio.models import Person
from apps.bio.models import Request

admin.site.register(Person)
admin.site.register(Request)
