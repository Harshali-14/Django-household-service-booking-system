from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Service, Booking, Provider, Payment, Profile, Product


# =========================
# PROFILE INLINE (IMPORTANT)
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
    inlines = (ProfileInline,)  # 👈 phone + address show here

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')


# unregister default user
admin.site.unregister(User)

# register custom user
admin.site.register(User, CustomUserAdmin)


# =========================
# OTHER MODELS
# =========================
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Provider)
admin.site.register(Payment)
admin.site.register(Profile)


# =========================
# PRODUCT ADMIN (CUSTOM)
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag')
    list_filter = ('category', 'tag')
    search_fields = ('name',)