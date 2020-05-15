'''
Defines what our app is called in settings
'''
from django.apps import AppConfig


class CoreConfig(AppConfig):
    '''
    Add core to installed apps to use this module
    '''
    name = 'core'
