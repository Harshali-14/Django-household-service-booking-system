from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Service, Booking, Provider, Payment, Profile, Product
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html


# =========================
# PROFILE INLINE
# =========================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# =========================
# CUSTOM USER ADMIN
# =========================
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')


# unregister default user admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# =========================
# SERVICE ADMIN
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'base_price')
    search_fields = ('name', 'category')
    list_filter = ('category',)


# =========================
# BOOKING ADMIN
# =========================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'service',
        'status',
        'action_buttons'
    )

    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">✔ Accept</a> '
            '<a class="button" href="{}">❌ Decline</a>',
            reverse('admin:booking-accept', args=[obj.id]),
            reverse('admin:booking-decline', args=[obj.id]),
        )

    action_buttons.short_description = "Actions"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                '<int:booking_id>/accept/',
                self.admin_site.admin_view(self.accept_booking),
                name='booking-accept'
            ),
            path(
                '<int:booking_id>/decline/',
                self.admin_site.admin_view(self.decline_booking),
                name='booking-decline'
            ),
        ]
        return custom_urls + urls

    def accept_booking(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = "Accepted"
        booking.save()
        return redirect(request.META.get('HTTP_REFERER'))

    def decline_booking(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = "Declined"
        booking.save()
        return redirect(request.META.get('HTTP_REFERER'))
# =========================
# PROVIDER ADMIN
# =========================
admin.site.register(Provider)


# =========================
# PAYMENT ADMIN (FIXED + IMPORTANT)
# =========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "order_id",
        "amount",
        "payment_type",   # ✅ booking/product comes from here
        "payment_status",
        "created_at",
    )

    list_filter = (
        "payment_type",
        "payment_status",
    )

    search_fields = (
        "order_id",
        "user__username",
    )


# =========================
# PROFILE ADMIN
# =========================
admin.site.register(Profile)


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag')
    list_filter = ('category', 'tag')
    search_fields = ('name',)
    
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')