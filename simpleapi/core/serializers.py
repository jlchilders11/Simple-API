from rest_framework import serializers

import base64

from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file_type', 'path', 'content']
        content = serializers.FileField()

class FileListSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = ['id', 'name']

class FileAsStringField(serializers.Field):
	'''
	Serialize a File as a string
	'''
	def get_attribute(self, instance):
		#return the whole object so that we can see our file_type 
		#and serialize properly
		return instance

	def to_representation(self, value):
		if value.file_type == 0:
			return value.content.read()
		elif value.file_type == 1:
			return value.content.read()
		else:
			return base64.b64encode(value.content.read())

class FilePostSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(max_length=256)
	file_type = serializers.IntegerField()
	content = FileAsStringField()