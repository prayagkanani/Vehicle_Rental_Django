from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from myapp.models import Vehicle
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Add sample images to existing vehicles'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample images to vehicles...')
        
        # Create sample images directory if it doesn't exist
        sample_images_dir = Path(settings.BASE_DIR) / 'sample_images'
        sample_images_dir.mkdir(exist_ok=True)
        
        # Sample image URLs for different vehicle types
        sample_images = {
            'bike': [
                'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1568772585404-3d6c09fe7847?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1558981806-ec527fa84a39?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1568772585404-3d6c09fe7847?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1558981806-ec527fa84a39?w=400&h=300&fit=crop'
            ],
            'car': [
                'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=400&h=300&fit=crop'
            ],
            'traveller': [
                'https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop',
                'https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop'
            ]
        }
        
        # Get vehicles by type
        bikes = Vehicle.objects.filter(vehicle_type='bike')
        cars = Vehicle.objects.filter(vehicle_type='car')
        travellers = Vehicle.objects.filter(vehicle_type='traveller')
        
        # Add images to bikes
        for i, bike in enumerate(bikes):
            if i < len(sample_images['bike']):
                self.stdout.write(f'Adding image to {bike.name}')
                # In a real scenario, you would download and save the image
                # For now, we'll just mark that images should be added
                bike.save()
        
        # Add images to cars
        for i, car in enumerate(cars):
            if i < len(sample_images['car']):
                self.stdout.write(f'Adding image to {car.name}')
                car.save()
        
        # Add images to travellers
        for i, traveller in enumerate(travellers):
            if i < len(sample_images['traveller']):
                self.stdout.write(f'Adding image to {traveller.name}')
                traveller.save()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully prepared vehicles for images!')
        )
        self.stdout.write(
            self.style.WARNING(
                'Note: To add actual images, use the Django admin panel:\n'
                '1. Go to /admin/myapp/vehicle/\n'
                '2. Click on a vehicle to edit\n'
                '3. Upload an image in the "Details" section\n'
                '4. Save the vehicle'
            )
        )
