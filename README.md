# Rental House - Vehicle Rental System

A comprehensive Django-based vehicle rental system with an attractive, modern website design. This system allows users to rent bikes, cars, and travellers with a user-friendly interface and robust backend functionality.

## 🚗 Features

### Core Functionality
- **Vehicle Management**: Support for bikes, cars, and travellers
- **User Authentication**: Registration, login, and profile management
- **Booking System**: Easy vehicle booking with date/time selection
- **Search & Filter**: Advanced vehicle search with multiple criteria
- **Pricing**: Flexible pricing per hour and per 24 hours (in Indian Rupees)
- **Reviews & Ratings**: User feedback system for vehicles

### Website Design
- **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5
- **Attractive Navigation**: Professional navigation bar with "Rental House" branding
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Mobile Responsive**: Optimized for all device sizes
- **Professional Footer**: Comprehensive footer with contact information and links

### Vehicle Types
- **Bikes**: Starting from ₹500/day
- **Cars**: Starting from ₹1500/day  
- **Travellers**: Starting from ₹2500/day

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Poppins)
- **Image Handling**: Pillow for image processing

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vehicle_rental
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### 6. Populate Sample Data (Optional)
```bash
python manage.py populate_db
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## 🏗️ Project Structure

```
vehicle_rental/
├── vehicles/                 # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── myapp/                   # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Form classes
│   ├── admin.py            # Admin interface
│   ├── urls.py             # App URL patterns
│   └── management/         # Custom management commands
├── templates/               # HTML templates
│   └── myapp/
│       ├── base.html       # Base template
│       ├── home.html       # Home page
│       ├── login.html      # Login page
│       ├── register.html   # Registration page
│       ├── vehicle_list.html # Vehicle listing
│       ├── about.html      # About page
│       └── contact.html    # Contact page
├── static/                  # Static files
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   ├── js/
│   │   └── main.js        # Custom JavaScript
│   └── images/            # Image assets
├── media/                  # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt        # Python dependencies

```
<img width="410" height="900" alt="Screenshot 2025-09-08 182523" src="https://github.com/user-attachments/assets/2c8f3298-a6c9-466d-a41e-027276996525" />


## 🎯 Key Features Explained

### User Authentication
- **Registration**: Users can create accounts with personal details
- **Login/Logout**: Secure authentication system
- **Profile Management**: Users can update their information

### Vehicle Management
- **Categories**: Economy, Premium, and Family vehicle categories
- **Detailed Information**: Comprehensive vehicle specifications
- **Pricing**: Transparent pricing in Indian Rupees
- **Availability Status**: Real-time availability tracking

### Booking System
- **Flexible Duration**: Hourly and daily booking options
- **Location Selection**: Pickup and return location specification
- **Price Calculation**: Automatic total amount calculation
- **Booking Management**: View, cancel, and track bookings

### Search & Filter
- **Vehicle Type**: Filter by bikes, cars, or travellers
- **Brand Search**: Search by vehicle brand
- **Price Range**: Filter by minimum and maximum price
- **Seating Capacity**: Filter by number of seats

## 🎨 Design Features

### Modern UI Elements
- **Gradient Backgrounds**: Beautiful color schemes
- **Card-based Layout**: Clean, organized information display
- **Hover Effects**: Interactive elements with smooth animations
- **Responsive Grid**: Bootstrap-based responsive design

### Navigation & Footer
- **Professional Branding**: "Rental House" navigation header
- **Comprehensive Footer**: Contact info, quick links, and social media
- **Mobile-friendly**: Responsive navigation for all devices

### Interactive Components
- **Animated Statistics**: Dynamic counters and hover effects
- **Form Validation**: Real-time form validation and feedback
- **Smooth Transitions**: CSS animations and JavaScript interactions

## 🔧 Customization

### Adding New Vehicle Types
1. Update the `VEHICLE_TYPES` choices in `models.py`
2. Add corresponding icons and styling
3. Update the admin interface

### Modifying Pricing
1. Update price fields in the Vehicle model
2. Modify the pricing display in templates
3. Update the booking calculation logic

### Styling Changes
1. Modify `static/css/style.css` for custom styles
2. Update `static/js/main.js` for JavaScript functionality
3. Customize Bootstrap classes in templates

## 📱 Mobile Responsiveness

The website is fully responsive and optimized for:
- **Mobile Phones**: Portrait and landscape orientations
- **Tablets**: Various screen sizes and resolutions
- **Desktop**: All modern browsers and screen sizes

## 🚀 Deployment

### Production Settings
1. Update `DEBUG = False` in `settings.py`
2. Configure production database (PostgreSQL/MySQL)
3. Set up static file serving
4. Configure environment variables

### Recommended Hosting
- **Heroku**: Easy Django deployment
- **DigitalOcean**: VPS hosting with full control
- **AWS**: Scalable cloud hosting
- **Vercel**: Modern deployment platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- Google Fonts for the typography

---

**Rental House** - Your trusted partner for vehicle rentals! 🚗🏍️🚐
