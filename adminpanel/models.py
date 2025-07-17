from django.db import models
from django.contrib.auth.models import User

class FarmerUpload(models.Model):
    SEVERITY_CHOICES = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='farmer_uploads/')
    predicted_class = models.CharField(max_length=255)
    confidence = models.FloatField()
    crop_type = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    primary_affected_part = models.CharField(max_length=100)
    affected_parts = models.JSONField(default=list)
    description = models.TextField()
    symptoms = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    correct_prediction = models.BooleanField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.crop_type} - {self.disease} ({self.upload_date})"

class TrainingImage(models.Model):
    image = models.ImageField(upload_to='training_images/')
    label = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.label