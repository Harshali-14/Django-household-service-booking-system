from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Profile , Booking


def login_required_popup(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "⚠️ Please login first to access this page")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    services = Service.objects.all()[:6]
    products = Product.objects.all()[:8]   # add this

    return render(request, 'home.html', {
        'services': services,
        'products': products
    })


def about(request):
    return render(request, 'about.html')

@login_required(login_url='/login/')
def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='/login/')
def services(request):

    services = Service.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        services = services.filter(name__icontains=query)

    if category and category != 'all':
        services = services.filter(category=category)

    return render(request, 'services.html', {
        'services': services
    })


def login_user(request):

    if request.method == "POST":

        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        # try email login
        if User.objects.filter(email=username_or_email).exists():
            username = User.objects.get(email=username_or_email).username
            user = authenticate(request, username=username, password=password)

        # try username login
        else:
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password")
            return redirect('login')

    return render(request, 'login.html')


def register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.save()

        # ✅ SAVE EXTRA DATA (IMPORTANT)
        Profile.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def booking(request, id=None):

    services = Service.objects.all()

    selected_service = None
    calculated_price = 0

    if id:
        selected_service = Service.objects.get(id=id)

    # AUTO PROFILE
    profile, created = Profile.objects.get_or_create(user=request.user)

    # PRICE CALCULATION
    if selected_service:
        calculated_price = selected_service.base_price

    if request.method == "POST":

        service_id = request.POST.get("service")
        service = Service.objects.get(id=service_id)

        quantity = 1  # default

        calculated_price = service.base_price + (quantity * service.price_per_unit)

        Booking.objects.create(
            user=request.user,
            service=service,
            user_name=request.POST.get("full_name"),
            quantity=quantity
        )

    return render(request, "booking.html", {
        "services": services,
        "selected_service": selected_service,
        "calculated_price": calculated_price,
        "user": request.user,
        "profile": profile
    })
    
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
def profile(request):
    user = request.user

    # ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.email = request.POST.get("email")
        user.save()

        profile.phone = request.POST.get("phone")
        profile.save()

    return render(request, "profile.html", {
        "user": user
    })

@login_required(login_url='/login/')
def payment(request):
    return render(request, 'payment.html')

from .models import Product

@login_required(login_url='/login/')
def product(request):
    electrician = Product.objects.filter(category="electrician")
    plumbing = Product.objects.filter(category="plumbing")
    cleaning = Product.objects.filter(category="cleaning")

    return render(request, "products.html", {
        "electrician": electrician,
        "plumbing": plumbing,
        "cleaning": cleaning,
    })