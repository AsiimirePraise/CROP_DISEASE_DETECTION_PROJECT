from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from diagnosis.models import DiagnosisRequest
from recommendations.models import Recommendation

from django.contrib.auth import get_user_model
User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This handles both User and Profile creation
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
    # Superuser gets admin dashboard
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html', {'user_role': 'admin'})

    try:
        # Ensure user has a profile
        if hasattr(request.user, 'profile'):
            user_role = request.user.profile.get_user_role()
        
        if user_role == 'farmer':
            # Redirect to the diagnosis app's index view
            return redirect('diagnosis:index')
        elif user_role == 'agronomist':
            return render(request, 'dashboard/agronomist_dashboard.html', {'user_role': 'agronomist'})
        elif user_role == 'extension_worker':
                farmers = User.objects.filter(profile__farmer=True)
                # Total number of farmers
                farmer_count = User.objects.filter(profile__farmer=True).count()

                # Active cases: maybe diagnosis entries with an "active" status
                active_cases = DiagnosisRequest.objects.all().count()

                # Pending visits or treatment recommendations
                pending_visits = Recommendation.objects.all().count()

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
                    'pending_visits': pending_visits,
                    'user_role': 'extension_worker'
                })
        else:
            messages.error(request, "Please select your role in your profile.")
            return redirect('profile')  # Redirect to profile page to set role
            
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup.")
        return redirect('profile')  # Redirect to profile page


def logout_view(request):
    """
    Logout view - logs out the user and redirects to home page
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
