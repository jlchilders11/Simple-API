from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, FormView

from rest_framework import viewsets, permissions, authentication
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import File 
from .serializers import FileSerializer, FileListSerializer, FilePostSerializer

class FileViewSet(viewsets.ModelViewSet):
	queryset = File.objects.all()
	serializer_class = FileSerializer
	authentication_classes = [authentication.BasicAuthentication, authentication.TokenAuthentication,]
	permission_classes = [permissions.IsAuthenticated]

	def list(self, request):
		serializer = FileListSerializer(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		instance = self.get_object()
		serializer = FilePostSerializer(instance)
		new_dict = dict()
		new_dict.update(serializer.data)
		new_dict['extra'] = "things"
		return Response(new_dict)

class AuthTokenListView(ListView):
	model = Token

class AuthTokenDeleteView(DeleteView):
	slug_field = 'user_id'
	model = Token
	success_url = reverse_lazy('TokenList')

class AuthTokenCreateView(CreateView):
	model = Token
	fields = ['user']
	success_url = reverse_lazy('TokenList')

class LoginView(FormView):
	template_name = 'login.html'
	form_class = AuthenticationForm
	success_url = reverse_lazy('TokenList')