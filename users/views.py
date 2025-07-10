from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


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
    """Main dashboard that redirects based on user role"""
    try:
        # Ensure user has a profile
        if hasattr(request.user, 'profile'):
            user_role = request.user.profile.get_user_role()
        
            if user_role == 'farmer':
                # Redirect to the diagnosis app's index view
                return redirect('diagnosis:index')
            elif user_role == 'agronomist':
                # Redirect to the agronomist app's index view
                return redirect('agronomist:index')  # Change 'agronomist:index' to your actual agronomist app URL name
            elif user_role == 'extension_worker':
                return render(request,'dashboard/dashboard.html', {'user_role': 'extension_worker'})
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