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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user and request.user.is_authenticated:
            self.fields['image'].queryset = UploadedImage.objects.filter(
                owner=request.user
            )
        else:
            self.fields['image'].queryset = UploadedImage.objects.none()

    def validate_points(self, value):
        """Accept only polygons with three or more normalized 2D points."""
        if not isinstance(value, list) or len(value) < 3:
            raise serializers.ValidationError("A polygon needs at least three points.")
        for point in value:
            if not isinstance(point, dict):
                raise serializers.ValidationError("Each point must contain x and y coordinates.")
            x, y = point.get('x'), point.get('y')
            if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise serializers.ValidationError("Point coordinates must be numbers.")
            if not 0 <= x <= 1 or not 0 <= y <= 1:
                raise serializers.ValidationError("Point coordinates must be between 0 and 1.")
        return value
class UploadedImageSerializer(serializers.ModelSerializer):
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

    def validate_username(self, value):
        # user à¦¯à¦¦à¦¿ username field à¦ email à¦¦à§‡à¦¯à¦¼, @ à¦à¦° à¦†à¦—à§‡à¦° à¦…à¦‚à¦¶ à¦¨à¦¾à¦“
        if '@' in value:
            value = value.split('@')[0]
        # unique check
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

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
    """Login à¦«à¦¿à¦²à§à¦¡à§‡ email à¦¦à¦¿à¦²à§‡ à¦¤à¦¾ username-à¦ à¦®à§à¦¯à¦¾à¦ª à¦•à¦°à§‡ à¦¦à§‡à¦¯à¦¼à¥¤"""
    def validate(self, attrs):
        email_or_username = attrs.get(self.username_field)
        try:
            user = User.objects.get(email=email_or_username)
            attrs[self.username_field] = user.username
        except User.DoesNotExist:
            pass
        return super().validate(attrs)