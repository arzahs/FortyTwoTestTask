from django.contrib import admin
from apps.bio.models import Person
from apps.bio.models import Request
from apps.bio.models import ChangesEntry


admin.site.register(Person)
admin.site.register(Request)
admin.site.register(ChangesEntry)
