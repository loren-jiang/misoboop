from django.db import models
from taggit.managers import TaggableManager
from tinymce import HTMLField
from core.models import BasicTag, TaggedWhatever
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from core.models import CreatedModified
from core.utils import remove_html_tags, remove_backslash_escaped

# Create your models here.
# Models for blogs

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Post(CreatedModified):
    headline = models.CharField(max_length=300, unique=True, verbose_name=_('Headline'))
    alt_headline = models.CharField(max_length=300, verbose_name=_('Alternative headline'), blank=True, null=True)
    short_description = models.TextField(default='', blank=True, null=True)
    content = HTMLField(default='', verbose_name=_('Text'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    tags = TaggableManager(through=TaggedWhatever, blank=True)
    slug = models.SlugField(max_length=100, editable=False)
    series = models.ForeignKey('core.Series', on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    is_published = models.BooleanField(default=False)
    image = models.OneToOneField('core.PublicImage', on_delete=models.SET_NULL, blank=True, null=True)
    image_url = models.URLField(max_length=300, default="https://via.placeholder.com/150")
    objects = PostManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    def __str__(self):
        return self.headline + ' | ' + str(self.created_at.date())

    def tag_names_as_list(self):
        return [tag.name for tag in self.tags.order_by('name')]

    def content_words_as_list(self):
        return remove_backslash_escaped(remove_html_tags(self.content)).split()

    @property
    def sd(self):
        return {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": self.headline,
            "alternativeHeadline": self.alt_headline,
            "image": self.image.upload.url if self.image.upload else '',
            "award": "",
            "editor": self.author.name,
            "genre": "food",
            "keywords": ', '.join(self.tag_names_as_list()),
            "wordcount": len(self.content_words_as_list()),
            "publisher": "",
            "url": self.get_absolute_url(),
            "datePublished": self.created_at.date().isoformat(),
            "dateCreated": self.created_at.date().isoformat(),
            "dateModified": self.modified_at.date().isoformat(),
            "description": self.short_description,
            "articleBody": self.content, #todo: is this okay to put html tags inside
            "author": {
                "@type": "Person",
                "name": self.author.name
            }
        }


    class Meta:
        ordering = ['created_at', 'modified_at', 'headline']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
