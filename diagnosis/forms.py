from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import DiagnosisRequest, FeedbackRating, Crop
from PIL import Image

class ImageUploadForm(forms.ModelForm):
    """Enhanced form with better file handling"""
    class Meta:
        model = DiagnosisRequest
        fields = ['image', 'crop', 'farmer_notes', 'location']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the user from the request
        if self.request and hasattr(self.request, 'user'):
            instance.user = self.request.user
        
        if commit:
            instance.save()
        return instance
    
class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback on diagnosis results"""
    
    class Meta:
        model = FeedbackRating
        fields = ['rating', 'comments', 'is_diagnosis_accurate', 'actual_disease']
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please share your experience and any suggestions...'
            }),
            'is_diagnosis_accurate': forms.RadioSelect(
                choices=[(True, 'Yes'), (False, 'No')],
                attrs={'class': 'form-check-input'}
            ),
            'actual_disease': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        help_texts = {
            'rating': _('Rate the overall quality of the diagnosis'),
            'is_diagnosis_accurate': _('Was the diagnosis correct?'),
            'actual_disease': _('If diagnosis was wrong, what was the actual disease?')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['actual_disease'].queryset = self.fields['actual_disease'].queryset.none()
        self.fields['actual_disease'].required = False

class CropFilterForm(forms.Form):
    """Form for filtering diagnosis history by crop type"""
    
    crop = forms.ModelChoiceField(
        queryset=Crop.objects.all(),
        required=False,
        empty_label="All Crops",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(DiagnosisRequest.Status.choices),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

class QuickUploadForm(forms.Form):
    """Simplified form for quick image upload"""
    
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*',
            'id': 'quick-upload'
        })
    )
    
    def clean_image(self):
        """Validate uploaded image"""
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError(_('Please upload an image'))
        
        # Check file size (max 5MB)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError(_('Image file too large. Maximum size is 5MB.'))
        
        return image
class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback on diagnosis results"""
    
    class Meta:
        model = FeedbackRating
        fields = ['rating', 'comments', 'is_diagnosis_accurate', 'actual_disease']
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please share your experience and any suggestions...'
            }),
            'is_diagnosis_accurate': forms.RadioSelect(
                choices=[(True, 'Yes'), (False, 'No')],
                attrs={'class': 'form-check-input'}
            ),
            'actual_disease': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        help_texts = {
            'rating': _('Rate the overall quality of the diagnosis'),
            'is_diagnosis_accurate': _('Was the diagnosis correct?'),
            'actual_disease': _('If diagnosis was wrong, what was the actual disease?')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['actual_disease'].queryset = self.fields['actual_disease'].queryset.none()
        self.fields['actual_disease'].required = False

class CropFilterForm(forms.Form):
    """Form for filtering diagnosis history by crop type"""
    
    crop = forms.ModelChoiceField(
        queryset=Crop.objects.all(),
        required=False,
        empty_label="All Crops",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(DiagnosisRequest.Status.choices),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

class QuickUploadForm(forms.Form):
    """Simplified form for quick image upload"""
    
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*',
            'id': 'quick-upload'
        })
    )
    
    def clean_image(self):
        """Validate uploaded image"""
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError(_('Please upload an image'))
        
        # Check file size (max 5MB)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError(_('Image file too large. Maximum size is 5MB.'))
        
        return image