from django.db import models
from django.utils import timezone


class Crop(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    affected_crops = models.ManyToManyField(Crop, related_name='diseases')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.crop.name}"


class Diagnosis(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence = models.IntegerField(help_text="Confidence percentage (0-100)")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    diagnosed_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.field.name} - {self.disease.name} ({self.diagnosed_at.date()})"

    class Meta:
        ordering = ['-diagnosed_at']


class SensorReading(models.Model):
    SENSOR_TYPES = [
        ('TEMPERATURE', 'Temperature'),
        ('HUMIDITY', 'Humidity'),
        ('SOIL_MOISTURE', 'Soil Moisture'),
        ('PH', 'pH Level'),
        ('LIGHT', 'Light Intensity'),
    ]
    
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    recorded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.field.name} - {self.sensor_type}: {self.value} {self.unit}"

    class Meta:
        ordering = ['-recorded_at']


class TreatmentRecommendation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('APPLIED', 'Applied'),
    ]
    
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    treatment = models.TextField()
    dosage = models.CharField(max_length=100, blank=True)
    application_method = models.CharField(max_length=200, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    recommended_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Treatment for {self.diagnosis} - {self.status}"

    class Meta:
        ordering = ['-created_at']
# Create your models here.
