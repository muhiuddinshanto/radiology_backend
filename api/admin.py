from django.contrib import admin
from .models import Task, UploadedImage, AnnotationPolygon

# মডেলগুলোকে অ্যাডমিন প্যানেলে রেজিস্টার করা হচ্ছে
admin.site.register(Task)
admin.site.register(UploadedImage)
admin.site.register(AnnotationPolygon)