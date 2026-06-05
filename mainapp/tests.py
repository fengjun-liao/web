from django.test import TestCase
from django.urls import reverse


class MainAppViewsTests(TestCase):
    def test_index_page_renders(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Test Website")
        self.assertContains(response, "About this site")

    def test_about_page_renders(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About the Test Website")
        self.assertContains(response, "This sample site shows a basic Django view")
