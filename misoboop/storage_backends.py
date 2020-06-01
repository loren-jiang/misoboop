from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import get_storage_class
import copy

class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False

class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class CachedS3Boto3Storage(S3Boto3Storage):
    """
    S3 storage backend that saves the files locally, too.
    """

    location = settings.STATIC_LOCATION
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        super(CachedS3Boto3Storage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    # def save(self, name, content):
    #     self.local_storage._save(name, content)
    #     super(CachedS3Boto3Storage, self).save(name, self.local_storage._open(name))
    #     return name

    # https://github.com/django-compressor/django-compressor/issues/404
    def save(self, name, content):
        non_gzipped_file_content = content.file
        name = super(CachedS3Boto3Storage, self).save(name, content)
        content.file = non_gzipped_file_content
        self.local_storage._save(name, content)
        return name