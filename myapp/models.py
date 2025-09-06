from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta
import os
from PIL import Image

def validate_image_file(value):
    """Custom validator for image files"""
    # Check file extension
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}'
        )
    
    # Check file size (max 10MB)
    if value.size > 10 * 1024 * 1024:  # 10MB in bytes
        raise ValidationError('File size cannot exceed 10MB.')
    
    # Validate image format using PIL
    try:
        img = Image.open(value)
        img.verify()  # Verify it's actually an image
        
        # Reset file pointer for future use
        value.seek(0)
        
        # Check dimensions (optional - you can adjust these values)
        img = Image.open(value)
        if img.width > 4000 or img.height > 4000:
            raise ValidationError('Image dimensions cannot exceed 4000x4000 pixels.')
        
        # Reset file pointer again
        value.seek(0)
        
    except Exception as e:
        raise ValidationError(f'Invalid image file: {str(e)}')

def validate_jpg_png_only(value):
    """Validator that only allows JPG/JPEG and PNG files"""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError('Only JPG/JPEG and PNG files are allowed.')
    
    # Check file size (max 10MB)
    if value.size > 10 * 1024 * 1024:  # 10MB in bytes
        raise ValidationError('File size cannot exceed 10MB.')
    
    # Validate image format using PIL
    try:
        img = Image.open(value)
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            raise ValidationError('File must be a valid JPG/JPEG or PNG image.')
        
        # Check dimensions
        if img.width > 4000 or img.height > 4000:
            raise ValidationError('Image dimensions cannot exceed 4000x4000 pixels.')
        
        # Reset file pointer
        value.seek(0)
        
    except Exception as e:
        raise ValidationError(f'Invalid image file: {str(e)}')

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="CSS class for icon")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('traveller', 'Traveller'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='vehicles/', 
        null=True, 
        blank=True,
        validators=[validate_jpg_png_only],
        help_text="Upload JPG/JPEG or PNG image. Max size: 10MB, Max dimensions: 4000x4000px"
    )
    description = models.TextField()
    features = models.TextField(help_text="Comma-separated features")
    is_available = models.BooleanField(default=True)
    mileage = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.name}"
    
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(',') if feature.strip()]
    
    def get_price_per_24h(self):
        return self.price_per_day
    
    def clean(self):
        """Custom validation for the model"""
        super().clean()
        
        if self.image:
            # Additional validation when saving
            try:
                # Check if file exists and is accessible
                if hasattr(self.image, 'file'):
                    # Validate file size
                    if self.image.size > 10 * 1024 * 1024:  # 10MB
                        raise ValidationError('Image file size cannot exceed 10MB.')
                    
                    # Validate image format
                    img = Image.open(self.image)
                    if img.format not in ['JPEG', 'JPG', 'PNG']:
                        raise ValidationError('Only JPG/JPEG or PNG images are allowed for vehicles.')
                    
                    # Validate dimensions
                    if img.width > 4000 or img.height > 4000:
                        raise ValidationError('Image dimensions cannot exceed 4000x4000 pixels.')
                    
                    # Reset file pointer
                    self.image.seek(0)
                    
            except Exception as e:
                raise ValidationError(f'Image validation failed: {str(e)}')
    
    def save(self, *args, **kwargs):
        """Override save method to ensure validation"""
        self.clean()
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    driving_license = models.CharField(max_length=50)
    id_proof = models.CharField(max_length=50)
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True,
        validators=[validate_image_file],
        help_text="Upload image (JPG, PNG, WebP). Max size: 10MB, Max dimensions: 4000x4000px"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=200)
    return_location = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.vehicle.name}"
    
    def get_duration_hours(self):
        duration = self.end_date - self.start_date
        return duration.total_seconds() / 3600
    
    def get_duration_days(self):
        duration = self.end_date - self.start_date
        return duration.days
    
    def calculate_total_amount(self):
        hours = self.get_duration_hours()
        if hours <= 24:
            return self.vehicle.price_per_hour * Decimal(str(round(hours, 2)))
        else:
            days = self.get_duration_days()
            return self.vehicle.price_per_day * days

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.vehicle.name}"
    
    class Meta:
        unique_together = ('user', 'vehicle')
