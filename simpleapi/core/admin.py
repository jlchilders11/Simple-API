from django.contrib import admin
from .models import File

# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	readonly_fields = ('modified', 'path', )
	fields  = ('name', 'file_type', 'path', 'modified')