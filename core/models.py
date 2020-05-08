from django.core.files.base import ContentFile
from django.db import models
import math
from django.utils.timezone import now
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField
from taggit.managers import TaggableManager
from misoboop.storage_backends import PrivateMediaStorage
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class BasicTag(TagBase):
    # ... fields here
    filterable = models.BooleanField(default=False)  # if tag is show on Recipe list filtering options
    shown = models.BooleanField(default=True)  # if tag is shown on Recipe detail page
    # objects = BasicTagManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedWhatever(GenericTaggedItemBase):
    tag = models.ForeignKey(
        BasicTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class NameDescription(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = HTMLField(default='', verbose_name=_('Text'))

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CreatedModified(models.Model):
    """
    Abstract base model for generic 'created_at' and 'modified_at' fields
    """

    # todo: add timezone support?
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Series(CreatedModified):
    """
    Model representing a 'Series', or collection of other models (many-to-one)
    """
    name = models.CharField(max_length=500, unique=True)
    description = HTMLField(default='', verbose_name=_('Text'))
    tags = TaggableManager(through=TaggedWhatever, blank=True)
    image = models.OneToOneField('core.PublicImage', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=100, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('series-detail', args=[self.slug])

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Seriess')


# Media models
class PublicImage(NameDescription):
    name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    description = HTMLField(default='', verbose_name=_('Text'), null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = ImageField()
    thumbnail = ImageField(null=True, blank=True)

    def __str__(self):
        splits = self.upload.url.split(settings.AWS_PUBLIC_MEDIA_LOCATION)
        if len(splits) > 1:
            return self.upload.url.split(settings.AWS_PUBLIC_MEDIA_LOCATION)[1]
        return self.upload.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # first save needed for get_thumbnail to also upload to s3
        if self.upload:
            self.thumbnail = get_thumbnail(self.upload, '300x300', quality=95, format='JPEG').name
        super().save(*args, **kwargs)


class PrivateImage(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    description = HTMLField(default='', verbose_name=_('Text'), null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = ImageField(storage=PrivateMediaStorage)
    user = models.ForeignKey(User, related_name='images', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        splits = self.upload.url.split(settings.AWS_PRIVATE_MEDIA_LOCATION)
        if len(splits) > 1:
            return self.upload.url.split(settings.AWS_PRIVATE_MEDIA_LOCATION)[1]
        return self.upload.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # first save needed for get_thumbnail to also upload to s3
        if self.upload:
            self.thumbnail = get_thumbnail(self.upload, '300x300', quality=95, format='JPEG').name
        super().save(*args, **kwargs)
