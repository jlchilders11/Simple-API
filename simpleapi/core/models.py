#django imports
from django.conf import settings
from django.db import models
from django.dispatch import receiver

#module imports
import arrow

#python imports
import os

# Create your models here.

class File(models.Model):
	FILE_TYPE_CHOICES = [
		(0, 'Text'),
		(1, 'Markdown'),
		(2, 'Binary'),
	]

	#human friendly name of our file
	name = models.CharField(max_length=256)
	#a choice of type for our file. Determines how it is returned by the API
	#types are defined in FILE_TYPE_CHOICES
	file_type = models.PositiveIntegerField(
		choices=FILE_TYPE_CHOICES, 
	)
	#our actual file
	content = models.FileField(
		unique=True
	)

	#calculated property that dynamically gets when a file was changed
	@property
	def modified(self):
		if(self.path):
			return arrow.get(
				os.path.getmtime(
					self.content.path
				)
			).format('M/D/YYYY h:mm A')
		else:
			return 'N/A'

	@property
	def path(self):
		return self.content.path
	
# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `File` object is deleted.
    """
    if instance.content:
        if os.path.isfile(instance.content.path):
            os.remove(instance.content.path)

@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `File` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).content
    except File.DoesNotExist:
        return False

    new_file = instance.path
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)