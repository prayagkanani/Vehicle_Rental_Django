from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Booking, Review
from datetime import datetime, timedelta

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    driving_license = forms.CharField(max_length=50, required=True)
    id_proof = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'driving_license', 'id_proof', 'profile_picture')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'driving_license': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local', 
                'class': 'form-control',
                'min': '2025-08-13T00:00'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local', 
                'class': 'form-control',
                'min': '2025-08-13T00:00'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'pickup_location', 'return_location')
        widgets = {
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'return_location': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            # Ensure both dates are timezone-aware
            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date)
            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date)
            
            # Update cleaned_data with timezone-aware dates
            cleaned_data['start_date'] = start_date
            cleaned_data['end_date'] = end_date
            
            if start_date <= timezone.now():
                raise forms.ValidationError("Start date must be in the future")
            
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date")
            
            # Minimum booking duration of 1 hour
            duration = end_date - start_date
            if duration.total_seconds() < 3600:
                raise forms.ValidationError("Minimum booking duration is 1 hour")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for better user experience
        if not self.instance.pk:  # Only for new bookings
            now = timezone.now()
            # Set start date to next hour
            start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            # Set end date to start date + 24 hours
            end_time = start_time + timedelta(hours=24)
            
            self.fields['start_date'].initial = start_time.strftime('%Y-%m-%dT%H:%M')
            self.fields['end_date'].initial = end_time.strftime('%Y-%m-%dT%H:%M')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class VehicleSearchForm(forms.Form):
    vehicle_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('bike', 'Bike'), ('car', 'Car'), ('traveller', 'Traveller')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'}))
    seats = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Seats'}))
