from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    TaskViewSet, 
    UploadedImageViewSet, 
    AnnotationPolygonViewSet, 
    RegisterView,
    EmailTokenObtainPairView
)

# রাউটার সেটআপ
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'images', UploadedImageViewSet, basename='image')
router.register(r'polygons', AnnotationPolygonViewSet, basename='polygon')

urlpatterns = [
    # রাউটার ইউআরএল
    path('', include(router.urls)),
    
    # Auth পাথসমূহ
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]