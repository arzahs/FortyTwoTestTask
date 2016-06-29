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
    photo = models.ImageField(upload_to='person', blank=True, null=True)

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


class ChangesEntry(models.Model):
    name = models.CharField(max_length=250)
    action = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'{0} {1} {2}'.format(self.name, self.action, self.date)

    class Meta:
        verbose_name = u"Entry about changes"
        verbose_name_plural = u"Entries about changes"
