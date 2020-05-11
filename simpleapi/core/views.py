from rest_framework import viewsets
from rest_framework import permissions 
from .models import File 
from .serializers import FileSerializer 

class FileViewSet(viewsets.ModelViewSet):
	queryset = File.objects.all()
	serializer_class = FileSerializer
	permissions_classes = [permissions.IsAuthenticated]