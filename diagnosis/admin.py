from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Crop, Disease, DiagnosisRequest, FeedbackRating, TreatmentRecommendation

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'created_at']
    search_fields = ['name', 'scientific_name']
    list_filter = ['created_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name')
        }),
        ('Details', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'severity_level', 'get_affected_crops_count', 'created_at']
    list_filter = ['severity_level', 'created_at', 'affected_crops']
    search_fields = ['name', 'scientific_name', 'description']
    filter_horizontal = ['affected_crops']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'severity_level')
        }),
        ('Description', {
            'fields': ('description', 'symptoms')
        }),
        ('Treatment', {
            'fields': ('prevention', 'treatment'),
            'classes': ('collapse',)
        }),
        ('Crops', {
            'fields': ('affected_crops',)
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def get_affected_crops_count(self, obj):
        return obj.affected_crops.count()
    get_affected_crops_count.short_description = 'Affected Crops'

@admin.register(DiagnosisRequest)
class DiagnosisRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'crop', 'status', 'is_healthy', 
        'confidence_percentage_display', 'predicted_disease', 'created_at'
    ]
    list_filter = [
        'status', 'is_healthy', 'severity', 'crop', 
        'predicted_disease', 'created_at'
    ]
    search_fields = [
        'user__username', 'user__email', 'crop__name', 
        'predicted_disease__name', 'notes', 'farmer_notes'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'processed_at',
        'confidence_percentage_display', 'image_preview'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'crop', 'status', 'image', 'image_preview')
        }),
        ('Diagnosis Results', {
            'fields': (
                'predicted_disease', 'confidence_score', 'confidence_percentage_display',
                'is_healthy', 'severity'
            )
        }),
        ('Additional Information', {
            'fields': ('farmer_notes', 'location', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def confidence_percentage_display(self, obj):
        if obj.confidence_score:
            percentage = obj.confidence_percentage
            color = 'green' if percentage >= 80 else 'orange' if percentage >= 60 else 'red'
            return format_html(
                '<span style="color: {};">{:.1f}%</span>',
                color, percentage
            )
        return '-'
    confidence_percentage_display.short_description = 'Confidence'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image Preview'
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status=DiagnosisRequest.Status.COMPLETED)
        self.message_user(
            request, 
            f'{updated} diagnosis requests marked as completed.'
        )
    mark_as_completed.short_description = 'Mark selected requests as completed'
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status=DiagnosisRequest.Status.FAILED)
        self.message_user(
            request, 
            f'{updated} diagnosis requests marked as failed.'
        )
    mark_as_failed.short_description = 'Mark selected requests as failed'

@admin.register(FeedbackRating)
class FeedbackRatingAdmin(admin.ModelAdmin):
    list_display = [
        'diagnosis_request', 'get_user', 'rating', 'rating_display',
        'is_diagnosis_accurate', 'created_at'
    ]
    list_filter = [
        'rating', 'is_diagnosis_accurate', 'created_at',
        'diagnosis_request__predicted_disease'
    ]
    search_fields = [
        'diagnosis_request__user__username', 
        'diagnosis_request__user__email',
        'comments'
    ]
    readonly_fields = ['created_at', 'get_user', 'get_diagnosis_details']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('diagnosis_request', 'get_user', 'get_diagnosis_details')
        }),
        ('Rating', {
            'fields': ('rating', 'rating_display', 'is_diagnosis_accurate', 'actual_disease')
        }),
        ('Comments', {
            'fields': ('comments',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_user(self, obj):
        return obj.diagnosis_request.user
    get_user.short_description = 'User'
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color, stars
        )
    rating_display.short_description = 'Rating Stars'
    
    def get_diagnosis_details(self, obj):
        diagnosis = obj.diagnosis_request
        return format_html(
            '<strong>Status:</strong> {}<br>'
            '<strong>Disease:</strong> {}<br>'
            '<strong>Confidence:</strong> {:.1f}%<br>'
            '<strong>Healthy:</strong> {}',
            diagnosis.get_status_display(),
            diagnosis.predicted_disease.name if diagnosis.predicted_disease else 'None',
            diagnosis.confidence_percentage,
            'Yes' if diagnosis.is_healthy else 'No'
        )
    get_diagnosis_details.short_description = 'Diagnosis Details'

@admin.register(TreatmentRecommendation)
class TreatmentRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        'diagnosis_request', 'disease', 'urgency_level', 
        'estimated_cost', 'get_user', 'created_at'
    ]
    list_filter = [
        'urgency_level', 'disease', 'created_at',
        'diagnosis_request__status'
    ]
    search_fields = [
        'diagnosis_request__user__username',
        'disease__name', 'treatment_steps', 'products_needed'
    ]
    readonly_fields = ['created_at', 'get_user', 'get_diagnosis_link']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('diagnosis_request', 'get_user', 'disease', 'urgency_level')
        }),
        ('Treatment Details', {
            'fields': ('treatment_steps', 'products_needed', 'estimated_cost', 'timeframe')
        }),
        ('Links', {
            'fields': ('get_diagnosis_link',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_user(self, obj):
        return obj.diagnosis_request.user
    get_user.short_description = 'User'
    
    def get_diagnosis_link(self, obj):
        url = reverse('admin:diagnosis_diagnosisrequest_change', args=[obj.diagnosis_request.id])
        return format_html('<a href="{}">View Diagnosis Request</a>', url)
    get_diagnosis_link.short_description = 'Diagnosis Request'

# Custom admin site configuration
admin.site.site_header = 'Crop Disease Detection Admin'
admin.site.site_title = 'Crop Disease Detection'
admin.site.index_title = 'Administration Dashboard'