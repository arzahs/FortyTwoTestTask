from django.test import TestCase
from django.core.urlresolvers import reverse
# Create your tests here.


class BioTests(TestCase):

    def test_page(self):
        "testing html layout"
        response = self.client.get(reverse('about_me'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Name', response.content)

    def test_view(self):
        response = self.client.get(reverse('about_me'))
        self.assertIn('person', response.context)
        self.assertIn('name', response.context['person'])