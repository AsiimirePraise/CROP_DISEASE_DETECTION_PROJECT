from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Crop(models.Model):
    """Model for different types of crops"""
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    """Model for plant diseases"""
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    symptoms = models.TextField()
    prevention = models.TextField()
    treatment = models.TextField()
    affected_crops = models.ManyToManyField(Crop, related_name='diseases')
    severity_level = models.CharField(
        max_length=20, 
        choices=[
            ('LOW', _('Low')),
            ('MEDIUM', _('Medium')),
            ('HIGH', _('High'))
        ]
    )
    image = models.ImageField(upload_to='disease_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class DiagnosisRequest(models.Model):
    """Model for diagnosis requests from farmers"""
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    class Severity(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnosis_requests')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='diagnosis_images/')
    
    # Model prediction results
    predicted_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    is_healthy = models.BooleanField(default=False)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    severity = models.CharField(max_length=20, choices=Severity.choices, blank=True, null=True)
    notes = models.TextField(blank=True)
    
    # Additional details from farmer
    farmer_notes = models.TextField(blank=True, help_text="Additional notes from the farmer")
    location = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Diagnosis Request')
        verbose_name_plural = _('Diagnosis Requests')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Diagnosis #{self.id} - {self.user.username} - {self.status}"

    @property
    def confidence_percentage(self):
        """Return confidence as percentage"""
        if self.confidence_score:
            return round(self.confidence_score * 100, 2)
        return 0

class FeedbackRating(models.Model):
    """Model for farmer feedback on diagnosis results"""
    class Rating(models.IntegerChoices):
        VERY_BAD = 1, _('Very Bad')
        BAD = 2, _('Bad')
        AVERAGE = 3, _('Average')
        GOOD = 4, _('Good')
        EXCELLENT = 5, _('Excellent')

    diagnosis_request = models.OneToOneField(
        DiagnosisRequest, 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )
    rating = models.IntegerField(choices=Rating.choices)
    comments = models.TextField(blank=True)
    is_diagnosis_accurate = models.BooleanField(null=True, blank=True)
    actual_disease = models.ForeignKey(
        Disease, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="What was the actual disease if diagnosis was wrong?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Feedback Rating')
        verbose_name_plural = _('Feedback Ratings')
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for Diagnosis #{self.diagnosis_request.id} - {self.get_rating_display()}"

class TreatmentRecommendation(models.Model):
    """Model for treatment recommendations based on diagnosis"""
    diagnosis_request = models.ForeignKey(
        DiagnosisRequest, 
        on_delete=models.CASCADE, 
        related_name='recommendations'
    )
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    treatment_steps = models.TextField()
    products_needed = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timeframe = models.CharField(max_length=100, blank=True)
    urgency_level = models.CharField(
        max_length=20,
        choices=[
            ('LOW', _('Low')),
            ('MEDIUM', _('Medium')),
            ('HIGH', _('High')),
            ('URGENT', _('Urgent'))
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Treatment Recommendation')
        verbose_name_plural = _('Treatment Recommendations')
        ordering = ['-created_at']

    def __str__(self):
        return f"Treatment for {self.disease.name} - Diagnosis #{self.diagnosis_request.id}"