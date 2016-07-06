# coding: utf-8
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from apps.bio.models import ChangesEntry


@receiver(post_save)
def post_save_signal(sender, created, **kwargs):
    tables = connection.introspection.table_names()
    if sender.__name__ != 'ChangesEntry' and 'bio_changesentry' in tables:
            if not created:
                ChangesEntry.objects.create(name=sender.__name__,
                                            action='update')
            else:
                ChangesEntry.objects.create(name=sender.__name__,
                                            action='create')

    return 0


@receiver(post_delete)
def post_delete_signal(sender, **kwargs):
    if sender.__name__ != 'ChangesEntry':
        ChangesEntry.objects.create(
            name=sender.__name__, action='delete'
        )

    return 0
