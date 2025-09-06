from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Vehicle, UserProfile, Booking

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model', 'vehicle_type', 'price_per_day', 'price_per_hour', 'is_available', 'image_preview', 'created_at')
    list_filter = ('vehicle_type', 'brand', 'fuel_type', 'transmission', 'is_available', 'created_at')
    search_fields = ('name', 'brand', 'model', 'description')
    list_editable = ('is_available', 'price_per_day', 'price_per_hour')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_per_page = 25
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'vehicle_type', 'brand', 'model', 'year')
        }),
        ('Specifications', {
            'fields': ('fuel_type', 'transmission', 'seats', 'mileage', 'color')
        }),
        ('Pricing', {
            'fields': ('price_per_day', 'price_per_hour')
        }),
        ('Details', {
            'fields': ('description', 'features', 'image')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            try:
                # Validate image format
                from PIL import Image
                with Image.open(obj.image.path) as img:
                    format_info = f" ({img.format}, {img.width}x{img.height})"
                    size_info = f" ({obj.image.size / (1024*1024):.1f}MB)"
                    format_color = "green" if img.format in ['JPEG', 'JPG', 'PNG'] else "orange"
                    return mark_safe(
                        f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
                        f'<br><small style="color: {format_color};">✓ Valid{format_info}{size_info}</small>'
                    )
            except Exception as e:
                return mark_safe(
                    f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
                    f'<br><small style="color: red;">✗ Invalid: {str(e)}</small>'
                )
        return "No Image"
    image_preview.short_description = 'Image'
    image_preview.allow_tags = True

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'driving_license', 'id_proof', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'driving_license')
    list_filter = ('created_at',)
    list_per_page = 25
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'start_date', 'end_date', 'total_amount', 'created_at')
    list_filter = ('start_date', 'created_at')
    search_fields = ('user__username', 'user__email', 'vehicle__name', 'vehicle__brand')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    list_display_links = ('id', 'user', 'vehicle')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'vehicle', 'start_date', 'end_date')
        }),
        ('Location', {
            'fields': ('pickup_location', 'return_location')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'vehicle')
    



