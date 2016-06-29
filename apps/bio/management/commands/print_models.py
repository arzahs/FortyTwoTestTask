# coding: utf-8
from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = u'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        for model in get_models():
            str = "Model {0} count objects: {1}".format(
                model.__name__, model.objects.count()
            )
            self.stdout.write(str)
            self.stderr.write("error: "+str)
