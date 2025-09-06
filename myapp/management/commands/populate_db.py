from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Category, Vehicle
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample vehicle data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories = [
            {
                'name': 'Economy',
                'description': 'Affordable vehicles for budget-conscious customers',
                'icon_class': 'fas fa-car'
            },
            {
                'name': 'Premium',
                'description': 'High-end vehicles with luxury features',
                'icon_class': 'fas fa-star'
            },
            {
                'name': 'Family',
                'description': 'Spacious vehicles perfect for family trips',
                'icon_class': 'fas fa-users'
            }
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create vehicles
        vehicles = [
            # Bikes
            {
                'name': 'Honda Activa 6G',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'bike',
                'brand': 'Honda',
                'model': 'Activa 6G',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'seats': 2,
                'price_per_day': Decimal('500.00'),
                'price_per_hour': Decimal('50.00'),
                'description': 'Reliable and fuel-efficient scooter perfect for city commuting.',
                'features': 'Fuel efficient, Easy to handle, Low maintenance, Good mileage',
                'mileage': '60 km/l',
                'color': 'White'
            },
            {
                'name': 'TVS Jupiter',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'bike',
                'brand': 'TVS',
                'model': 'Jupiter',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'seats': 2,
                'price_per_day': Decimal('450.00'),
                'price_per_hour': Decimal('45.00'),
                'description': 'Comfortable scooter with good storage space.',
                'features': 'Good storage, Comfortable seat, Fuel efficient, Easy handling',
                'mileage': '55 km/l',
                'color': 'Red'
            },
            {
                'name': 'Yamaha R15 V4',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'bike',
                'brand': 'Yamaha',
                'model': 'R15 V4',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 2,
                'price_per_day': Decimal('800.00'),
                'price_per_hour': Decimal('80.00'),
                'description': 'Sporty bike with advanced features and great performance.',
                'features': 'Sporty design, Advanced features, High performance, LED lighting',
                'mileage': '45 km/l',
                'color': 'Blue'
            },
            
            # Cars
            {
                'name': 'Maruti Swift',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'car',
                'brand': 'Maruti Suzuki',
                'model': 'Swift',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 5,
                'price_per_day': Decimal('1500.00'),
                'price_per_hour': Decimal('150.00'),
                'description': 'Popular hatchback with great fuel efficiency and reliability.',
                'features': 'Fuel efficient, Spacious interior, Good safety ratings, Easy to drive',
                'mileage': '22 km/l',
                'color': 'White'
            },
            {
                'name': 'Honda City',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'car',
                'brand': 'Honda',
                'model': 'City',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'seats': 5,
                'price_per_day': Decimal('2500.00'),
                'price_per_hour': Decimal('250.00'),
                'description': 'Premium sedan with luxury features and comfortable ride.',
                'features': 'Luxury features, Comfortable ride, Advanced safety, Premium interior',
                'mileage': '18 km/l',
                'color': 'Silver'
            },
            {
                'name': 'Toyota Innova Crysta',
                'category': Category.objects.get(name='Family'),
                'vehicle_type': 'car',
                'brand': 'Toyota',
                'model': 'Innova Crysta',
                'year': 2023,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'seats': 7,
                'price_per_day': Decimal('3500.00'),
                'price_per_hour': Decimal('350.00'),
                'description': 'Spacious MPV perfect for family trips and group travel.',
                'features': '7 seats, Spacious interior, Good ground clearance, Family friendly',
                'mileage': '15 km/l',
                'color': 'White'
            },
            
            # Travellers
            {
                'name': 'Force Traveller',
                'category': Category.objects.get(name='Family'),
                'vehicle_type': 'traveller',
                'brand': 'Force',
                'model': 'Traveller',
                'year': 2023,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'seats': 12,
                'price_per_day': Decimal('4000.00'),
                'price_per_hour': Decimal('400.00'),
                'description': 'Large capacity vehicle ideal for group tours and corporate travel.',
                'features': '12 seats, Air conditioning, Comfortable seating, Good luggage space',
                'mileage': '12 km/l',
                'color': 'White'
            },
            {
                'name': 'Mahindra Supro',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'traveller',
                'brand': 'Mahindra',
                'model': 'Supro',
                'year': 2023,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'seats': 8,
                'price_per_day': Decimal('2500.00'),
                'price_per_hour': Decimal('250.00'),
                'description': 'Compact traveller perfect for small groups and family trips.',
                'features': '8 seats, Compact size, Good fuel efficiency, Easy to park',
                'mileage': '18 km/l',
                'color': 'Silver'
            },
            {
                'name': 'Tata Winger',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'traveller',
                'brand': 'Tata',
                'model': 'Winger',
                'year': 2023,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'seats': 15,
                'price_per_day': Decimal('5000.00'),
                'price_per_hour': Decimal('500.00'),
                'description': 'Premium traveller with luxury amenities and maximum comfort.',
                'features': '15 seats, Luxury amenities, Premium interior, Entertainment system',
                'mileage': '10 km/l',
                'color': 'Black'
            },
            
            # Additional 5 vehicles
            # Additional Bike
            {
                'name': 'Royal Enfield Classic 350',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'bike',
                'brand': 'Royal Enfield',
                'model': 'Classic 350',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 2,
                'price_per_day': Decimal('1000.00'),
                'price_per_hour': Decimal('100.00'),
                'description': 'Iconic cruiser bike with classic design and powerful engine.',
                'features': 'Classic design, Powerful engine, Comfortable ride, Heritage appeal',
                'mileage': '35 km/l',
                'color': 'Gunmetal Grey'
            },
            
            # Additional Car
            {
                'name': 'Hyundai Creta',
                'category': Category.objects.get(name='Premium'),
                'vehicle_type': 'car',
                'brand': 'Hyundai',
                'model': 'Creta',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'seats': 5,
                'price_per_day': Decimal('2800.00'),
                'price_per_hour': Decimal('280.00'),
                'description': 'Premium SUV with modern design and advanced features.',
                'features': 'SUV design, Advanced features, Spacious interior, High ground clearance',
                'mileage': '16 km/l',
                'color': 'Phantom Black'
            },
            
            # Additional Traveller
            {
                'name': 'Ashok Leyland Dost',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'traveller',
                'brand': 'Ashok Leyland',
                'model': 'Dost',
                'year': 2023,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'seats': 10,
                'price_per_day': Decimal('3000.00'),
                'price_per_hour': Decimal('300.00'),
                'description': 'Reliable traveller with good fuel efficiency and comfortable seating.',
                'features': '10 seats, Good fuel efficiency, Comfortable seating, Reliable engine',
                'mileage': '16 km/l',
                'color': 'White'
            },
            
            # Additional Bike
            {
                'name': 'Bajaj Pulsar 150',
                'category': Category.objects.get(name='Economy'),
                'vehicle_type': 'bike',
                'brand': 'Bajaj',
                'model': 'Pulsar 150',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 2,
                'price_per_day': Decimal('600.00'),
                'price_per_hour': Decimal('60.00'),
                'description': 'Popular commuter bike with sporty design and good performance.',
                'features': 'Sporty design, Good performance, Fuel efficient, Low maintenance',
                'mileage': '50 km/l',
                'color': 'Red'
            },
            
            # Additional Car
            {
                'name': 'Maruti Ertiga',
                'category': Category.objects.get(name='Family'),
                'vehicle_type': 'car',
                'brand': 'Maruti Suzuki',
                'model': 'Ertiga',
                'year': 2023,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'seats': 7,
                'price_per_day': Decimal('2000.00'),
                'price_per_hour': Decimal('200.00'),
                'description': 'Compact MPV perfect for small families with good fuel efficiency.',
                'features': '7 seats, Compact MPV, Good fuel efficiency, Easy to drive',
                'mileage': '20 km/l',
                'color': 'Pearl White'
            }
        ]
        
        for vehicle_data in vehicles:
            vehicle, created = Vehicle.objects.get_or_create(
                name=vehicle_data['name'],
                defaults=vehicle_data
            )
            if created:
                self.stdout.write(f'Created vehicle: {vehicle.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
