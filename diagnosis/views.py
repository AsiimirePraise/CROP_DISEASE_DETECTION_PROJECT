
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import DiagnosisRequest, DiagnosisResult, Crop, Disease, FeedbackRating
from .forms import DiagnosisRequestForm, FeedbackRatingForm
from .tasks import process_diagnosis


@login_required
def diagnosis_list_view(request):
    diagnoses = DiagnosisRequest.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        diagnoses = diagnoses.filter(
            Q(crop__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(diagnoses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'diagnosis/list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
def diagnosis_create_view(request):
    if request.method == 'POST':
        form = DiagnosisRequestForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.user = request.user
            diagnosis.save()
            
            # Trigger async processing
            process_diagnosis.delay(str(diagnosis.id))
            
            messages.success(request, 'Diagnosis request submitted! Results will be available shortly.')
            return redirect('diagnosis:detail', diagnosis_id=diagnosis.id)
    else:
        form = DiagnosisRequestForm()
    
    return render(request, 'diagnosis/create.html', {'form': form})


@login_required
def diagnosis_detail_view(request, diagnosis_id):
    diagnosis = get_object_or_404(DiagnosisRequest, id=diagnosis_id, user=request.user)
    
    try:
        result = diagnosis.result
        disease_detections = result.diseasedetection_set.all()
    except DiagnosisResult.DoesNotExist:
        result = None
        disease_detections = []
    
    context = {
        'diagnosis': diagnosis,
        'result': result,
        'disease_detections': disease_detections,
    }
    
    return render(request, 'diagnosis/detail.html', context)


@login_required
def feedback_create_view(request, diagnosis_id):
    diagnosis = get_object_or_404(DiagnosisRequest, id=diagnosis_id, user=request.user)
    
    try:
        result = diagnosis.result
    except DiagnosisResult.DoesNotExist:
        messages.error(request, 'No result available for feedback.')
        return redirect('diagnosis:detail', diagnosis_id=diagnosis_id)
    
    if request.method == 'POST':
        form = FeedbackRatingForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.diagnosis_result = result
            feedback.user = request.user
            feedback.save()
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('diagnosis:detail', diagnosis_id=diagnosis_id)
    else:
        form = FeedbackRatingForm()
    
    return render(request, 'diagnosis/feedback.html', {
        'form': form,
        'diagnosis': diagnosis,
        'result': result
    })


def crop_list_view(request):
    crops = Crop.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        crops = crops.filter(
            Q(name__icontains=search_query) |
            Q(scientific_name__icontains=search_query)
        )
    
    paginator = Paginator(crops, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'diagnosis/crops.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def disease_list_view(request):
    diseases = Disease.objects.all()
    
    search_query = request.GET.get('search')
    severity_filter = request.GET.get('severity')
    
    if search_query:
        diseases = diseases.filter(
            Q(name__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )
    
    if severity_filter:
        diseases = diseases.filter(severity=severity_filter)
    
    paginator = Paginator(diseases, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'diagnosis/diseases.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'severity_filter': severity_filter,
        'severity_choices': Disease.SEVERITY_CHOICES
    })


def disease_detail_view(request, disease_id):
    disease = get_object_or_404(Disease, id=disease_id)
    
    context = {
        'disease': disease,
        'related_crops': disease.crops.all(),
    }
    
    return render(request, 'diagnosis/disease_detail.html', context)
