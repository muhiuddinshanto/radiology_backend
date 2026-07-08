from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Task, UploadedImage, AnnotationPolygon
from .serializers import (
    TaskSerializer, 
    UploadedImageSerializer, 
    AnnotationPolygonSerializer,
    RegisterSerializer, 
    EmailTokenObtainPairSerializer,
)

# --- ViewSets ---

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all().order_by('-created_at')
        date_param = self.request.query_params.get('date', None)
        if date_param is not None:
            queryset = queryset.filter(due_date=date_param)
        return queryset

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all().order_by('uploaded_at')
    serializer_class = UploadedImageSerializer

class AnnotationPolygonViewSet(viewsets.ModelViewSet):
    queryset = AnnotationPolygon.objects.all()
    serializer_class = AnnotationPolygonSerializer

# --- Auth Views ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer