# coding utf-8
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.bio.models import Person
from apps.bio.models import Request
from apps.bio.forms import EditPersonForm
from apps.bio.templatetags.edit_link import edit_link
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
        person, _ = Person.objects.get_or_create(
            pk=1,
            name="Sergey",
            last_name="Nelepa",
            contacts="+380664290126",
            birthday=date(1995, 07, 11),
            bio='Test data',
            email='nelepa1995@mail.ru',
            jabber='arzahs@jabber.ru',
            skype='skype',
            other_contacts='Test data',
        )
        self.assertIn('person', self.response.context)
        self.assertIn(person.name, self.response.content)
        self.assertIn(person.last_name, self.response.content)
        self.assertIn(person.contacts, self.response.content)
        self.assertIn(person.bio, self.response.content)
        self.assertIn(person.email, self.response.content)
        self.assertIn(person.jabber, self.response.content)
        self.assertIn(person.skype, self.response.content)
        self.assertIn(person.other_contacts, self.response.content)

    def test_person(self):
        """Test model person """
        person = Person.objects.create(
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
        self.assertEqual(person.__str__(),
                         u"{0} {1}".format(person.last_name, person.name))


class RequestTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('requests_list'))

    def test_context_data(self):
        """ Test hard-coded data """
        self.assertEqual(self.response.status_code, 200)
        self.assertIn("requests", self.response.context)

    def test_model_request(self):
        """ Test model Request """
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 0)
        req, _ = Request.objects.get_or_create(
            id=1,
            method='POST',
            path='/test/',
            status_code='200',
            server_protocol='http',
            content_len='1200'
        )
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 1)

    def test_middleware(self):
        """Test middleware that save request in DB"""
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 0)
        self.response = self.client.get(reverse('requests_list'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 0)
        self.response = self.client.get(reverse('about_me'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 1)
        self.response = self.client.get(reverse('about_me'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 2)

    def test_view_requests(self):
        """Test for view, that use model Request"""
        self.response = self.client.get(reverse('about_me'))
        self.response = self.client.get(reverse('requests_list'))
        self.assertIn('requests', self.response.context)
        self.assertIn('200', self.response.content)
        req, _ = Request.objects.get_or_create(
            id=3,
            method='POST',
            path='/test/',
            status_code='200',
            server_protocol='http',
            content_len='1200'
        )
        self.response = self.client.get('{0}?id=1'.format(
            reverse('requests_list')
        ))
        self.assertIn(str(req.id), self.response.content)
        self.assertIn(req.method, self.response.content)
        self.assertIn(req.path, self.response.content)
        self.assertIn(req.status_code, self.response.content)
        self.assertIn(req.server_protocol, self.response.content)
        self.assertIn(req.content_len, self.response.content)


class EditFormTest(TestCase):

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_edit(self):
        """ Test for view that edit main page """
        self.client.login(username='admin', password='admin')
        person, _ = Person.objects.get_or_create(
            pk=1,
            name="Sergey",
            last_name="Nelepa",
            contacts="+380664290126",
            birthday=date(1995, 07, 11),
            bio='Test data',
            email='nelepa1995@mail.ru',
            jabber='arzahs@jabber.ru',
            skype='skype',
            other_contacts='Test data',
        )
        self.response = self.client.get(reverse('edit_form'))
        self.assertIn('form', self.response.context)
        self.response = self.client.post(reverse('edit_form'), {
            'name': "Sergey1",
            'last_name': "Nelepa1",
            'contacts': "+380664290126",
            'birthday': "1995-07-11",
            'bio': 'Test data',
            'email': 'nelepa1995@mail.ru',
            'jabber': 'arzahs@jabber.ru',
            'skype': 'skype',
            'other_contacts': 'Test data'})
        self.assertEqual(self.response.status_code, 302)

    def test_form(self):
        """ Test for edit main form """
        form = EditPersonForm(data={
            'name': "Sergey",
            'last_name': "Nelepa",
            'contacts': "+380664290126",
            'birthday': "1995-07-11",
            'bio': 'Test data',
            'email': 'nelepa1995@mail.ru',
            'jabber': 'arzahs@jabber.ru',
            'skype': 'skype',
            'other_contacts': 'Test data',
        })
        self.assertTrue(form.is_valid())


class AdminTagTest(TestCase):

    def test_admin_object_tag(self):
        """ Test for tag that return link to edit admin"""

        person, _ = Person.objects.get_or_create(
            pk=1,
            name="Sergey",
            last_name="Nelepa",
            contacts="+380664290126",
            birthday=date(1995, 07, 11),
            bio='Test data',
            email='nelepa1995@mail.ru',
            jabber='arzahs@jabber.ru',
            skype='skype',
            other_contacts='Test data',
        )
        self.assertEqual('<a href="/admin/bio/person/1/">admin</a>', edit_link(person))


