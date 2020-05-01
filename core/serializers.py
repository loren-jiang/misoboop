from rest_framework import routers, serializers, viewsets
from .models import PublicImage

class PublicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicImage
        exclude = ()