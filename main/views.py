from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Profile , Booking, Provider
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import client
from django.conf import settings
from .models import ContactMessage
from django.utils import timezone
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
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        return redirect('contact')  # reload page after submit

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

from django.utils import timezone

@login_required(login_url='/login/')
def booking(request, id=None):

    services = Service.objects.all()
    selected_service = None
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if id:
        selected_service = Service.objects.get(id=id)

    if request.method == "POST":

        service_id = request.POST.get("service")
        service = Service.objects.get(id=service_id)

        # ✅ ALWAYS CREATE BOOKING FIRST
        booking = Booking.objects.create(
            user=request.user,
            service=service,
            user_name=request.POST.get("full_name"),
            date=request.POST.get("date") or timezone.now().date(),
            quantity=1,
            status="Pending"
        )

        payment_method = request.POST.get("payment_method")

        # COD FLOW
        if payment_method == "cod":
            booking.status = "COD Pending"
            booking.save()
            messages.success(request, "Booking done with COD")
            return redirect("dashboard")

        # Razorpay FLOW
        return redirect("dashboard")  # payment handled separately

    return render(request, "booking.html", {
        "services": services,
        "selected_service": selected_service,
        "user": request.user,
        "profile": profile
    })
                        
@login_required(login_url='/login/')
def dashboard(request):

    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    payments = Payment.objects.filter(user=request.user).order_by('-id')

    total_bookings = bookings.count()

    # ✅ ONLY PRODUCT ORDERS
    product_orders = payments.filter(
        payment_type="product",
        payment_status="paid"
    ).count()

    # ✅ ONLY PAID TOTAL SPENDING
    total_spending = sum(
        p.amount for p in payments if p.payment_status == "paid"
    )

    return render(request, 'dashboard.html', {
        "bookings": bookings,
        "payments": payments,
        "total_bookings": total_bookings,
        "product_orders": product_orders,
        "total_spending": total_spending,
    })

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


@login_required
@csrf_exempt
def create_order(request):

    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid method"}, status=400)

        item_id = request.POST.get("id")
        item_type = request.POST.get("type")

        if not item_id or not item_type:
            return JsonResponse({"error": "Missing data"}, status=400)

        # SERVICE
        if item_type == "service":
            item = Service.objects.filter(id=item_id).first()
            if not item:
                return JsonResponse({"error": "Service not found"}, status=404)

            amount = int(item.base_price) * 100

        # PRODUCT
        elif item_type == "product":
            item = Product.objects.filter(id=item_id).first()
            if not item:
                return JsonResponse({"error": "Product not found"}, status=404)

            amount = int(item.price) * 100

        else:
            return JsonResponse({"error": "Invalid type"}, status=400)

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            user=request.user,
            order_id=order["id"],
            amount=amount / 100,
            payment_status="created",
            payment_type=item_type
        )

        return JsonResponse({
            "order_id": order["id"],
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID,
            "payment_id": payment.id
        })

    except Exception as e:
        print("CREATE ORDER ERROR:", e)
        return JsonResponse({"error": str(e)}, status=500)
                
from .models import Payment
import json

@csrf_exempt
def payment_success(request):

    if request.method == "POST":
        data = json.loads(request.body)

        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")

        try:
            payment = Payment.objects.get(order_id=order_id)

            payment.payment_id = payment_id
            payment.signature = signature
            payment.status = "paid"
            payment.save()

            # ✅ ALSO UPDATE BOOKING (IMPORTANT FIX)
            Booking.objects.filter(user=payment.user).update(status="Paid")

            return JsonResponse({"status": "success"})

        except Payment.DoesNotExist:
            return JsonResponse({"status": "not found"}, status=404)

    return JsonResponse({"error": "invalid method"}, status=400)
@login_required
def provider_dashboard(request):
    try:
        provider = request.user.provider
    except Provider.DoesNotExist:
        provider = None

    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'provider_dashboard.html', {
        'provider': provider,
        'bookings': bookings
    })

def update_booking_status(request, booking_id, status):
    booking = Booking.objects.get(id=booking_id)
    booking.status = status
    booking.save()
    return redirect('provider_dashboard')