from PIL import Image, ImageOps
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.bio.models import Person


@receiver(post_save, sender=Person)
def resize_photo(sender, instance, **kwargs):
    size = (200, 200)
    if instance.profile_picture:
        path = instance.photo.path
        img = Image.open(path)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(path)
