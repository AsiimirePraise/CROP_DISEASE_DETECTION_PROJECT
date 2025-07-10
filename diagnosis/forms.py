
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import DiagnosisRequest, FeedbackRating, Crop


class DiagnosisRequestForm(forms.ModelForm):
    class Meta:
        model = DiagnosisRequest
        fields = ['crop', 'image', 'location', 'gps_coordinates', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('crop'),
            Field('image'),
            Row(
                Column('location', css_class='form-group col-md-8'),
                Column('gps_coordinates', css_class='form-group col-md-4'),
            ),
            Field('description'),
            Submit('submit', 'Submit for Diagnosis', css_class='btn btn-success btn-lg')
        )


class FeedbackRatingForm(forms.ModelForm):
    class Meta:
        model = FeedbackRating
        fields = ['accuracy_rating', 'usefulness_rating', 'comments', 'would_recommend']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('accuracy_rating', css_class='form-group col-md-6'),
                Column('usefulness_rating', css_class='form-group col-md-6'),
            ),
            Field('would_recommend'),
            Field('comments'),
            Submit('submit', 'Submit Feedback', css_class='btn btn-primary')
        )
