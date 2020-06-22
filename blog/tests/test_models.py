from django.test import TestCase
from blog.tests.factories import PostFactory
from blog.models import Post
import pytest

blog_schema = {

}

pytestmark = pytest.mark.django_db

class TestPostModel:
    def test_post_factory(self, post_factory):
        """
        Makes sure post_factory fixture is properly set up
        """
        assert type(post_factory) == type(PostFactory)

    def test_post(self, post):
        """
        Instances become fixtures automatically
        """
        assert isinstance(post, Post)

    @pytest.mark.parametrize("post__headline", ["PyTest for Dummies"])
    @pytest.mark.parametrize("post__content", ["Testing content"])
    def test_post_creation(self, post):
        assert post.headline == "PyTest for Dummies"
        assert post.content == "Testing content"

    def test_add_and_remove_posts_series(self, series):
        posts = [PostFactory() for _ in range(5)]
        for post in posts:
            series.posts.add(post)
        
        assert series.posts.count() == 5

        for post in posts[:2]:
            series.posts.remove(post)

        assert series.posts.count() == 3

    def test_sd_schema(self, complete_post):
        
        assert complete_post.sd

    def test_tag_names_as_list(self, post_factory):
        post= post_factory()
        post.tags.add(*['tag4', 'tag1', 'tag3', 'tag2'])
        assert post.tag_names_as_list() == ['tag1', 'tag2', 'tag3', 'tag4']
    
    def test_content_words_as_list(self, post_factory):
        post = post_factory(content="<div>test post</div>")
        assert post.content_words_as_list() == ['test', 'post']

    def test_post_manager(self, ten_posts):
        for post in ten_posts:
            assert post.is_published

    def test_post_get_image_url(self, post_factory, public_image_factory):
        public_image = public_image_factory()
        post = post_factory()
        assert post.get_image_url() == ''

        post.image = public_image
        post.save()
        assert post.get_image_url() == public_image.upload.url

    def test_post_get_author_name(self, post_factory, admin_user):
        post = post_factory()
        assert post.get_author_name() == ''

        post.author = admin_user

        assert post.get_author_name() == admin_user.username
