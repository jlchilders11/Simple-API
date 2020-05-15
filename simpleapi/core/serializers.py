'''
Home for all of our serializers
we use a few different ones for each of our methods
'''
import base64
import os

from rest_framework import serializers
from rest_framework import exceptions

from .models import File

class FileAsStringField(serializers.Field):
    '''
    Serialize a File as a string, based on its type
    '''
    def get_attribute(self, instance):
        #return the whole object so that we can see our file_type
        #and serialize properly
        return instance

    def to_representation(self, value):
        '''
        Return our value in different ways, based on file type
        mainly converts to base64 if it is a binary file
        '''
        if value.file_type == 0:
            return value.content.read()
        elif value.file_type == 1:
            return value.content.read()
        else:
            return base64.b64encode(value.content.read())

class FileSerializer(serializers.ModelSerializer):
    '''
    Our default serializer for reading our content
    '''
    path = serializers.CharField(source='content.path')
    content = FileAsStringField()
    modified = serializers.ReadOnlyField()

    class Meta: #pylint: disable=too-few-public-methods disable=missing-class-docstring
        model = File
        fields = ['name', 'file_type', 'path', 'modified', 'content']

class FileListSerializer(serializers.ModelSerializer):
    '''
    When serializing for a list, return on the id and name so it is not overly large
    '''
    class Meta: #pylint: disable=too-few-public-methods disable=missing-class-docstring
        model = File
        fields = ['id', 'name']

class FilePostSerializer(serializers.ModelSerializer):
    '''
    Serializer for handling our uploads and replaces,
    it sets the path equal to a  non model path field
    '''
    path = serializers.CharField(source='content.path', required=True)

    def validate_path(self, value):
        '''
        Makes sure we can write to the provided path, raises 403 if we can't
        '''
        path_var = os.path.dirname(value)
        if not os.access(path_var, os.W_OK):
            raise exceptions.PermissionDenied(
                "Cannot write to {}".format(path_var)
            )

    def to_internal_value(self, data):
        '''
        Changes our uploaded files path to the included path
        '''
        internal_value = super(FilePostSerializer, self).to_internal_value(data)
        path = data.get('path')
        internal_value['content']._name = path
        return internal_value

    class Meta: #pylint: disable=too-few-public-methods disable=missing-class-docstring
        model = File
        fields = ['name', 'file_type', 'path', 'content']
