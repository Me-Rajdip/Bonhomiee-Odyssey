from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import TravelRequest
from .forms import TravelRequestForm
# travel/views.py
import time
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.conf import settings
from .forms import UserRegistrationForm
from django.core.exceptions import ValidationError

from django.http import JsonResponse

def create_travel_request(request):
    if request.method == 'POST':
        form = TravelRequestForm(request.POST)
        if form.is_valid():
            travel_request = form.save(commit=False)
            travel_request.user = request.user
            travel_request.status = 'pending'  # Default status
            travel_request.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('travel:travel_request_list?status=pending')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TravelRequestForm()
    
    # Check if user has any requests that were recently verified
    if request.user.is_authenticated:
        recently_verified = TravelRequest.objects.filter(
            user=request.user,
            status='approved',
            is_notified=False
        ).exists()
        
        if recently_verified:
            TravelRequest.objects.filter(
                user=request.user,
                status='approved',
                is_notified=False
            ).update(is_notified=True)
            return redirect('travel:travel_request_list?status=verified')
    
    return render(request, 'travel/create_request.html', {'form': form})

def travel_request_list(request):
    status = request.GET.get('status')
    requests = TravelRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'travel/request_list.html', {
        'travel_requests': requests,
        'status': status
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Using email as username
            user.save()
            
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Bonhomiee Odyssey!')
            return redirect('home')  # Replace 'home' with your desired redirect URL
        
        # If form is invalid, collect all error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.title()}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'travel/register.html', {'form': form})

# def travel_request_create(request):
#     if request.method == 'POST':
#         form = TravelRequestForm(request.POST)
#         if form.is_valid():
#             travel_request = form.save(commit=False)
#             travel_request.user = request.user
#             travel_request.status = 'pending'  # Default status
#             travel_request.save()
            
#             if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#                 return JsonResponse({'success': True, 'reset_form': True})
#             return redirect('travel:submission_success')
#     else:
#         form = TravelRequestForm()
    
#     return render(request, 'travel/travel_request_form.html', {'form': form})

def some_view(request):
    verification_status = None
    if request.user.is_authenticated:
        # Check if user has any recently approved/rejected requests
        recent_request = TravelRequest.objects.filter(
            user=request.user,
            status__in=['approved', 'rejected'],
            notification_sent=False
        ).first()
        
        if recent_request:
            verification_status = recent_request.status
            recent_request.notification_sent = True
            recent_request.save()
    
    return render(request, 'template.html', {
        'verification_status': verification_status
    })

def home_page(request):
    """Render the home page with login option"""
    return render(request, 'travel/home_page.html')

def custom_login(request):
    """Redirect to Django's built-in login view"""
    return redirect('login')

def custom_logout(request):
    """Handle logout functionality"""
    logout(request)
    return redirect('home')

from django.views.generic import ListView

class TravelRequestListView(ListView):
    model = TravelRequest
    template_name = 'travel/travel_request_list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        # For demo, show all requests (filter by user in real application)
        return TravelRequest.objects.all().order_by('-created_at')
    
from django.views.generic import ListView

class TravelRequestListView(ListView):
    model = TravelRequest
    template_name = 'travel/travel_request_list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        # For demo, show all requests (filter by user in real application)
        return TravelRequest.objects.all().order_by('-created_at')
    


# @login_required
# def travel_request_list(request):
#     """List travel requests (different views for admin vs regular users)"""
#     if request.user.is_superuser:
#         requests = TravelRequest.objects.all()
#     else:
#         requests = TravelRequest.objects.filter(submitted_by=request.user)
#     return render(request, 'travel/travel_request_list.html', {'requests': requests})



# @login_required
# def travel_request_create(request):
#     """Create new travel request"""
#     if request.method == 'POST':
#         form = TravelRequestForm(request.POST, user=request.user)
#         if form.is_valid():
#             travel_request = form.save(commit=False)
#             travel_request.submitted_by = request.user
#             travel_request.save()
#             return redirect('travel:travel_request_list')
#     else:
#         form = TravelRequestForm(user=request.user)
#     return render(request, 'travel/travel_request_form.html', {'form': form})

@login_required
def travel_request_update(request, pk):
    """Update existing travel request"""
    travel_request = get_object_or_404(TravelRequest, pk=pk, submitted_by=request.user)
    if request.method == 'POST':
        form = TravelRequestForm(request.POST, instance=travel_request, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('travel:travel_request_list')
    else:
        form = TravelRequestForm(instance=travel_request, user=request.user)
    return render(request, 'travel/travel_request_form.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import TravelRequest
from .forms import TravelRequestForm
from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404

@login_required
def travel_request_detail(request, pk):
    travel_request = get_object_or_404(TravelRequest, pk=pk, user=request.user)
    return render(request, 'travel/travel_request_detail.html', {
        'request': travel_request
    })

@login_required
def travel_request_update(request, pk):
    travel_request = get_object_or_404(TravelRequest, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TravelRequestForm(request.POST, instance=travel_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('travel:travel_request_detail', pk=travel_request.pk)
    else:
        form = TravelRequestForm(instance=travel_request)
    return render(request, 'travel/travel_request_form.html', {'form': form})

@login_required
def travel_request_delete(request, pk):
    travel_request = get_object_or_404(TravelRequest, pk=pk, user=request.user)
    if request.method == 'POST':
        travel_request.delete()
        messages.success(request, 'Request deleted successfully!')
        return redirect('travel:travel_request_list')
    return render(request, 'travel/travel_request_confirm_delete.html', {
        'object': travel_request
    })

@login_required
def travel_request_create(request):
    if request.method == 'POST':
        form = TravelRequestForm(request.POST)
        if form.is_valid():
            travel_request = form.save(commit=False)
            travel_request.user = request.user  # Set the user before saving
            travel_request.status = 'pending'
            travel_request.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Your travel request has been submitted successfully!'
                })
            messages.success(request, 'Your travel request has been submitted successfully!')
            return redirect('travel:submission_success')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data()
                }, status=400)
    else:
        form = TravelRequestForm()
    
    return render(request, 'travel/travel_request_form.html', {'form': form})

@login_required
def submission_success(request):
    return render(request, 'travel/submission_success.html')

@login_required
def travel_request_list(request):
    # Check for pending verification notifications
    verified_requests = TravelRequest.objects.filter(
        user=request.user,
        admin_verified=True,
        verification_notification_sent=False
    )
    
    for req in verified_requests:
        req.verification_notification_sent = True
        req.save()
    
    requests = TravelRequest.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'travel/travel_request_list.html', {
        'requests': requests,
        'has_pending_notifications': verified_requests.exists()
    })


