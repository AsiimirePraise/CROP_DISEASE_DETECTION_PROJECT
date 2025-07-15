from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    Phone = forms.CharField(required=True, max_length=20)
    Address = forms.CharField(required=True, max_length=255)
    
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('extension_worker', 'Extension Worker'),
        ('agronomist', 'Agronomist'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EditUserForm(forms.Form):  # Change from ModelForm to Form
    # User model fields
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    # Profile fields (custom fields)
    Phone = forms.CharField(max_length=15, required=False, label="Phone")
    Address = forms.CharField(max_length=200, required=False, label="Address")
    role = forms.ChoiceField(
        choices=[
            ('farmer', 'Farmer'),
            ('extension_worker', 'Extension Worker'),
            ('agronomist', 'Agronomist'),
        ],
        required=True,
        label="Role"
    )
    
    def __init__(self, *args, **kwargs):
        # Extract the user instance if provided
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Pre-populate fields if user exists
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email
            
            # Pre-populate profile fields if user exists
            try:
                profile = self.instance.profile
                self.fields['Phone'].initial = profile.phone
                self.fields['Address'].initial = profile.address
                self.fields['role'].initial = profile.user_role
            except:
                pass