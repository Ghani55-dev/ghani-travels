from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import random
import string
import uuid
import qrcode
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.core.files.storage import default_storage

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """Custom user manager to use email instead of username"""

    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('C', 'Customer'),
        ('A', 'Agent'),
        ('AD', 'Admin'),
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(_('user type'), max_length=2, choices=USER_TYPE_CHOICES, default='C')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(_('phone number'), max_length=20, default="0000000000")
    profile_picture = models.ImageField(_('profile picture'), upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    email_verified = models.BooleanField(_('email verified'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # ✅ USE EMAIL AS THE USERNAME
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']  # ✅ ADD REQUIRED FIELDS

    objects = CustomUserManager()  # ✅ ADD CUSTOM USER MANAGER

    def __str__(self):
        return self.email

    # Custom related names for auth system
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="custom_users",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="custom_users",
        related_query_name="custom_user",
    )
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s Profile"
# Category for Products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

# Tour Category
class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)

# Tour Package Model
class TourPackage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(TourCategory)
    featured_image = models.ImageField(upload_to='tours/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} - ₹{self.price}"

# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    version = models.PositiveIntegerField(default=1)
    last_updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='bookings')
    tour_package = models.ForeignKey('TourPackage', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    passengers = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    travelers = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    special_requests = models.TextField(blank=True)
    
    def generate_ticket_number(self):
        """Generate a random 8-digit alphanumeric ticket number"""
        while True:
            # Generate random characters (uppercase letters + digits)
            chars = string.ascii_uppercase + string.digits
            ticket_number = 'GH-' + ''.join(random.choices(chars, k=8))
            if not Booking.objects.filter(ticket_number=ticket_number).exists():
                return ticket_number
    
    def save(self, *args, **kwargs):
        if not self.ticket_number and self.status == 'confirmed':  # Only generate for confirmed bookings
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)

    
    def save(self, *args, **kwargs):
        if not self.id:  # Only generate ID for new bookings
            # Generate random 8-digit booking ID
            while True:
                booking_id = ''.join(random.choice(string.digits) for _ in range(8))
                if not Booking.objects.filter(id=booking_id).exists():
                    self.id = booking_id
                    break
        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     # Auto-increment version on updates
    #     if self.pk:
    #         self.version += 1
    #     super().save(*args, **kwargs)
    
    @property
    def is_confirmed(self):
        return self.status == 'confirmed'
    def __str__(self):
        return f"Booking {self.id} (UID: {self.uid}) - {self.user.username} ({self.status})"




# Review Model
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

# Contact Message Model (Added)
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

#------------------------------------------------------------------------------------------------------------  

# Payment Model



class PaymentTransaction(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('phonepay', 'PhonePe'),
        ('gpay', 'Google Pay'),
        ('paytm', 'Paytm'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"PYMT-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def process_refund(self):
        """Initiate refund process for this transaction"""
        if self.status != 'completed':
            return False
        
        # Implement your refund logic here
        try:
            # Example: Process refund through payment gateway
            # refund_result = payment_gateway.refund(self.transaction_id, self.amount)
            # if refund_result.success:
            self.status = 'refunded'
            self.save()
            return True
        except Exception as e:
            return False


class Ticket(models.Model):
    """Represents a ticket issued for a booking."""
    TICKET_TYPES = [
        ('general', 'General'),
        ('vip', 'VIP'),
        ('premium', 'Premium'),
    ]
    
    TICKET_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    booking = models.OneToOneField(
        "Booking",
        on_delete=models.CASCADE,
        related_name="ticket"
    )
    ticket_type = models.CharField(
        max_length=20,
        choices=TICKET_TYPES,
        default='general'
    )
    ticket_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS,
        default='confirmed'
    )
    issued_date = models.DateTimeField(default=now)
    barcode_data = models.CharField(
        max_length=255,
        blank=True,
        editable=False
    )
    qr_code = models.ImageField(
        upload_to='tickets/qr_codes/',
        blank=True,
        null=True,
        editable=False
    )
    payment_transaction = models.OneToOneField(
        PaymentTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ticket'
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-issued_date']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['booking', 'issued_date']),
        ]

    def __str__(self):
        return f"Ticket #{self.ticket_number} ({self.get_ticket_type_display()})"

    def save(self, *args, **kwargs):
        # Generate ticket number if not exists
        if not self.ticket_number:
            prefix = "TKT"
            booking_id = str(self.booking.id).zfill(6)
            user_id = str(self.booking.user.id).zfill(4)
            package_id = str(self.booking.tour_package.id).zfill(4)
            unique_id = uuid.uuid4().hex[:6].upper()
            self.ticket_number = f"{prefix}-{booking_id}{user_id}{package_id}-{unique_id}"

        # Generate barcode data if not exists
        if not self.barcode_data:
            self.barcode_data = (
                f"{self.booking.id}-{self.booking.user.id}-"
                f"{self.booking.tour_package.id}-{self.ticket_number}"
            )

        # Generate QR code if not exists
        if not self.qr_code and self.barcode_data:
            self._generate_qr_code()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to clean up QR code file"""
        if self.qr_code:
            default_storage.delete(self.qr_code.path)
        super().delete(*args, **kwargs)

    def _generate_qr_code(self):
        """Generate QR code image for the ticket"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.barcode_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            filename = f"qr_{self.ticket_number}.png"
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        except Exception as e:
            # Log error but don't fail ticket creation
            pass

    @property
    def is_active(self):
        return self.status == 'confirmed'

    @property
    def user(self):
        """Shortcut to access user through booking"""
        return self.booking.user

    def mark_as_cancelled(self, refund=False):
        """Cancel ticket with optional refund"""
        self.status = 'refunded' if refund else 'cancelled'
        self.save(update_fields=['status'])
        
        if refund and self.payment_transaction:
            return self.payment_transaction.process_refund()
        return True

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ticket_detail', kwargs={'ticket_number': self.ticket_number})

    def generate_pdf(self):
        """Generate PDF ticket (to be implemented)"""
        pass