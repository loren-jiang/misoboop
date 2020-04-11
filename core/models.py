from django.db import models
import math
from django.utils.timezone import now

# Create your models here.

class CreatedModified(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True