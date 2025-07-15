from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

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
    from diagnosis.models import Issue
    issues = Issue.objects.all()
    return render(request, 'adminpanel/manage_issues.html', {'issues': issues})

@admin_required
def manage_datasets(request):
    # Replace with your actual Dataset model
    from yourapp.models import ImageDataset
    datasets = ImageDataset.objects.all()
    return render(request, 'adminpanel/manage_datasets.html', {'datasets': datasets})

@admin_required
def retrain_model(request):
    if request.method == 'POST':
        # Add your actual retraining logic here
        message = "Model retraining started successfully."
        return render(request, 'adminpanel/retrain_model.html', {'message': message})
    return render(request, 'adminpanel/retrain_model.html')
