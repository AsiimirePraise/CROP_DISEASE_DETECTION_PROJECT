from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from diagnosis.models import DiagnosisRequest, FarmerDiagnosis
from recommendations.models import Recommendation, Training
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
import json
import os
from django.conf import settings
from recommendations.forms import TrainingForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html', {'user_role': 'admin'})

    try:
        if hasattr(request.user, 'profile'):
            user_role = request.user.profile.get_user_role()
        
        if user_role == 'farmer':
            return redirect('diagnosis:index')
        
        elif user_role == 'agronomist':
            today = timezone.now().date()

            total_diagnoses = DiagnosisRequest.objects.count()

            active_users_today = User.objects.filter(
                last_login__gte=today
            ).distinct().count()

            recommendations = Recommendation.objects.all().count()

            context = {
                'diagnoses': total_diagnoses,
                'active_users': active_users_today,
                'recommendations': recommendations,
                'user_role': 'agronomist'
            }
            return render(request, 'dashboard/agronomist_dashboard.html', context)

        elif user_role == 'extension_worker':
            farmers = User.objects.filter(profile__farmer=True)
            farmer_count = farmers.count()
            active_cases = DiagnosisRequest.objects.all().count()
            trainings = Training.objects.filter(date__gte=timezone.now().date()).order_by('date')

            # === Load JSON recommendation data ===
            json_path = os.path.join(settings.BASE_DIR, 'recommendations.json')
            if os.path.exists(json_path):
             with open(json_path, 'r') as file:
              recommendations_data = json.load(file)
              recommendations = len(recommendations_data)
            else:
              recommendations_data = []
              recommendations = 0  # Default if file doesn't exist


            if request.method == 'POST':
                farmer_id = request.POST.get('farmer')
                if farmer_id:
                    try:
                        farmer = User.objects.get(id=farmer_id)
                    except User.DoesNotExist:
                        messages.error(request, "Farmer not found.")

            return render(request, 'dashboard/extension_worker_dashboard.html', {
                'farmers': farmers,
                'farmer_count': farmer_count,
                'active_cases': active_cases,
                'trainings': trainings,
                'recommendations': recommendations,
                'recommendations_data': recommendations_data,
                'user_role': 'extension_worker'
            })

        else:
            messages.error(request, "Please select your role in your profile.")
            return redirect('profile')

    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup.")
        return redirect('profile')

@csrf_exempt
@login_required
def store_diagnosis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            diagnosis = FarmerDiagnosis.objects.create(
                farmer=request.user,
                image_url=data.get('imageSrc'),
                disease_details=data.get('diseaseDetails')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

def disease_chart_data(request):
    data = (
        DiagnosisRequest.objects
        .values('predicted_disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    labels = [item['predicted_disease__name'] or "Unknown" for item in data]
    counts = [item['count'] for item in data]

    return JsonResponse({
        'labels': labels,
        'data': counts,
    })

def get_diagnosis_analytics(request):
    time_threshold = timezone.now() - timedelta(days=30)

    diseases = FarmerDiagnosis.objects.filter(
        timestamp__gte=time_threshold
    ).values('disease_details__predicted_class_name').annotate(
        count=Count('id')
    ).order_by('-count')

    recent = FarmerDiagnosis.objects.filter(
        timestamp__gte=time_threshold
    ).order_by('-timestamp')[:10]

    return JsonResponse({
        'disease_distribution': list(diseases),
        'recent_activity': [
            {
                'image_url': d.image_url,
                'disease': d.disease_details.get('predicted_class_name'),
                'timestamp': d.timestamp
            } for d in recent
        ],
        'total_diagnoses': FarmerDiagnosis.objects.count()
    })

@login_required
def schedule_training(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        date = request.POST.get('date')
        location = request.POST.get('location')

        if topic and date and location:
            Training.objects.create(
                topic=topic,
                date=date,
                location=location,
                created_by=request.user  # optional field
            )
            messages.success(request, "Training scheduled!")
        else:
            messages.error(request, "Please fill all fields.")
    return redirect('dashboard')  # or the route name for your dashboard


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
