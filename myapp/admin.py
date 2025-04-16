from django.contrib import admin
from django.urls import path
from .models import Booking

# Register your models here.
from .models import Product, Category

# admin.site.register(Product)
# admin.site.register(Category)
from .models import PaymentTransaction

from .models import (
    CustomUser, Category, Product, TourCategory, TourPackage, 
    Destination, Booking, PaymentTransaction, Review, ContactMessage, Ticket,
)

# CustomUser Admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_type', 'email_verified', 'is_staff')
    list_filter = ('user_type', 'email_verified', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# TourCategory Admin
@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon')
    search_fields = ('name',)

# TourPackage Admin
@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'price', 'available_seats', 'start_date', 'end_date', 'is_active')
    list_filter = ('destination', 'categories', 'is_active')
    search_fields = ('title', 'destination')
    filter_horizontal = ('categories',)

# Destination Admin
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Booking Admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour_package', 'booking_date', 'start_date', 'end_date', 'travelers', 'total_price', 'status',"id")
    list_filter = ('status', 'tour_package', 'user')
    actions = ["confirm_selected_bookings"]
    search_fields = ('user__email', 'tour_package__title')
    def confirm_selected_bookings(self, request, queryset):
        queryset.update(status="confirmed")
    confirm_selected_bookings.short_description = "Confirm selected bookings"
if not admin.site.is_registered(Booking):
    admin.site.register(Booking, BookingAdmin)
    def tour_package_title(self, obj):
        return obj.tour_package.title 
    tour_package_title.short_description = 'Tour Package'
# Payment Admin
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('booking', 'amount', 'payment_method', 'transaction_id', 'payment_date', 'status')
#     list_filter = ('status', 'payment_method')
#     search_fields = ('booking__id', 'transaction_id')

from django.contrib import admin
from .models import Ticket, PaymentTransaction
from django.utils.html import format_html

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'get_booking_user', 'get_issued_date', 'get_barcode')
    list_filter = (
        'booking__user',
        'issued_date',
    )
    search_fields = (
        'ticket_number',
        'booking__user__username',
        'booking__tour_package__name'
    )
    readonly_fields = ('ticket_number', 'barcode_data')
    
    def get_booking_user(self, obj):
        return obj.booking.user.get_full_name() or obj.booking.user.username
    get_booking_user.short_description = 'User'
    get_booking_user.admin_order_field = 'booking__user'
    
    def get_issued_date(self, obj):
        return obj.issued_date.strftime("%Y-%m-%d %H:%M")
    get_issued_date.short_description = 'Issued Date'
    get_issued_date.admin_order_field = 'issued_date'
    
    def get_barcode(self, obj):
        return format_html('<code>{}</code>', obj.barcode_data[:50] + '...' if len(obj.barcode_data) > 50 else obj.barcode_data)
    get_barcode.short_description = 'Barcode Data'

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'get_user',
        'amount',
        'get_payment_method',
        'get_status',
        'get_created_at'
    )
    list_filter = (
        'status',
        'payment_method',
        'created_at',
    )
    search_fields = (
        'transaction_id',
        'user__username',
        'user__email'
    )
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    list_select_related = ('user',)
    
    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'
    
    def get_payment_method(self, obj):
        return obj.get_payment_method_display()
    get_payment_method.short_description = 'Payment Method'
    
    def get_status(self, obj):
        status_colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'blue'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            status_colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    get_status.short_description = 'Status'
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")
    get_created_at.short_description = 'Created At'
    get_created_at.admin_order_field = 'created_at'
# admin.site.register(Payment, PaymentAdmin)


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at', 'approved')
    list_filter = ('rating', 'approved')
    search_fields = ('user__email', 'tour__title')

# ContactMessage Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at','message')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

