
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Recommendation, Treatment, TreatmentTracking, PreventiveMeasure


@login_required
def recommendation_list_view(request):
    # Get recommendations for user's diagnoses
    recommendations = Recommendation.objects.filter(
        diagnosis_result__diagnosis_request__user=request.user
    ).select_related('diagnosis_result__diagnosis_request')
    
    paginator = Paginator(recommendations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recommendations/list.html', {'page_obj': page_obj})


@login_required
def recommendation_detail_view(request, recommendation_id):
    recommendation = get_object_or_404(
        Recommendation,
        id=recommendation_id,
        diagnosis_result__diagnosis_request__user=request.user
    )
    
    treatment_recommendations = recommendation.treatmentrecommendation_set.all()
    
    context = {
        'recommendation': recommendation,
        'treatment_recommendations': treatment_recommendations,
    }
    
    return render(request, 'recommendations/detail.html', context)


@login_required
def treatment_tracking_view(request, recommendation_id):
    recommendation = get_object_or_404(
        Recommendation,
        id=recommendation_id,
        diagnosis_result__diagnosis_request__user=request.user
    )
    
    tracking_records = TreatmentTracking.objects.filter(
        user=request.user,
        recommendation=recommendation
    )
    
    context = {
        'recommendation': recommendation,
        'tracking_records': tracking_records,
    }
    
    return render(request, 'recommendations/tracking.html', context)


def treatment_list_view(request):
    treatments = Treatment.objects.all()
    
    search_query = request.GET.get('search')
    treatment_type = request.GET.get('type')
    organic_only = request.GET.get('organic')
    
    if search_query:
        treatments = treatments.filter(
            Q(name__icontains=search_query) |
            Q(active_ingredients__icontains=search_query)
        )
    
    if treatment_type:
        treatments = treatments.filter(treatment_type=treatment_type)
    
    if organic_only:
        treatments = treatments.filter(organic_friendly=True)
    
    paginator = Paginator(treatments, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'treatment_type': treatment_type,
        'organic_only': organic_only,
        'treatment_types': Treatment.TREATMENT_TYPES,
    }
    
    return render(request, 'recommendations/treatments.html', context)


def treatment_detail_view(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    context = {
        'treatment': treatment,
        'related_diseases': treatment.diseases.all(),
    }
    
    return render(request, 'recommendations/treatment_detail.html', context)


def preventive_measures_view(request):
    measures = PreventiveMeasure.objects.all()
    
    search_query = request.GET.get('search')
    cost_filter = request.GET.get('cost')
    difficulty_filter = request.GET.get('difficulty')
    
    if search_query:
        measures = measures.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if cost_filter:
        measures = measures.filter(implementation_cost=cost_filter)
    
    if difficulty_filter:
        measures = measures.filter(difficulty_level=difficulty_filter)
    
    paginator = Paginator(measures, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'cost_filter': cost_filter,
        'difficulty_filter': difficulty_filter,
    }
    
    return render(request, 'recommendations/preventive.html', context)
