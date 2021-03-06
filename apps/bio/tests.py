# coding utf-8
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.utils.six import StringIO
from apps.bio.models import Person
from apps.bio.models import Request, ChangesEntry
from apps.bio.forms import EditPersonForm
from apps.bio.templatetags.edit_link import edit_link
# Create your tests here.


class BioTests(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('about_me'))
        self.person, _ = Person.objects.get_or_create(
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

    def test_page(self):
        """testing html layout"""
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('Name', self.response.content)

    def test_view(self):
        """Test hard-coded data in view"""
        self.assertIn('person', self.response.context)
        self.assertIn(self.person.name, self.response.content)
        self.assertIn(self.person.last_name, self.response.content)
        self.assertIn(self.person.contacts, self.response.content)
        self.assertIn(self.person.bio, self.response.content)
        self.assertIn(self.person.email, self.response.content)
        self.assertIn(self.person.jabber, self.response.content)
        self.assertIn(self.person.skype, self.response.content)
        self.assertIn(self.person.other_contacts, self.response.content)

    def test_person(self):
        """Test model person """
        self.assertEqual(self.person.__str__(),
                         u"{0} {1}".format(self.person.last_name,
                                           self.person.name))


class RequestTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.response = self.client.get(reverse('requests_list'))
        self.req, _ = Request.objects.get_or_create(
            id=1,
            method='POST',
            path='/test/',
            status_code='200',
            server_protocol='http',
            content_len='1200'
        )

    def test_context_data(self):
        """ Test hard-coded data """
        self.assertEqual(self.response.status_code, 200)
        self.assertIn("requests", self.response.context)

    def test_model_request(self):
        """ Test model Request """
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 1)

    def test_middleware(self):
        """Test middleware that save request in DB"""
        self.client.get(reverse('requests_list'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 1)
        self.client.get(reverse('about_me'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 2)
        self.client.get(reverse('about_me'))
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 3)

    def test_view_requests(self):
        """Test for view, that use model Request"""
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

    def test_request_priority(self):
        """ Test for RequestList view that changes priority request"""
        self.assertEqual(self.req.priority, 0)
        self.response = self.client.post(reverse('requests_list'), {
            'id': '1',
            'priority': '3'
        })
        request = Request.objects.get(id=1)
        self.assertEqual(request.priority, 3)


class EditFormTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.person, _ = Person.objects.get_or_create(
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

    def test_edit(self):
        """ Test for view that edit main page """
        self.client.login(username='admin', password='admin')
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

    def setUp(self):
        self.person, _ = Person.objects.get_or_create(
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

    def test_admin_object_tag(self):
        """ Test for tag that return link to edit admin"""
        self.assertEqual(
            '<a href="/admin/bio/person/1/">admin</a>',
            edit_link(self.person))


class CommandTest(TestCase):

    def test_print_models_command(self):
        """ Test for command, that print count objects from all object"""
        out = StringIO()
        call_command('print_models', stdout=out)
        result = out.getvalue()
        self.assertTrue(result)
        self.assertIn('Model Person count objects: 0', result)


class EntryChangesTest(TestCase):

    def setUp(self):
        self.person = Person.objects.create(
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

    def test_model(self):
        """ Test for model ChangesEntry """
        entry, _ = ChangesEntry.objects.get_or_create(
            name='Name',
            action='create'
        )

        self.assertEqual(entry.__str__(),
                         u"{0} {1} {2}".format(entry.name,
                                               entry.action,
                                               entry.date))

    def test_creation_object(self):
        """
        Test for signal that create
        entry about create in ChangesEntry
        """
        ChangesEntry.objects.all().delete()
        self.assertEqual(ChangesEntry.objects.all().count(), 0)
        Request.objects.create(
            method='GET',
            path='/',
            status_code='200',
            server_protocol='http',
            content_len='1123'
        )
        self.assertEqual(ChangesEntry.objects.all().count(), 1)

    def test_update_object(self):
        """
        Test for signal that create
        entry about update object in ChangesEntry
        """
        ChangesEntry.objects.all().delete()
        self.assertEqual(ChangesEntry.objects.all().count(), 0)
        person = Person.objects.get(pk=1)
        person.name = "Test"
        person.save()
        self.assertEqual(ChangesEntry.objects.all().count(), 1)
        self.assertEqual(ChangesEntry.objects.get(pk=1).action, u'update')

    def test_delete_object(self):
        """
        Test for signal that create
        entry about deleting object in ChangesEntry
        """
        ChangesEntry.objects.all().delete()
        self.assertEqual(ChangesEntry.objects.all().count(), 0)
        self.person.delete()
        self.assertEqual(ChangesEntry.objects.all().count(), 1)
        self.assertEqual(ChangesEntry.objects.get(pk=1).action, u'delete')
