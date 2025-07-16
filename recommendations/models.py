from django.db import models
from diagnosis.models import DiagnosisRequest
from users.models import User

class Recommendation(models.Model):
    diagnosis = models.ForeignKey(DiagnosisRequest, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="No description available")
    steps = models.TextField(help_text="Step-by-step treatment plan", default="No treatment steps available")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class SavedRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default="")
    
    class Meta:
        unique_together = ('user', 'recommendation')
    
    def __str__(self):
        return f"{self.user.username} saved {self.recommendation.title}"