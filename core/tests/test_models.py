import pytest
from django.conf import settings


pytestmark = pytest.mark.django_db


class TestPublicImageModel:
    def test_public_image_factory(self, public_image_factory):
        image = public_image_factory()
        location = image.upload.storage.location
        splits = image.upload.url.split(location)
        assert len(splits) > 0
        assert str(image) == splits[-1]