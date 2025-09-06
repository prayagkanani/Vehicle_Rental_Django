from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Vehicle, Category, Booking, Review, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, BookingForm, ReviewForm, VehicleSearchForm
from datetime import datetime, timedelta

def home(request):
    """Home page with featured vehicles and categories"""
    featured_vehicles = Vehicle.objects.filter(is_available=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    
    # Get vehicle counts by type
    bike_count = Vehicle.objects.filter(vehicle_type='bike', is_available=True).count()
    car_count = Vehicle.objects.filter(vehicle_type='car', is_available=True).count()
    traveller_count = Vehicle.objects.filter(vehicle_type='traveller', is_available=True).count()
    
    context = {
        'featured_vehicles': featured_vehicles,
        'categories': categories,
        'bike_count': bike_count,
        'car_count': car_count,
        'traveller_count': traveller_count,
    }
    return render(request, 'myapp/home.html', context)

def vehicle_list(request):
    """Display all available vehicles with search and filtering"""
    vehicles = Vehicle.objects.filter(is_available=True).order_by('-created_at')
    search_form = VehicleSearchForm(request.GET)
    
    if search_form.is_valid():
        vehicle_type = search_form.cleaned_data.get('vehicle_type')
        brand = search_form.cleaned_data.get('brand')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        seats = search_form.cleaned_data.get('seats')
        
        if vehicle_type:
            vehicles = vehicles.filter(vehicle_type=vehicle_type)
        if brand:
            vehicles = vehicles.filter(brand__icontains=brand)
        if min_price:
            vehicles = vehicles.filter(price_per_day__gte=min_price)
        if max_price:
            vehicles = vehicles.filter(price_per_day__lte=max_price)
        if seats:
            vehicles = vehicles.filter(seats__gte=seats)
    
    # Enhanced pagination with better error handling
    paginator = Paginator(vehicles, 12)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    # Get page range for better pagination display
    page_range = paginator.get_elided_page_range(
        page_obj.number, 
        on_each_side=2, 
        on_ends=1
    )
    
    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'search_form': search_form,
        'total_vehicles': vehicles.count(),
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }
    return render(request, 'myapp/vehicle_list.html', context)

def vehicle_detail(request, vehicle_id):
    """Display detailed information about a specific vehicle"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    reviews = Review.objects.filter(vehicle=vehicle).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user has already reviewed this vehicle
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, vehicle=vehicle).first()
    
    # Get similar vehicles
    similar_vehicles = Vehicle.objects.filter(
        vehicle_type=vehicle.vehicle_type,
        is_available=True
    ).exclude(id=vehicle.id)[:4]
    
    context = {
        'vehicle': vehicle,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_review': user_review,
        'similar_vehicles': similar_vehicles,
    }
    return render(request, 'myapp/vehicle_detail.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                driving_license=form.cleaned_data['driving_license'],
                id_proof=form.cleaned_data['id_proof'],
            )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    """User profile view"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if profile is None:
                profile = form.save(commit=False)
                profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'form': form,
        'bookings': bookings,
    }
    return render(request, 'myapp/profile.html', context)

@login_required
def book_vehicle(request, vehicle_id):
    """Book a vehicle view"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    if not vehicle.is_available:
        messages.error(request, 'This vehicle is not available for booking.')
        return redirect('vehicle_detail', vehicle_id=vehicle.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.vehicle = vehicle
                booking.total_amount = booking.calculate_total_amount()
                booking.save()
                
                messages.success(request, 'Vehicle booked successfully!')
                return redirect('booking_confirmation', booking_id=booking.id)
            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
        else:
            # Display form errors to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BookingForm()
    
    context = {
        'vehicle': vehicle,
        'form': form,
    }
    return render(request, 'myapp/book_vehicle.html', context)

@login_required
def booking_confirmation(request, booking_id):
    """Booking confirmation view"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'myapp/booking_confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    """Display user's bookings with pagination"""
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination for bookings
    paginator = Paginator(all_bookings, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    # Get page range for better pagination display
    page_range = paginator.get_elided_page_range(
        page_obj.number, 
        on_each_side=2, 
        on_ends=1
    )
    
    # Filter bookings for statistics
    active_bookings = all_bookings.filter(status__in=['pending', 'confirmed', 'active'])
    pending_bookings = all_bookings.filter(status='pending')
    completed_bookings = all_bookings.filter(status='completed')
    
    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'all_bookings': all_bookings,  # For statistics
        'active_bookings': active_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }
    return render(request, 'myapp/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('my_bookings')

@login_required
@require_POST
def add_review(request, vehicle_id):
    """Add a review for a vehicle"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.vehicle = vehicle
        review.save()
        messages.success(request, 'Review added successfully!')
    else:
        messages.error(request, 'Error adding review.')
    
    return redirect('vehicle_detail', vehicle_id=vehicle.id)

def about(request):
    """About page"""
    return render(request, 'myapp/about.html')

def contact(request):
    """Contact page"""
    return render(request, 'myapp/contact.html')

def category_vehicles(request, category_id):
    """Display vehicles by category with pagination"""
    category = get_object_or_404(Category, id=category_id)
    vehicles = Vehicle.objects.filter(category=category, is_available=True).order_by('-created_at')
    all_categories = Category.objects.all()
    
    # Pagination for category vehicles
    paginator = Paginator(vehicles, 9)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    # Get page range for better pagination display
    page_range = paginator.get_elided_page_range(
        page_obj.number, 
        on_each_side=2, 
        on_ends=1
    )
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'page_range': page_range,
        'vehicles': page_obj,  # Use paginated vehicles
        'all_categories': all_categories,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }
    return render(request, 'myapp/category_vehicles.html', context)
