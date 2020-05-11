from rest_framework import viewsets
from rest_framework import permissions 
from rest_framework.response import Response
from .models import File 
from .serializers import FileSerializer, FileListSerializer, FilePostSerializer

class FileViewSet(viewsets.ModelViewSet):
	queryset = File.objects.all()
	serializer_class = FileSerializer
	permission_classes = [permissions.IsAuthenticated]

	def list(self, request):
		serializer = FileListSerializer(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		instance = self.get_object()
		serializer = FilePostSerializer(instance)
		return Response(serializer.data)
