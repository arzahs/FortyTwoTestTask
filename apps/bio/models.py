# coding: utf-8
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255, default="")
    birthday = models.DateField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=255)
    bio = models.TextField()
    other_contacts = models.TextField()

    def __str__(self):
        return u"{0} {1}".format(self.last_name, self.name)

    class Meta:
        verbose_name = u"Person"
        verbose_name_plural = u"Persons"
