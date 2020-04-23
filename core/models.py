from django.db import models
import math
from django.utils.timezone import now
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField
from taggit.managers import TaggableManager

# Create your models here.
class BasicTag(TagBase):
    # ... fields here
    filterable = models.BooleanField(default=False) # if tag is show on Recipe list filtering options
    shown = models.BooleanField(default=True) # if tag is shown on Recipe detail page

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class TaggedWhatever(GenericTaggedItemBase):

    tag = models.ForeignKey(
        BasicTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '' #todo: implement

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Seriess')