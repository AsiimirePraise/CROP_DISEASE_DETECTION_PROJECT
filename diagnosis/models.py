from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from users.models import User 
from django.utils import timezone 


  




class Crop(models.Model):
    """Model for different types of crops"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    """Model for plant diseases"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(default="No description available")
    symptoms = models.TextField(default="No symptoms information available")
    prevention = models.TextField(default="No prevention information available")
    treatment = models.TextField(default="No treatment information available")
    affected_crops = models.ManyToManyField(Crop, related_name='diseases')
    severity_level = models.CharField(
        max_length=20, 
        choices=[
            ('LOW', _('Low')),
            ('MEDIUM', _('Medium')),
            ('HIGH', _('High'))
        ],
        default='MEDIUM'
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


    id = models.BigAutoField(primary_key=True)

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
    notes = models.TextField(blank=True, default="")
    
    # Additional details from farmer
    farmer_notes = models.TextField(blank=True, default="", help_text="Additional notes from the farmer")
    location = models.CharField(max_length=200, blank=True, default="")
    
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

    id = models.BigAutoField(primary_key=True)
    diagnosis_request = models.OneToOneField(
        DiagnosisRequest, 
        on_delete=models.CASCADE, 
        related_name='feedback',
        null=True,
        blank=True,
    )
    rating = models.IntegerField(choices=Rating.choices, default=Rating.AVERAGE)
    comments = models.TextField(blank=True, default="")
    is_diagnosis_accurate = models.BooleanField(null=True, blank=True)
    actual_disease = models.ForeignKey(
        Disease, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="What was the actual disease if diagnosis was wrong?"
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = _('Feedback Rating')
        verbose_name_plural = _('Feedback Ratings')
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for Diagnosis #{self.diagnosis_request.id} - {self.get_rating_display()}"

class TreatmentRecommendation(models.Model):
    """Model for treatment recommendations based on diagnosis"""
    id = models.BigAutoField(primary_key=True)
    diagnosis_request = models.ForeignKey(
        DiagnosisRequest, 
        on_delete=models.CASCADE, 
        related_name='recommendations',
        null=True, blank=True,
    )
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)
    diagnosis = models.TextField(default="No diagnosis available")
    description = models.TextField(default="No description available")
    treatment_steps = models.TextField(default="No treatment steps available")
    products_needed = models.TextField(blank=True, default="")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timeframe = models.CharField(max_length=100, blank=True, default="")
    urgency_level = models.CharField(
        max_length=20,
        choices=[
            ('LOW', _('Low')),
            ('MEDIUM', _('Medium')),
            ('HIGH', _('High')),
            ('URGENT', _('Urgent'))
        ],
        default='MEDIUM'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Treatment Recommendation')
        verbose_name_plural = _('Treatment Recommendations')
        ordering = ['-created_at']

    def __str__(self):
        return f"Treatment for {self.disease.name} - Diagnosis #{self.diagnosis_request.id}"
    
class DiseasePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='prediction_images/')
    predicted_class = models.CharField(max_length=100)
    confidence = models.FloatField()
    disease_info = models.JSONField()  # Stores the disease info dictionary
    recommendations = models.JSONField()  # Stores recommendations list
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20)
    
    # Optional: Link to diagnosis request if applicable
    diagnosis_request = models.ForeignKey(
        DiagnosisRequest, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence:.2f}%)"
    

class ReportedIssue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Issue #{self.id} - {self.title} ({self.status})"

    # models.py
class FarmerDiagnosis(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Farmer Upload #{self.id}"

    class Meta:
        ordering = ['-timestamp']


