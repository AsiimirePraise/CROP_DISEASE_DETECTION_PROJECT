from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    
    # Replace the three BooleanFields with a single ChoiceField
    USER_ROLE_CHOICES = [
        ('farmer', 'I am a farmer'),
        ('agronomist', 'I am an agronomist'),
        ('extension_worker', 'I am an extension worker'),
    ]
    
    user_role = forms.ChoiceField(
        choices=USER_ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Select your role"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update the profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.address = self.cleaned_data['address']
            
            # Set the selected role to True, others to False
            profile.farmer = self.cleaned_data['user_role'] == 'farmer'
            profile.agronomist = self.cleaned_data['user_role'] == 'agronomist'
            profile.extension_worker = self.cleaned_data['user_role'] == 'extension_worker'
            
            profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # Also update this form to use radio buttons for consistency
    USER_ROLE_CHOICES = [
        ('farmer', 'I am a farmer'),
        ('agronomist', 'I am an agronomist'),
        ('extension_worker', 'I am an extension worker'),
    ]
    
    user_role = forms.ChoiceField(
        choices=USER_ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Select your role"
    )
    
    class Meta:
        model = Profile
        fields = ['phone', 'address']  
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value based on the current profile
        if self.instance and self.instance.pk:
            if self.instance.farmer:
                self.fields['user_role'].initial = 'farmer'
            elif self.instance.agronomist:
                self.fields['user_role'].initial = 'agronomist'
            elif self.instance.extension_worker:
                self.fields['user_role'].initial = 'extension_worker'
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Set the selected role to True, others to False
        profile.farmer = self.cleaned_data['user_role'] == 'farmer'
        profile.agronomist = self.cleaned_data['user_role'] == 'agronomist'
        profile.extension_worker = self.cleaned_data['user_role'] == 'extension_worker'
        
        if commit:
            profile.save()
        return profile