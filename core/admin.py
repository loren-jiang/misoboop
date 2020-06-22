from django.contrib import admin
from .models import Series, PublicImage, BasicTag
from sorl.thumbnail.admin import AdminImageMixin

# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    model = Series

class PublicImageInline(admin.StackedInline):
    model = PublicImage

class PublicImageAdmin(AdminImageMixin, admin.ModelAdmin):
    model = PublicImage

class BasicTagAdmin(admin.ModelAdmin):
    model = BasicTag


admin.site.register(Series)
admin.site.register(PublicImage, PublicImageAdmin)

admin.site.register(BasicTag, BasicTagAdmin)

