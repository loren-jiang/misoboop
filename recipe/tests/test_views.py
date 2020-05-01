from django.urls import resolve, reverse
from django.test import TestCase

from recipe.views import home, about

class HomePageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.response = self.client.get('/')

    def tearDown(self):
        pass

    def test_home_url_resolves_to_home_page(self):
        # response = self.client.get('/')
        self.assertEqual(self.response.resolver_match.func, home, "view should be a function view called home")

    def test_home_has_correct_view_name(self):
        # response = self.client.get('/')
        self.assertEqual('home', self.response.resolver_match.view_name, "view_name should be 'home'")

    def test_home_has_correct_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_has_correct_title(self):
        html = self.response.content.decode('utf8')
        self.assertInHTML('<title>MisoBoop</title>', html,1)

    def test_home_url_contains_correct_context(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('latest_recipes' in response.context)
        self.assertTrue('latest_posts' in response.context)
        self.assertTrue('welcome_image' in response.context)

class AboutPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.response = self.client.get('/about/')

    def tearDown(self):
        pass

    def test_about_url_resolves_to_about_page(self):
        # response = self.client.get('/about/')
        self.assertEqual(self.response.resolver_match.func, about, "view should be function view called about")

    def test_about_has_right_view_name(self):
        # response = self.client.get('/about/')
        self.assertEqual('about', self.response.resolver_match.view_name, "view_name should be 'about'")

    def test_about_has_correct_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_about_url_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_has_correct_title(self):
        html = self.response.content.decode('utf8')
        self.assertInHTML('<title>MisoBoop | About</title>', html,1)

