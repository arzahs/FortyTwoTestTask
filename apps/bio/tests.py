# coding utf-8
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.bio.models import Person
# Create your tests here.


class BioTests(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('about_me'))

    def test_page(self):
        """testing html layout"""
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('Name', self.response.content)

    def test_view(self):
        """Test hard-coded data in view"""

        self.assertIn('person', self.response.context)
        self.assertIn('name', self.response.context['person'])

    def test_person(self):
        """Test model person """
        person, _ = Person.objects.get_or_create(
            name="Sergey",
            last_name="Nelepa",
            contacts="+380664290126",
            birthday=date(1995, 11, 07),
            bio='Test data',
            email='nelepa1995@mail.ru',
            jabber='arzahs@jabber.ru',
            skype='skype',
            other_contacts='Test data'
        )
        self.assertEqual(person.__str__(), u"{0} {1}".format(person.last_name, person.name))


