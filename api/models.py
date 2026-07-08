from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField()
    tags = models.JSONField(default=list, blank=True)
    assignee = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='annotations/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

class AnnotationPolygon(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='polygons')
    points = models.JSONField() 
    label = models.CharField(max_length=100, blank=True, null=True) # 💡 আপডেট করা হয়েছে
    color = models.CharField(max_length=20, default="#EF4444")      # 💡 আপডেট করা হয়েছে
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label or 'Polygon'} {self.id} on Image {self.image.id}"