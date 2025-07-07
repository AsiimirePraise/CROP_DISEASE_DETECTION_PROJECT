
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from .models import User, UserProfile, PasswordReset, LoginAttempt
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,
    PasswordResetRequestForm, PasswordResetConfirmForm
)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@ratelimit(key='ip', rate='5/m', method='POST')
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Send verification email (placeholder)
            # send_verification_email(user)
            
            messages.success(request, 'Account created successfully! Please check your email for verification.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@ratelimit(key='ip', rate='10/m', method='POST')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        ip_address = get_client_ip(request)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                LoginAttempt.objects.create(
                    email=user.email,
                    ip_address=ip_address,
                    success=True
                )
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect(request.GET.get('next', 'accounts:dashboard'))
        
        # Log failed attempt
        email = request.POST.get('username', '')
        LoginAttempt.objects.create(
            email=email,
            ip_address=ip_address,
            success=False
        )
        messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    context = {
        'user_profile': user_profile,
        'recent_diagnoses': [],  # Will be populated from diagnosis app
        'dashboard_stats': {
            'total_diagnoses': 0,
            'successful_treatments': 0,
            'active_alerts': 0,
        }
    }
    
    # Different dashboard based on user type
    template_name = f'accounts/dashboard_{user_profile.user_type}.html'
    try:
        return render(request, template_name, context)
    except:
        return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_update_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'accounts/profile_update.html', {'form': form})


@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})


@ratelimit(key='ip', rate='3/h', method='POST')
def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = secrets.token_urlsafe(32)
            PasswordReset.objects.create(user=user, token=token)
            
            # Send email (placeholder)
            reset_url = request.build_absolute_uri(f'/accounts/password-reset-confirm/{token}/')
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset link sent to your email!')
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm_view(request, token):
    reset_obj = get_object_or_404(PasswordReset, token=token)
    
    if reset_obj.used or reset_obj.is_expired():
        messages.error(request, 'This password reset link is invalid or has expired.')
        return redirect('accounts:password_reset_request')
    
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = reset_obj.user
            user.set_password(password)
            user.save()
            
            reset_obj.used = True
            reset_obj.save()
            
            messages.success(request, 'Password reset successfully! You can now login.')
            return redirect('accounts:login')
    else:
        form = PasswordResetConfirmForm()
    
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})
