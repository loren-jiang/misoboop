import pytest
from bs4 import BeautifulSoup
from core.utils import strip_leading_trailing_spaces
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestBlogPostViews:
    def test_post_detail_absolute_url(self, client, post_factory):
        post = post_factory()
        response = client.get(post.get_absolute_url())
        assert response.status_code == 200

    def test_post_detail_has_correct_title(self, client, post_factory):
        post = post_factory(headline="test_post")
        response = client.get(post.get_absolute_url())
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert 'MisoBoop | test_post' == strip_leading_trailing_spaces(
            title[0].text), "title is MisoBoop | test_post"

    def test_post_list_url(self, client, ten_posts):
        response = client.get(reverse('post-list'))
        assert response.status_code == 200
        assert len(response.context['object_list']) == 10

