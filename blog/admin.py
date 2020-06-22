from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    model = Post
    readonly_fields = ["slug"]

    def get_queryset(self, request):
        return Post.objects.all()

admin.site.register(Post, PostAdmin)
