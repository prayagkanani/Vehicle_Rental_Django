from django.core.management.base import BaseCommand
from myapp.models import Category, Vehicle
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add 6 new vehicles to the existing database'

    def handle(self, *args, **options):
        self.stdout.write('Adding 6 new vehicles...')
        
        # New vehicles to add
        new_vehicles = [
            # New Premium Bike
            {
                'name': 'KTM Duke 390',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'bike',
                'brand': 'KTM',
                'model': 'Duke 390',
                'year': 2024,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 2,
                'price_per_day': Decimal('1200.00'),
                'price_per_hour': Decimal('120.00'),
                'description': 'High-performance naked street bike with aggressive styling and advanced electronics.',
                'features': 'High performance, Advanced electronics, Aggressive styling, ABS, LED lighting',
                'mileage': '30 km/l',
                'color': 'Orange'
            },
            
            # New Economy Car
            {
                'name': 'Tata Punch',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'car',
                'brand': 'Tata',
                'model': 'Punch',
                'year': 2024,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 5,
                'price_per_day': Decimal('1800.00'),
                'price_per_hour': Decimal('180.00'),
                'description': 'Compact SUV with modern design, good safety ratings, and excellent value for money.',
                'features': 'Compact SUV, Modern design, Good safety ratings, High ground clearance, Value for money',
                'mileage': '18 km/l',
                'color': 'Tropical Mist'
            },
            
            # New Family Car
            {
                'name': 'MG Hector Plus',
                'category': Category.objects.get(name='Family'),
                'vehicle_type': 'car',
                'brand': 'MG',
                'model': 'Hector Plus',
                'year': 2024,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 6,
                'price_per_day': Decimal('3200.00'),
                'price_per_hour': Decimal('320.00'),
                'description': 'Premium 6-seater SUV with panoramic sunroof and advanced connectivity features.',
                'features': '6 seats, Panoramic sunroof, Advanced connectivity, Premium interior, Spacious cabin',
                'mileage': '16 km/l',
                'color': 'Glaze Red'
            },
            
            # New Premium Car
            {
                'name': 'BMW X1',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'car',
                'brand': 'BMW',
                'model': 'X1',
                'year': 2024,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'seats': 5,
                'price_per_day': Decimal('4500.00'),
                'price_per_hour': Decimal('450.00'),
                'description': 'Luxury compact SUV with premium features, excellent driving dynamics, and sophisticated design.',
                'features': 'Luxury features, Premium interior, Advanced safety, Excellent driving dynamics, Sophisticated design',
                'mileage': '14 km/l',
                'color': 'Alpine White'
            },
            
            # New Economy Bike
            {
                'name': 'Hero Splendor Plus',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'bike',
                'brand': 'Hero',
                'model': 'Splendor Plus',
                'year': 2024,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 2,
                'price_per_day': Decimal('400.00'),
                'price_per_hour': Decimal('40.00'),
                'description': 'India\'s most trusted commuter bike with excellent fuel efficiency and low maintenance.',
                'features': 'Excellent fuel efficiency, Low maintenance, Trusted brand, Comfortable ride, Good resale value',
                'mileage': '65 km/l',
                'color': 'Black'
            },
            
            # New Premium Traveller
            {
                'name': 'Mercedes-Benz Sprinter',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'traveller',
                'brand': 'Mercedes-Benz',
                'model': 'Sprinter',
                'year': 2024,
                'fuel_type': 'Diesel',
                'transmission': 'Automatic',
                'seats': 20,
                'price_per_day': Decimal('8000.00'),
                'price_per_hour': Decimal('800.00'),
                'description': 'Ultra-luxury traveller with premium amenities, maximum comfort, and advanced safety features.',
                'features': '20 seats, Ultra-luxury amenities, Premium interior, Advanced safety, Entertainment system, Climate control',
                'mileage': '8 km/l',
                'color': 'Obsidian Black'
            }
        ]
        
        # Add new vehicles
        for vehicle_data in new_vehicles:
            vehicle, created = Vehicle.objects.get_or_create(
                name=vehicle_data['name'],
                defaults=vehicle_data
            )
            if created:
                self.stdout.write(f'Created new vehicle: {vehicle.name}')
            else:
                self.stdout.write(f'Vehicle already exists: {vehicle.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully added 6 new vehicles to the database!')
        )
