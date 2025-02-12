from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import SignUPForm, ServiceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def home_view(request):
    context = {}
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_dashboard') 
    if request.user.is_authenticated:
        # get all service requests for logged in user, newest first
        context['service_requests'] = Service.objects.filter(
            user=request.user
        ).order_by('-created_at')
    return render(request, 'base.html', context)

def signup_view(request):

    try:
        if request.method == 'GET':
           form = SignUPForm()
           return render(request, 'signup.html', {'form': form})

        elif request.method == 'POST':
            form = SignUPForm(request.POST)
            if form.is_valid():
               form.save()
               return redirect('login') 
            return render(request, 'signup.html', {'form': form})

    except Exception as e:
        print(f" There is an issue with signup page: {e}")
        return HttpResponse(f"<h1>There is an issue with signup page: {e}</h1>")

def login_view(request):
    if request.method == "POST":
        # process login credentials
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard') #staff redirect
            return redirect('home')  # redirect to home after login
        else:
            # error msg for template
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login') 
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def service_request_view(request):
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            messages.success(request, f'Service request submitted successfully! Service Request No. is: {service.ser_req_no}')
            return redirect('home')
    else:
        form = ServiceForm()
    
    return render(request, 'service_form.html', {'form': form})

def track_request_view(request):
    service_requests = None
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '').strip()
        
        try:
            # Try to find by service request number
            if search_query.isdigit():
                service_requests = Service.objects.filter(ser_req_no=int(search_query))
            
            # If not found, try account number or email
            if not service_requests or not service_requests.exists():
                service_requests = Service.objects.filter(
                    Q(user__util_acc_no__iexact=search_query) |
                    Q(user__email__iexact=search_query)
                ).order_by('-created_at')
                
        except (ValueError, Service.DoesNotExist):
            service_requests = None

    return render(request, 'track_request.html', {
        'service_requests': service_requests
    })

@login_required
@staff_member_required
def staff_dashboard(request):
    service_requests = Service.objects.all().order_by('-created_at')
    search_query = request.GET.get('q', '')
    
    if search_query:
        service_requests = Service.objects.filter(
            Q(user__email__iexact=search_query) |
            Q(ser_req_no=search_query) |
            Q(user__util_acc_no__iexact=search_query) 
        )
    
    return render(request, 'staff_login.html', {
        'service_requests': service_requests,
        'search_query': search_query
    })

@login_required
@staff_member_required
def service_update_view(request, pk): 
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.status = request.POST.get('status')
        service.note = request.POST.get('note')
        service.save()
        messages.success(request, 'Service request updated successfully!')
        return redirect('staff_dashboard')
    return redirect('staff_dashboard')

@login_required
@staff_member_required
def service_docs(request, pk): #file view
    service = get_object_or_404(Service, pk=pk)
    if service.files:
        return redirect(service.files.url)
    messages.error(request, "No file attached to this service request")
    return redirect('staff_dashboard')
