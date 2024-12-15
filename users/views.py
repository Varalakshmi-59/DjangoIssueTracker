from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import UserRegistrationForm, CustomUserChangeForm
from .models import User
from main.models import Issue, Project
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('main:dashboard')  # Redirect to home if user is already logged in
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Get the next parameter if it exists, otherwise go to home
                next_url = request.GET.get('next', 'main:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url="users:login")
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    # Get user statistics
    context = {
        'form': form,
        'assigned_issues': Issue.objects.filter(assigned_to=request.user).order_by('-created_at')[:5],
        'created_issues': Issue.objects.filter(created_by=request.user).order_by('-created_at')[:5],
        'projects': Project.objects.filter(members=request.user).order_by('-created_at')[:5],
        'total_assigned_issues': Issue.objects.filter(assigned_to=request.user).count(),
        'total_created_issues': Issue.objects.filter(created_by=request.user).count(),
        'total_projects': Project.objects.filter(members=request.user).count(),
    }
    
    return render(request, 'users/profile.html', context)

@login_required(login_url="users:login")
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_update.html', {'form': form})

@login_required(login_url="users:login")
def dashboard(request):
    # Get recent activities and statistics
    context = {
        'assigned_issues': Issue.objects.filter(assigned_to=request.user)
                                      .order_by('-created_at')[:5],
        'created_issues': Issue.objects.filter(created_by=request.user)
                                     .order_by('-created_at')[:5],
        'projects': Project.objects.filter(members=request.user)
                                 .order_by('-created_at')[:5],
        'stats': {
            'open_issues': Issue.objects.filter(assigned_to=request.user, status='OPEN').count(),
            'in_progress_issues': Issue.objects.filter(assigned_to=request.user, status='IN_PROGRESS').count(),
            'completed_issues': Issue.objects.filter(assigned_to=request.user, status='COMPLETED').count(),
        }
    }
    return render(request, 'users/dashboard.html', context)

@login_required(login_url="users:login")
def user_list(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': User.ROLE_CHOICES,
    }
    
    return render(request, 'users/user_list.html', context)

@login_required(login_url="users:login")
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    
    context = {
        'user_profile': user,
        'assigned_issues': Issue.objects.filter(assigned_to=user).order_by('-created_at')[:5],
        'created_issues': Issue.objects.filter(created_by=user).order_by('-created_at')[:5],
        'projects': Project.objects.filter(members=user).order_by('-created_at')[:5],
        'stats': {
            'total_assigned_issues': Issue.objects.filter(assigned_to=user).count(),
            'total_created_issues': Issue.objects.filter(created_by=user).count(),
            'total_projects': Project.objects.filter(members=user).count(),
        }
    }
    
    return render(request, 'users/user_detail.html', context)

@login_required(login_url="users:login")
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly.')
            return redirect('accounts:change_password')
        
        if new_password1 != new_password2:
            messages.error(request, "The two password fields didn't match.")
            return redirect('accounts:change_password')
        
        request.user.set_password(new_password1)
        request.user.save()
        login(request, request.user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('accounts:profile')
    
    return render(request, 'users/change_password.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('users:login')