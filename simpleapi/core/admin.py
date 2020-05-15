'''
Django admin files for the Simple API project
'''
import os

from django.contrib import admin
from django.forms import ModelForm, CharField, ValidationError

from .models import File

class FileAdminForm(ModelForm):
    '''
    A custom admin form for handling where custom path saving for documents
    '''
    def save(self, commit=True):
        '''
        To avoid saving the path to a file in the database twice, we
        pull it out of the form data and append it here
        '''
        model = super(FileAdminForm, self).save(commit=False)
        path_var = self.cleaned_data['path']
        self.instance.content.name = path_var

        if commit:
            model.save()
        return model

    def __init__(self, *args, **kwargs):
        '''
        Set our path to the pre existing path to the file
        as the default
        '''
        instance = kwargs.get('instance', None)

        if instance:
            kwargs.update(initial={
                'path': instance.content.path
            })

        super(FileAdminForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        Validate that we can write to the chosen path
        '''
        cleaned_data = super().clean()
        path_var = os.path.dirname(cleaned_data.get('path'))
        if not os.access(path_var, os.W_OK):
            raise ValidationError(
                "Cannot write to {}".format(path_var)
            )

    path = CharField(required=True)
    class Meta: # pylint: disable=too-few-public-methods disable=missing-class-docstring
        model = File
        fields = ('name', 'file_type', 'path', 'content')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    '''
    Admin file for File class
    uses our form above, and also appends the modified field
    '''
    form = FileAdminForm
    readonly_fields = ('modified',)
    fields = ('name', 'file_type', 'path', 'content', 'modified')
