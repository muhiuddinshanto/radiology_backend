from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import EmailTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API অ্যাপের পাথসমূহ (এখানেই রেজিস্টার এবং অন্যান্য রাউট থাকবে)
    path('api/', include('api.urls')),
    
    # JWT Auth Endpoints
    # এখানে ডিফল্ট ভিউয়ের পরিবর্তে আপনার কাস্টম EmailTokenObtainPairView ব্যবহার করা হয়েছে
    path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# মিডিয়া ফাইল পরিবেশনের জন্য (শুধুমাত্র DEBUG মোডে)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)