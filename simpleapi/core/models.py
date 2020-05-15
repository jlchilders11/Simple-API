'''
Our defined models for the Simple API
Contains the File class and its listeners
'''
# python imports
import os

# django imports
from django.db import models
from django.dispatch import receiver

# module imports
import arrow

class File(models.Model):
    '''
    This model represents a File on our Filesystem
    name: A human readable name for our lists
    file_type: determines how our file is stringified for return
    content: in the database this is our paht to our file, but also allows for using
        the file system to manipulate the object at the end of that path
    modified: This returns when the file was last modified, and is read only
    '''

    #Text: returns the plaintext read of the file
    #Markdown: returns the plaintext read of the file, plus the markdown as html
    #Binary: Returns the base64 string representation of the file
    FILE_TYPE_CHOICES = [
        (0, 'Text'),
        (1, 'Markdown'),
        (2, 'Binary'),
    ]

    name = models.CharField(max_length=256)
    file_type = models.PositiveIntegerField(
        choices=FILE_TYPE_CHOICES,
    )
    content = models.FileField(
        unique=True
    )
    @property
    def modified(self):
        '''
        Calculated property that gets the modified time from the OS
        and formats it nicely using arrow
        '''
        if self.content:
            return arrow.get(
                os.path.getmtime(
                    self.content.path # pylint: disable=no-member
                )
            ).format('M/D/YYYY h:mm A')
        return 'N/A'

# These two auto-delete files from filesystem when they are unneeded:


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs): # pylint: disable=unused-argument
    """
    Deletes file from filesystem
    when corresponding `File` object is deleted.
    """
    if instance.content:
        if os.path.isfile(instance.content.path):
            os.remove(instance.content.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs): # pylint: disable=unused-argument disable=inconsistent-return-statements
    """
    Deletes old file from filesystem
    when corresponding `File` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).content # pylint: disable=no-member
    except File.DoesNotExist: # pylint: disable=no-member
        return False

    new_file = instance.content
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
