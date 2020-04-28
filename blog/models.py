from django.db import models
from taggit.managers import TaggableManager
from tinymce import HTMLField
from core.models import BasicTag, TaggedWhatever
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from core.models import CreatedModified

# Create your models here.
# Models for blogs

class Post(CreatedModified):
    name = models.CharField(max_length=300, unique=True, verbose_name=_('Name'))
    image = models.OneToOneField('core.PublicImage', on_delete=models.SET_NULL, blank=True, null=True)
    summary = models.TextField(default='', verbose_name=_('Summary'), blank=True, null=True)
    text = HTMLField(default='', verbose_name=_('Text'), blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    tags = TaggableManager(through=TaggedWhatever, blank=True)
    slug = models.SlugField(max_length=100, editable=False)
    series = models.ForeignKey('core.Series', on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    def __str__(self):
        return self.name + ' | ' + str(self.created_at)

    class Meta:
        ordering = ['name']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')