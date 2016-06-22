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


class Request(models.Model):
    method = models.CharField(max_length=4)
    path = models.CharField(max_length=100)
    status_code = models.CharField(max_length=3)
    server_protocol = models.CharField(max_length=3)
    content_len = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"{0} {1} {2}".format(self.method, self.path, self.date)

    class Meta:
        verbose_name = u"Request"
        verbose_name_plural = u"Requests"
