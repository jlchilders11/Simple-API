from rest_framework import serializers

from .models import File

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file_type', 'content', 'path']

class FileListSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = File
		fields = ['id', 'name']

class FilePostSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(max_length=256)
	file_type = serializers.IntegerField()
	content = serializers.FileField()
	comment = 'stuff and things'