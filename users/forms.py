from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.db import connection, transaction

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    
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
            # Use transaction.atomic() for proper transaction handling
            with transaction.atomic():
                user.save()
                
                # Use raw PostgreSQL query with proper transaction context
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users_profile (user_id, phone, address, farmer, agronomist, extension_worker)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) 
                        DO UPDATE SET
                            phone = EXCLUDED.phone,
                            address = EXCLUDED.address,
                            farmer = EXCLUDED.farmer,
                            agronomist = EXCLUDED.agronomist,
                            extension_worker = EXCLUDED.extension_worker
                    """, [
                        user.id,
                        self.cleaned_data['phone'],
                        self.cleaned_data['address'],
                        self.cleaned_data['user_role'] == 'farmer',
                        self.cleaned_data['user_role'] == 'agronomist',
                        self.cleaned_data['user_role'] == 'extension_worker'
                    ])
                
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
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
        if self.instance and self.instance.pk:
            # Use Django ORM for simplicity in form initialization
            if self.instance.farmer:
                self.fields['user_role'].initial = 'farmer'
            elif self.instance.agronomist:
                self.fields['user_role'].initial = 'agronomist'
            elif self.instance.extension_worker:
                self.fields['user_role'].initial = 'extension_worker'
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            with transaction.atomic():
                # Use raw PostgreSQL for the update
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE users_profile 
                        SET 
                            phone = %s,
                            address = %s,
                            farmer = %s,
                            agronomist = %s,
                            extension_worker = %s
                        WHERE user_id = %s
                    """, [
                        self.cleaned_data['phone'],
                        self.cleaned_data['address'],
                        self.cleaned_data['user_role'] == 'farmer',
                        self.cleaned_data['user_role'] == 'agronomist',
                        self.cleaned_data['user_role'] == 'extension_worker',
                        profile.user_id
                    ])
                
        return profile