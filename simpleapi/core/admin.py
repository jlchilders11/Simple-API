from django.contrib import admin
from django.forms import ModelForm, CharField, ValidationError

import os

from .models import File

# Register your models here.

class FileAdminForm(ModelForm):
	def save(self, commit=True):

		m = super(FileAdminForm, self).save(commit=False)

		path_var = self.cleaned_data['path']
		self.instance.content.name = path_var

		if commit:
			m.save()
		return m

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)

		if instance:
			kwargs.update(initial={
					'path': instance.content.path
			})

		form = super(FileAdminForm, self).__init__(*args, **kwargs)

	def clean(self):
		
		cleaned_data = super().clean()
		path_var = os.path.dirname(cleaned_data.get('path'))
		if not os.access(path_var, os.W_OK):
			raise ValidationError(
				"Cannot write to {}".format(path_var)
			)
			
			
	path = CharField(required=True)
	class Meta:
		model = File
		fields  = ('name', 'file_type', 'path', 'content')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	form = FileAdminForm
	readonly_fields = ('modified',)
	fields  = ('name', 'file_type', 'path', 'content', 'modified')