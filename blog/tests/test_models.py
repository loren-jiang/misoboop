from django.test import TestCase
from blog.tests.factories import PostFactory
from blog.models import Post
import pytest

blog_schema = {

}

pytestmark = pytest.mark.django_db

def test_post_factory(post_factory):
    """
    Makes sure post_factory fixture is properly set up
    """
    assert type(post_factory) == type(PostFactory)

def test_post(post):
    """
    Instances become fixtures automatically
    """
    assert isinstance(post, Post)

@pytest.mark.parametrize("post__headline", ["PyTest for Dummies"])
@pytest.mark.parametrize("post__content", ["Testing content"])
def test_post_creation(post):
    assert post.headline == "PyTest for Dummies"
    assert post.content == "Testing content"

def test_add_and_remove_posts_series(series):
    posts = [PostFactory() for _ in range(5)]
    for post in posts:
        series.posts.add(post)
    
    assert series.posts.count() == 5

    for post in posts[:2]:
        series.posts.remove(post)

    assert series.posts.count() == 3
