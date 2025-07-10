
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=50, blank=True)
    growing_season = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Disease(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    name = models.CharField(max_length=150)
    scientific_name = models.CharField(max_length=200, blank=True)
    crops = models.ManyToManyField(Crop, related_name='diseases')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    symptoms = models.TextField()
    causes = models.TextField(blank=True)
    prevention_methods = models.TextField(blank=True)
    treatment_methods = models.TextField(blank=True)
    image = models.ImageField(upload_to='disease_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class DiagnosisRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diagnosis_images/')
    location = models.CharField(max_length=200, blank=True)
    gps_coordinates = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, help_text="Additional symptoms or observations")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True, help_text="Time in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis for {self.crop.name} by {self.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']


class DiagnosisResult(models.Model):
    diagnosis_request = models.OneToOneField(DiagnosisRequest, on_delete=models.CASCADE, related_name='result')
    detected_diseases = models.ManyToManyField(Disease, through='DiseaseDetection')
    overall_health_status = models.CharField(max_length=50, default='Unknown')
    recommendations = models.TextField(blank=True)
    urgency_level = models.CharField(
        max_length=10,
        choices=Disease.SEVERITY_CHOICES,
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.diagnosis_request}"


class DiseaseDetection(models.Model):
    diagnosis_result = models.ForeignKey(DiagnosisResult, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence_score = models.FloatField()
    affected_area_percentage = models.FloatField(null=True, blank=True)
    severity_assessment = models.CharField(
        max_length=10,
        choices=Disease.SEVERITY_CHOICES,
        default='medium'
    )

    def __str__(self):
        return f"{self.disease.name} - {self.confidence_score}% confidence"

    class Meta:
        ordering = ['-confidence_score']


class FeedbackRating(models.Model):
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    diagnosis_result = models.OneToOneField(DiagnosisResult, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accuracy_rating = models.IntegerField(choices=RATING_CHOICES)
    usefulness_rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.get_full_name()} - {self.accuracy_rating}/5"
