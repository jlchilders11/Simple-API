from rest_framework import serializers

from .models import File

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['name', 'file_type', 'content', 'path']