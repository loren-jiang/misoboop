from django.urls import resolve, reverse
from django.test import TestCase
import pytest
from bs4 import BeautifulSoup
from recipe.views import home, about


pytestmark = pytest.mark.django_db

class TestHomeView:
    def test_home_url_resolves_to_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.resolver_match.func == home, "view should be a function view called home"

    def test_home_has_correct_view_name(self, client):
        response = client.get('/')
        assert 'home' == response.resolver_match.view_name, "view_name should be 'home'"

    def test_home_has_correct_template(self, client):
        response = client.get('/')
        assert 'home.html' in (
            t.name for t in response.templates), "home view uses correct html template home.html"

    def test_home_url_accessible_by_name(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200, "home url accessible by reverse('home')"

    def test_home_has_correct_title(self, client):
        response = client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert title[0].encode_contents() == b'MisoBoop', "title is MisoBoop"

    def test_home_url_contains_correct_context(self, client):
        response = client.get(reverse('home'))
        assert 'latest_recipes' in response.context, "context has 'latest_recipes'"
        assert 'latest_posts' in response.context, "context has 'latest_posts'"
        assert 'welcome_image' in response.context, "context has 'welcome_image'"

class TestAboutView:
    def test_about_url_resolves_to_home_page(self, client):
        response = client.get('/about/')
        assert response.status_code == 200
        assert response.resolver_match.func == about, "view should be a function view called about"

    def test_about_has_correct_view_name(self, client):
        response = client.get('/about/')
        assert 'about' == response.resolver_match.view_name, "view_name should be 'about'"

    def test_about_has_correct_template(self, client):
        response = client.get('/about/')
        assert 'about.html' in (
            t.name for t in response.templates), "about view uses correct html template about.html"

    def test_about_url_accessible_by_name(self, client):
        response = client.get(reverse('about'))
        assert response.status_code == 200, "about url accessible by reverse('about')"

    def test_about_has_correct_title(self, client):
        response = client.get('/about/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert b'MisoBoop | About' in title[0].encode_contents(), "title is MisoBoop | About"

