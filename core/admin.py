from django.contrib import admin
from .models import Series

# Register your models here.

class SeriesAdmin(admin.ModelAdmin):
    model = Series

admin.site.register(Series)
