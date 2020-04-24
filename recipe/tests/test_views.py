from django.urls import resolve, reverse
from django.test import TestCase

from recipe.views import home, about

class HomePageTest(TestCase):

    def test_home_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home, "view should be function home")
        self.assertEqual('home', found.view_name, "view_name should be 'home'")

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_url_returns_correct_html(self):
        response = self.client.get(reverse('home'))
        html = response.content.decode('utf8')
        self.assertIn('<title>MisoBoop</title>', html)

    def test_home_url_contains_correct_context(self):
        response = self.client.get(reverse('home'))
        context = response.context
        self.assertTrue('latest_recipes' in context)
        self.assertTrue('latest_posts' in context)