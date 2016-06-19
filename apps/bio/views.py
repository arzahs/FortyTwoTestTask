# coding: utf-8
from django.views.generic import View
from django.shortcuts import render_to_response



class AboutMe(View):

    def get(self, request, *args, **kwargs):
        person = {"name": 'Sergey',
                  "last_name": 'Nelepa',
                  "contacts": "+380664290126",
                  "email": "nelepa1995@mail.ru",
                  "jabber": "arzahs@42cc.co",
                  "skype": "dgarzahs",
                  "birthday": "11.07.1995",
                  "bio": {
                      "wertewwrtwqerwqerwqer",
                      "afdsafasdfsadfasdfsadf",
                      "asdfsadfsdafsdfsdfsdfsd"
                          },
                  "other_contacts": {
                      "sadfsdfsdaf",
                      "asdfsadfasd",
                      "sadfsdfsdfas"
                  }

                  }
        return render_to_response("bio/about_me.html", {'person': person})


