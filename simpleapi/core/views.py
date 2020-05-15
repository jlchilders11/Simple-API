'''
Our view file for both the API and the token authentication backends
includes a custom login screen that sends people to the token list
'''
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView

from django_markup.markup import formatter
from rest_framework import viewsets, permissions, authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import File
from .serializers import FileSerializer, FileListSerializer, FilePostSerializer

class FileViewSet(viewsets.ModelViewSet):
    '''
    A viewset handing our interactions with the File API
    only allows get, post, and put
    '''
    queryset = File.objects.all()
    serializer_class = FileSerializer
    authentication_classes = [
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put']
    serializer_classes = {
        'list': FileListSerializer,
        'create': FilePostSerializer,
        'update': FilePostSerializer,
    }

    def retrieve(self, request, pk=None): #pylint: disable=unused-argument
        queryset = self.queryset
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer_class()
        data = dict()
        data.update(serializer(obj).data)
        if data['file_type'] == 1:
            data.update({
                'markdown': formatter(data['content'], filter_name='markdown')
            })
        return Response(data)

    def get_serializer_class(self):
        '''
        Set our serializer based on serializer_classes, defaults to serializer_class
        '''
        return self.serializer_classes.get(self.action, self.serializer_class)

class AuthTokenListView(LoginRequiredMixin, ListView):
    '''
    Class based list view for Token
    '''
    model = Token

class AuthTokenDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Class Based Delete view for Token
    '''
    slug_field = 'user_id'
    model = Token
    success_url = reverse_lazy('TokenList')

class AuthTokenCreateView(LoginRequiredMixin, CreateView):
    '''
    Class based delete view for Token
    '''
    model = Token
    fields = ['user']
    success_url = reverse_lazy('TokenList')

class CustomLoginView(LoginView):
    '''
    Overwrite the standard loginview to use a template,
    and to redirect to a different location
    '''
    template_name = 'login.html'

    def get_success_url(self):
        '''
        Redirect to our token list, or the next argument from the url
        '''
        url = self.get_redirect_url()
        return url or reverse_lazy('TokenList')
