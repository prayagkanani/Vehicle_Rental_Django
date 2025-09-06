from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('category/<int:category_id>/', views.category_vehicles, name='category_vehicles'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('add-review/<int:vehicle_id>/', views.add_review, name='add_review'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
