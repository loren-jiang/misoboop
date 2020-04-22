from django.db import models
import math
from django.utils.timezone import now
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _

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
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True