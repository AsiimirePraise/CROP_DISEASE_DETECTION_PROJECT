
from turtle import pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from adminpanel.models import FarmerUpload, TrainingImage
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
from diagnosis.models import DiagnosisRequest, DiseasePrediction, FarmerDiagnosis
from .forms import EditUserForm 
from django.db import transaction
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from diagnosis.models import DiagnosisRequest
import json
import csv
from io import StringIO
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import pandas as pd 

# Optional: Decorator to allow only superusers
def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

@admin_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'adminpanel/manage_users.html', {'users': users})

@admin_required
def manage_issues(request):
    
    return render(request, 'adminpanel/manage_issues.html')

@admin_required
def manage_datasets(request):
    
    return render(request, 'adminpanel/manage_datasets.html')

@admin_required
def retrain_model(request):
    if request.method == 'POST':
        # Add your actual retraining logic here
        message = "Model retraining started successfully."
        return render(request, 'adminpanel/retrain_model.html', {'message': message})
    return render(request, 'adminpanel/retrain_model.html')

def manage_users(request):
    users = User.objects.filter(is_superuser=False).select_related('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Save profile fields
            profile = user.profile
            profile.phone = form.cleaned_data['Phone']
            profile.address = form.cleaned_data['Address']

            # Reset all roles first
            profile.farmer = False
            profile.agronomist = False
            profile.extension_worker = False

            # Set selected role
            selected_role = form.cleaned_data['role']
            if selected_role == 'farmer':
                profile.farmer = True
            elif selected_role == 'agronomist':
                profile.agronomist = True
            elif selected_role == 'extension_worker':
                profile.extension_worker = True

            profile.save()

            messages.success(request, 'User created successfully.')
            return redirect('manage-users')
    else:
        form = CustomUserCreationForm()

    return render(request, 'adminpanel/manage_users.html', {'users': users, 'form': form})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Update User fields
                    user.username = form.cleaned_data['username']
                    user.email = form.cleaned_data['email']
                    user.save()

                    # Get or create profile
                    profile, created = Profile.objects.get_or_create(user=user)

                    # Update profile fields
                    profile.phone = form.cleaned_data.get('Phone', '')
                    profile.address = form.cleaned_data.get('Address', '')

                    # Reset all roles to False
                    profile.farmer = False
                    profile.agronomist = False
                    profile.extension_worker = False

                    # Set selected role to True
                    selected_role = form.cleaned_data.get('role')
                    if selected_role == 'farmer':
                        profile.farmer = True
                    elif selected_role == 'agronomist':
                        profile.agronomist = True
                    elif selected_role == 'extension_worker':
                        profile.extension_worker = True

                    profile.save()

                    messages.success(request, f'User "{user.username}" updated successfully.')
                    return redirect('manage-users')
                         
            except Exception as e:
                messages.error(request, f'Error updating user: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        try:
            profile = user.profile
            # Determine current role
            if profile.farmer:
                role = 'farmer'
            elif profile.agronomist:
                role = 'agronomist'
            elif profile.extension_worker:
                role = 'extension_worker'
            else:
                role = ''
        except Profile.DoesNotExist:
            profile = None
            role = ''

        form = EditUserForm(initial={
            'username': user.username,
            'email': user.email,
            'Phone': profile.phone if profile else '',
            'Address': profile.address if profile else '',
            'role': role,
        }, instance=user)

    context = {
        'form': form,
        'user': user,
        'title': f'Edit User: {user.username}'
    }
    return render(request, 'adminpanel/edit_user.html', context)
@login_required
def admin_dashboard(request):
    # Check if user is admin
    if not request.user.is_staff:
        return redirect('login')
    
    # Get current date and time ranges
    now = timezone.now()
    today = now.date()
    this_week_start = now - timedelta(days=7)
    this_month_start = now.replace(day=1)

    farmers = User.objects.filter(profile__farmer=True)
    agronomists = User.objects.filter(profile__agronomist=True)
    extension_workers = User.objects.filter(profile__extension_worker=True)
    
    user_stats = {
        'total_farmers': farmers.count(),
        'total_agronomists': agronomists.count(),
        'total_extension_workers': extension_workers.count(),
        'total_users': User.objects.filter(is_staff=False, is_superuser=False).count(),

        
        # Active users this month (users who have logged in or made diagnoses)
        
        
        # Online agronomists (logged in within last 30 minutes)
        'online_agronomists': agronomists.filter(
            last_login__gte=now - timedelta(minutes=30)
        ).count(),
        
       
        
        
        # New users this week
        'new_users_week': User.objects.filter(
            date_joined__gte=this_week_start
        ).count(),

          
    }

    # Get total diagnoses
    diagnosis_stats = {
        'total_diagnoses': DiagnosisRequest.objects.count()
    }
    avg_accuracy = DiagnosisRequest.objects.filter(
    status='COMPLETED',
    confidence_score__isnull=False
    ).aggregate(Avg('confidence_score'))['confidence_score__avg']

    diagnosis_stats['model_accuracy'] = round(avg_accuracy * 100, 1) if avg_accuracy else 0
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'user_stats': user_stats,
        'title': 'Admin Dashboard',
        'diagnosis_stats': diagnosis_stats,

    })
@user_passes_test(lambda u: u.is_superuser)
def manage_datasets(request):
    farmer_uploads = FarmerUpload.objects.all().order_by('-upload_date')
    training_images = TrainingImage.objects.all().order_by('-upload_date')
    
    context = {
        'farmer_uploads': farmer_uploads,
        'training_images': training_images,
    }
    return render(request, 'adminpanel/manage_datasets.html', context)

@user_passes_test(lambda u: u.is_superuser)
def verify_upload(request, upload_id):
    if request.method == 'POST':
        upload = FarmerUpload.objects.get(id=upload_id)
        upload.verified = True
        upload.correct_prediction = request.POST.get('correct_prediction') == 'true'
        upload.admin_notes = request.POST.get('admin_notes', '')
        upload.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt  # OR use csrf token properly via headers in JS (see note below)
@user_passes_test(lambda u: u.is_superuser)
def upload_training_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        label = request.POST.get('label')
        
        if image and label:
            TrainingImage.objects.create(
                image=image,
                label=label,
                uploaded_by=request.user,
                verified=True
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing image or label'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@user_passes_test(lambda u: u.is_superuser)
def export_to_csv(request):
    from datetime import datetime
    import pandas as pd
    from django.http import HttpResponse

    farmer_uploads = FarmerUpload.objects.filter(verified=True)

    data = []
    for upload in farmer_uploads:
        data.append({
            'image_path': upload.image.url if upload.image else '',
            'label': f"{upload.crop_type}__{upload.disease}",
            'crop_type': upload.crop_type,
            'disease': upload.disease,
            'severity': upload.severity,
            'primary_affected_part': upload.primary_affected_part,
            'affected_parts': ', '.join(upload.affected_parts) if isinstance(upload.affected_parts, list) else '',
            'description': upload.description,
            'symptoms': upload.symptoms,
            'upload_date': upload.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='text/csv')
    filename = f"farmer_uploads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    df.to_csv(response, index=False)
    return response

@user_passes_test(lambda u: u.is_superuser)
def export_training_images(request):
    # Get all verified training images
    training_images = TrainingImage.objects.filter(verified=True)
    
    # Prepare data for CSV
    data = []
    for img in training_images:
        data.append({
            'image_path': img.image.url,
            'label': img.label,
            'upload_date': img.upload_date,
            'uploaded_by': img.uploaded_by.username if img.uploaded_by else 'system',
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    filename = f"training_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    df.to_csv(response, index=False)
    return response