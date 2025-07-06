
from django.db import models
from django.contrib.auth import get_user_model
from diagnosis.models import Disease, DiagnosisResult

User = get_user_model()


class TreatmentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Treatment Categories"


class Treatment(models.Model):
    TREATMENT_TYPES = [
        ('chemical', 'Chemical'),
        ('biological', 'Biological'),
        ('cultural', 'Cultural'),
        ('integrated', 'Integrated'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE)
    treatment_type = models.CharField(max_length=15, choices=TREATMENT_TYPES)
    diseases = models.ManyToManyField(Disease, related_name='treatments')
    active_ingredients = models.TextField(blank=True)
    application_method = models.TextField()
    dosage_instructions = models.TextField()
    safety_precautions = models.TextField(blank=True)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    effectiveness_rating = models.FloatField(default=0.0, help_text="Rating out of 5")
    organic_friendly = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_treatment_type_display()})"

    class Meta:
        ordering = ['-effectiveness_rating', 'name']


class Recommendation(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    diagnosis_result = models.ForeignKey(DiagnosisResult, on_delete=models.CASCADE)
    treatments = models.ManyToManyField(Treatment, through='TreatmentRecommendation')
    custom_recommendations = models.TextField(blank=True)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timeline = models.CharField(max_length=200, blank=True, help_text="Expected treatment timeline")
    follow_up_required = models.BooleanField(default=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.diagnosis_result.diagnosis_request}"


class TreatmentRecommendation(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1, help_text="Order of application")
    specific_instructions = models.TextField(blank=True)
    quantity_needed = models.CharField(max_length=100, blank=True)
    application_frequency = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.treatment.name} for {self.recommendation}"


class TreatmentTracking(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    effectiveness_rating = models.IntegerField(
        null=True, blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rate effectiveness 1-5"
    )
    side_effects_observed = models.TextField(blank=True)
    cost_incurred = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.treatment.name}"

    class Meta:
        unique_together = ['user', 'recommendation', 'treatment']


class PreventiveMeasure(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    diseases = models.ManyToManyField(Disease, related_name='preventive_measures')
    implementation_cost = models.CharField(max_length=50, choices=[
        ('low', 'Low Cost'),
        ('medium', 'Medium Cost'),
        ('high', 'High Cost'),
    ], default='medium')
    difficulty_level = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    seasonal_timing = models.CharField(max_length=200, blank=True)
    effectiveness = models.FloatField(default=0.0, help_text="Effectiveness rating out of 5")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-effectiveness', 'name']
