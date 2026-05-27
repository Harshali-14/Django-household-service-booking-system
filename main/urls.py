from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('services/', views.services, name='services'),

    path('login/', views.login_user, name='login'),

    path('register/', views.register, name='register'),
    
    path('logout/', views.logout_user, name='logout'),

    path('booking/<int:id>/', views.booking, name='booking_with_id'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('profile/', views.profile, name='profile'),

    path('payment/', views.payment, name='payment'),
    
    path('product/', views.product, name='product'),
    

]