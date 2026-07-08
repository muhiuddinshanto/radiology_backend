from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task, UploadedImage, AnnotationPolygon

# --- Task & Annotation Serializers ---

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

class AnnotationPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationPolygon
        fields = ['id', 'image', 'points', 'label', 'color', 'created_at']

class UploadedImageSerializer(serializers.ModelSerializer):
    # নেস্টেড সিরিয়ালাইজার রিড-অনলি
    polygons = AnnotationPolygonSerializer(many=True, read_only=True)

    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'uploaded_at', 'polygons', 'owner']
        read_only_fields = ['owner']

# --- Auth Serializers ---

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login ফিল্ডে email দিলে তা username-এ ম্যাপ করে দেয়।"""
    def validate(self, attrs):
        email_or_username = attrs.get(self.username_field)
        try:
            # যদি ইনপুটটি ইমেইল হয়, তবে ডাটাবেস থেকে ইউজারনেম খুঁজে বের করবে
            user = User.objects.get(email=email_or_username)
            attrs[self.username_field] = user.username
        except User.DoesNotExist:
            # যদি ইমেইল দিয়ে না পাওয়া যায়, তবে সাধারণ ইউজারনেম হিসেবেই প্রসেস করবে
            pass
        return super().validate(attrs)