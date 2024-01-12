from rest_framework import serializers
from .models import Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images

        fields = ('id', 'photo', 'slug', 'description', 'image_size', 'dominant_color', 'average_color', 'image_palette',
                  'time_create', 'time_update', 'user_id',)