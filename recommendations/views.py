from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from diagnosis.models import Diagnosis
from .models import Recommendation, SavedRecommendation
from .forms import RecommendationForm

@login_required
def index(request):
    if request.user.is_farmer:
        saved_recs = SavedRecommendation.objects.filter(user=request.user).select_related('recommendation')
        return render(request, 'recommendations/index.html', {
            'recommendations': saved_recs,
            'is_farmer': True
        })
    else:
        recommendations = Recommendation.objects.filter(is_approved=True)
        return render(request, 'recommendations/index.html', {
            'recommendations': recommendations,
            'is_farmer': False
        })

@login_required
def create_recommendation(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.diagnosis = diagnosis
            recommendation.created_by = request.user
            recommendation.is_approved = not request.user.is_farmer
            recommendation.save()
            
            messages.success(request, 'Recommendation created successfully!')
            return redirect('recommendations:detail', recommendation.id)
    else:
        initial_data = {
            'title': f"Treatment for {diagnosis.result['disease']}",
            'description': f"Recommended treatment plan for {diagnosis.result['disease']} detected in {diagnosis.result['affected_part']}",
            'steps': diagnosis.result['recommendations']
        }
        form = RecommendationForm(initial=initial_data)
    
    return render(request, 'recommendations/create.html', {
        'form': form,
        'diagnosis': diagnosis
    })

@login_required
def recommendation_detail(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    is_saved = SavedRecommendation.objects.filter(
        user=request.user,
        recommendation=recommendation
    ).exists()
    
    return render(request, 'recommendations/detail.html', {
        'recommendation': recommendation,
        'is_saved': is_saved,
        'can_edit': request.user == recommendation.created_by or request.user.is_admin
    })

@login_required
def save_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    
    if request.method == 'POST':
        _, created = SavedRecommendation.objects.get_or_create(
            user=request.user,
            recommendation=recommendation,
            defaults={'notes': request.POST.get('notes', '')}
        )
        
        if created:
            messages.success(request, 'Recommendation saved to your account!')
        else:
            messages.info(request, 'You already saved this recommendation')
    
    return redirect('recommendations:detail', recommendation_id)

@login_required
def saved_recommendations(request):
    saved_recs = SavedRecommendation.objects.filter(user=request.user).select_related('recommendation')
    return render(request, 'recommendations/saved.html', {'recommendations': saved_recs})