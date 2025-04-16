from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.utils import timezone
import stripe
import logging
import json
import uuid
import datetime
import random
from django.conf import settings
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import PaymentTransaction, Ticket
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login
from myapp.forms import LoginForm 
from .forms import BookingForm
from .models import Booking, TourPackage, ContactMessage, CustomUser
from .forms import CustomUserCreationForm 
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
import openai  # Assuming you're using OpenAI's GPT API or another AI service
from .models import Booking
from django.contrib.auth.views import LoginView
from .models import TourPackage, Booking, Review, ContactMessage
from .forms import CustomUserCreationForm, BookingForm, ReviewForm
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login, logout
from .models import CustomUser
from django.contrib.auth import get_user_model, authenticate

from django.db import transaction
from .models import PaymentTransaction, Ticket, Booking

User = get_user_model()

logger = logging.getLogger(__name__)
#------------------------------------------------------------------------------------------------------------
def home(request):
    return render(request, 'home.html')
def main_page(request):
    return render(request, 'mainpage.html') 
def register(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html') 

# def booking(request):
#     return render(request, 'registration/booking.html') 
#------------------------------------------------------------------------------------------------------------
def service(request):
    services = [
        {"name": "Flight Booking", "description": "Book your flights with ease."},
        {"name": "Hotel Reservation", "description": "Find the best hotels for your stay."},
        {"name": "Tour Packages", "description": "Explore our curated tour packages."},
    ]
    return render(request, 'registration/service.html', {'services': services})
#------------------------------------------------------------------------------------------------------------
def about(request):
    about_info = {
        "company_name": "Ghani Travels",
        "mission": "To provide the best travel experiences.",
        "team": [
            {"name": "Ganagani Ganesh", "role": "CEO"},
            {"name": "Prashant", "role": "Travel Consultant"},
        ],
    }
    return render(request, 'registration/about.html', {'about_info': about_info})
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
def tours(request):
    tours = TourPackage.objects.all()
    return render(request, 'registration/tours.html', {'tours': tours})

#------------------------------------------------------------------------------------------------------------
# Tour Detail View
@login_required
class TourDetailView(DetailView):
    model = TourPackage
    template_name = 'registration/package_detail.html'
    context_object_name = 'tours'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        return context
#------------------------------------------------------------------------------------------------------------
@login_required
def package_detail(request, package_id):
    # Fetch the current package
    package = get_object_or_404(TourPackage, id=package_id)
    
    # Fetch other packages (exclude the current package)
    other_packages = TourPackage.objects.exclude(id=package_id).order_by('?')[:5]  # Random 5 packages
    
    # Fetch reviews for the current package
    reviews = Review.objects.filter(tour=package)
    
    context = {
        'package': package,
        'reviews': reviews,
        'other_packages': other_packages,
    }
    
    return render(request, 'registration/package_detail.html', context)
#------------------------------------------------------------------------------------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Log in the new user
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            
            user = CustomUser.objects.create_user(email=email, password=raw_password)
            user = authenticate(request, email=email, password=raw_password)  # Use email for authentication

            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, "Registration successful! You are now logged in.")
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Failed to log in after registration. Please try logging in manually.")
                return redirect('login')
        else:
            # If form is invalid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/successpage.html')
#------------------------------------------------------------------------------------------------------------
class RegisterUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('registration_success')
#------------------------------------------------------------------------------------------------------------

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        return super().form_valid(form)
#------------------------------------------------------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"Trying to authenticate user: {email}")

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                print(f"User authenticated: {user}") 
                login(request, user)
                return redirect('dashboard')
            else:
                print("Authentication failed")
                messages.error(request, 'Invalid credentials, please try again.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(f"🔍 Trying to authenticate: {email}")  # Debugging
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            print("✅ User authenticated and logged in!")  # Debugging
            return redirect("dashboard")  # Redirect to dashboard
        else:
            print("❌ Authentication failed!")  # Debugging
            messages.error(request, "Invalid email or password.")
            return render(request, "registration/login.html", {"error": "Invalid email or password."})

    return render(request, "registration/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
#------------------------------------------------------------------------------------------------------------
@login_required
def book_package(request):
    package = (TourPackage)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            selected_package = booking.tour_package
            booking.total_price = selected_package.price * booking.passengers
            booking.save()
            print(f"Booking ID: {booking.id}, Booking: {booking.tour_package.title}, Price per seat: {booking.tour_package.price}, Passengers: {booking.passengers}, Total: {booking.total_price}")

            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'registration/book_package.html', {'form': form, 'package': package})

#------------------------------------------------------------------------------------------------------------
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

from .models import Booking

def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Update booking status to confirmed
        booking.status = 'confirmed'
        booking.save()

        # Generate ticket number if not exists
        if not booking.ticket_number:
            booking.ticket_number = booking.generate_ticket_number()
            booking.save()

        # Send confirmation email to the booking user
        send_booking_confirmation(booking)

        messages.success(request, "Booking confirmed! A confirmation has been sent to your email.")
        return redirect('booking_detail', booking_id=booking.id)

    return render(request, 'emails/confirm_booking.html', {'booking': booking})

def send_booking_confirmation(booking):
    # Get the user's email who made the booking
    recipient_email = booking.user.email

    subject = f"Ghani Travels Booking Confirmation - {booking.ticket_number}"

    context = {
        'booking': booking,
        'user': booking.user,
        'package': booking.tour_package,
    }

    html_message = render_to_string('emails/booking_confirmation.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # This is the sender (your company email)
            recipient_list=[booking.user.email],         # This is the recipient (user's email)
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {str(e)}")

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'registration/booking_confirmation.html', {'booking': booking})

def redirect_to_ticket(request, booking_id):                                    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'confirmed'
    booking.save()

    # Force refresh with new version
    return redirect(reverse('ticket', kwargs={'booking_id': booking.id}) + f'?v={booking.version}')

#------------------------------------------------------------------------------------------------------------
@login_required
def add_review(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = package
            review.save()
            return redirect('package_detail', package_id=package.id)
    else:
        form = ReviewForm()
    
    return render(request, 'registration/add_review.html', {
        'form': form,
        'package': package
    })
#------------------------------------------------------------------------------------------------------------
def create_checkout_session(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'INR',
                    'product_data': {'name': package.title},
                    'unit_amount': int(package.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        logger.error(f"Stripe Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
#------------------------------------------------------------------------------------------------------------
# Error handlers
def handler404(request, exception):
    logger.error(f"404 Error: {exception}")
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    logger.critical("500 Server Error")
    return render(request, 'errors/500.html', status=500)

#------------------------------------------------------------------------------------------------------------       
# Set OpenAI API key
# Initialize OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
@method_decorator(csrf_exempt, name='dispatch')  # Add CSRF exemption
@method_decorator(login_required, name='dispatch')
class AIChatView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            user_input = data.get('message')

            if not user_input:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Log the user input
            logger.info(f"User input: {user_input}")

            # Send the user input to the OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use the desired model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=150,
            )

            # Log the OpenAI API response
            logger.info(f"OpenAI API Response: {response}")

            # Extract the AI's response
            ai_response = response.choices[0].message.content.strip()
            return JsonResponse({'response': ai_response})

        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except openai.RateLimitError:
            logger.error("OpenAI API quota exceeded")
            return JsonResponse({'error': 'You have exceeded your OpenAI API quota.'}, status=429)
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return JsonResponse({'error': f'OpenAI API error: {str(e)}'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
        except openai.RateLimitError:
            logger.error("OpenAI API quota exceeded")
            return JsonResponse({'response': 'Sorry, I am currently unable to respond due to quota limits. Please try again later.'})
@login_required
def chat_interface(request):
    """
    Render the chat interface.
    """
    return render(request, 'registration/chat_interface.html')

#------------------------------------------------------------------------------------------------------------       

@login_required
def dashboard(request):
    # Get the currently logged-in user
    user = request.user

    # Fetch user-specific data
    user_bookings = Booking.objects.filter(user=user).select_related('tour_package')
    tour_packages = TourPackage.objects.all()
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    bookings = Booking.objects.filter(user=request.user)

    context = {
        "user": user,  # Pass the logged-in user to the template
        "bookings": user_bookings,
        "tour_packages": tour_packages,
        "recent_messages": recent_messages,
        'total_bookings': bookings.count(),
        'confirmed_bookings': bookings.filter(status='confirmed').count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'cancelled_bookings': bookings.filter(status='cancelled').count(),
    }

    return render(request, "registration/dashboard.html", context)
#--------------------------------------------------------------------------------------------------------
import string
from uuid import UUID
def generate_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Generate a random ticket number if one doesn't exist
    if not booking.ticket_number:  # assuming your model has a ticket_number field
        # Create an 8-character alphanumeric ticket number (adjust as needed)
        ticket_length = 8
        characters = string.ascii_uppercase + string.digits
        ticket_number = 'GH-' + ''.join(random.choice(characters) for _ in range(ticket_length))
        
        # Save the ticket number to the booking
        booking.ticket_number = ticket_number
        booking.save()
    
    return render(request, 'registration/ticket.html', {'booking': booking})

logger = logging.getLogger(__name__)

def is_valid_uuid(uuid_to_test, version=4):
    try:
        UUID(uuid_to_test, version=version)
        return True
    except ValueError:
        return False


def view_ticket(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id', '').strip()
        
        try:
            # Try both ID and UID fields
            booking = (Booking.objects.filter(id=booking_id).first() or 
                      Booking.objects.filter(uid=booking_id).first())
            
            if not booking:
                messages.error(request, "Invalid booking ID")
                return render(request, 'registration/lookup_form.html')
            
            # Ensure ticket number exists for confirmed bookings
            if booking.status == 'confirmed' and not booking.ticket_number:
                booking.ticket_number = booking.generate_ticket_number()
                booking.save()
            
            return render(request, 'registration/ticket.html', {'booking': booking})
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            messages.error(request, "Error retrieving booking")
    
    return render(request, 'registration/lookup_form.html')
#------------------------------------------------------------------------------------------------------------
# Set your Stripe secret key
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # Your secret key

##########################################################################
# Payment Processing Helper: PaymentProcessor
##########################################################################
class PaymentProcessor:
    """Handles payment processing logic using Stripe."""
    
    @staticmethod
    def create_payment_intent(amount, currency, user, ticket_type):
        try:
            # Validate amount: convert to paise
            amount_in_paise = int(amount * 100)
            if amount_in_paise < 100:  # Ensure at least ₹1
                raise ValueError("Amount must be at least ₹1")

            # Get or create a Stripe customer
            customer_id = PaymentProcessor.get_or_create_customer(user)
            if not customer_id:
                raise Exception("Could not create payment customer")

            # Create a payment intent on Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency=currency,
                customer=customer_id,
                payment_method_types=['card'],
                metadata={
                    'user_id': user.id,
                    'ticket_type': ticket_type,
                    'email': user.email
                },
                description=f"Ticket purchase for {ticket_type}"
            )
            
            logger.info(f"Created payment intent {intent.id} for user {user.id}")
            return intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API error: {str(e)}", exc_info=True)
            raise Exception("Payment processing error. Please try again.")
        except Exception as e:
            logger.error(f"Payment processing error: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_or_create_customer(user):
        try:
            customers = stripe.Customer.list(email=user.email, limit=1)
            if customers.data:
                return customers.data[0].id
            
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}".strip(),
                metadata={'user_id': user.id}
            )
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe customer error: {str(e)}", exc_info=True)
            return None

##########################################################################
# PaymentView: Renders Payment Selection & Handles Card Payment Processing
##########################################################################
@method_decorator(login_required, name='dispatch')
class PaymentView(View):
    def get(self, request):
        try:
            # Retrieve ticket details from session; defaults if not provided
            ticket_type = request.session.get('ticket_type', 'general')
            amount = settings.TICKET_PRICES.get(ticket_type, 500)
            
            context = {
                'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,  # use public key here
                'ticket_type': ticket_type,
                'amount': amount,
                'payment_methods': PaymentTransaction.PAYMENT_METHODS,
                'selected_method': request.session.get('payment_method')
            }
            return render(request, 'registration/payment.html', context)
            
        except Exception as e:
            logger.error(f"Payment GET error: {str(e)}", exc_info=True)
            messages.error(request, "Error loading payment page")
            return redirect('dashboard')

    @transaction.atomic
    def post(self, request):
        try:
            payment_method = request.POST.get('payment_method')
            if not payment_method:
                raise ValueError("Please select a payment method")
            if payment_method not in dict(PaymentTransaction.PAYMENT_METHODS):
                raise ValueError("Invalid payment method selected")

            ticket_type = request.session.get('ticket_type', 'general')
            amount = settings.TICKET_PRICES.get(ticket_type, 500)
            
            # Store payment details in session
            request.session['payment_data'] = {
                'ticket_type': ticket_type,
                'amount': amount,
                'payment_method': payment_method,
                'created_at': str(timezone.now())
            }
            
            if payment_method == 'card':
                # Create a Stripe PaymentIntent for card payments
                payment_intent = PaymentProcessor.create_payment_intent(
                    amount=amount,
                    currency='inr',
                    user=request.user,
                    ticket_type=ticket_type
                )
                request.session['payment_intent_id'] = payment_intent.id
                return render(request, 'registration/payment.html', {
                    'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
                    'client_secret': payment_intent.client_secret,
                    'ticket_type': ticket_type,
                    'amount': amount,
                    'payment_methods': PaymentTransaction.PAYMENT_METHODS,
                    'selected_method': payment_method
                })
            else:
                # Handle other payment methods (e.g., UPI)
                return redirect('upi_payment')
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('payment_page')
        except Exception as e:
            logger.error(f"Payment POST error: {str(e)}", exc_info=True)
            messages.error(request, "Error processing payment")
            return redirect('payment_page')

##########################################################################
# UpiPaymentView: Handle UPI Payment Processing
##########################################################################
@method_decorator(login_required, name='dispatch')
class UpiPaymentView(View):
    def get(self, request):
        try:
            payment_data = request.session.get('payment_data')
            if not payment_data:
                messages.error(request, "Session expired. Please start over.")
                return redirect('payment_page')
                
            if 'transaction_id' not in payment_data:
                payment_data['transaction_id'] = f"UPI-{uuid.uuid4().hex[:8].upper()}"
                request.session['payment_data'] = payment_data
                request.session.modified = True
            
            context = {
                'amount': payment_data['amount'],
                'ticket_type': payment_data['ticket_type'],
                'transaction_id': payment_data['transaction_id'],
                'payment_method': payment_data['payment_method'],
                'merchant_upi': settings.UPI_ID,
                'merchant_name': settings.MERCHANT_NAME,
                'issued_date': timezone.now()
            }
            return render(request, 'registration/upi_payment.html', context)
        except Exception as e:
            logger.error(f"UPI GET error: {str(e)}", exc_info=True)
            messages.error(request, "Error loading payment page")
            return redirect('payment_page')

    @transaction.atomic
    def post(self, request):
        try:
            payment_data = request.session.get('payment_data')
            if not payment_data:
                raise ValueError("Session expired. Please start over.")
            
            upi_reference = request.POST.get('upi_reference', '').strip()
            if not upi_reference:
                raise ValueError("Please enter UPI transaction reference")
            
            # Retrieve pending booking from session data
            try:
                booking = Booking.objects.get(id=request.session.get('booking_id'), user=request.user)
            except Booking.DoesNotExist:
                messages.error(request, "Invalid booking reference")
                return redirect('payment_page')
            
            # Create a completed payment transaction
            transaction_obj = PaymentTransaction.objects.create(
                user=request.user,
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method'],
                transaction_id=payment_data['transaction_id'],
                status='completed',
                raw_response={'upi_reference': upi_reference, 'verified': False}
            )
            
            # Create ticket and link the transaction
            ticket = Ticket.objects.create(
                booking=booking,
                ticket_type=payment_data.get('ticket_type', 'general'),
                status='confirmed',
                payment_transaction=transaction_obj
            )
            
            # Send confirmation email
            self._send_confirmation(request.user, ticket, transaction_obj)
            self._clear_session(request)
            
            return redirect(reverse('payment_success') + f'?ticket_id={ticket.id}')
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('upi_payment')
        except Exception as e:
            logger.error(f"UPI POST error: {str(e)}", exc_info=True)
            messages.error(request, "Error processing payment. Please contact support.")
            return redirect('payment_failed')

    def _send_confirmation(self, user, ticket, transaction_obj):
        try:
            send_mail(
                subject=f'Ticket Confirmation - {ticket.ticket_number}',
                message=self._get_confirmation_message(user, ticket, transaction_obj),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
        except Exception as e:
            logger.error(f"Confirmation email error: {str(e)}")

    def _get_confirmation_message(self, user, ticket, transaction_obj):
        return f"""Dear {user.get_full_name()},

Your ticket has been successfully booked!

Ticket Details:
- Ticket Number: {ticket.ticket_number}
- Ticket Type: {ticket.get_ticket_type_display()}
- Status: {ticket.get_status_display()}

Payment Details:
- Amount: ₹{transaction_obj.amount:.2f}
- Payment Method: {transaction_obj.get_payment_method_display()}
- Transaction ID: {transaction_obj.transaction_id}

Thank you for your purchase!

Best regards,
{settings.SITE_NAME} Team"""

    def _clear_session(self, request):
        for key in ['payment_data', 'payment_intent_id', 'booking_id']:
            if key in request.session:
                del request.session[key]
        request.session.modified = True

##########################################################################
# ProcessPaymentView: Process Payment via AJAX (for Card/Other flows)
##########################################################################
@method_decorator(login_required, name='dispatch')
class ProcessPaymentView(View):
    @transaction.atomic
    def post(self, request):
        try:
            payment_data = request.session.get('payment_data', {})
            if not payment_data:
                logger.warning("Payment data missing from session")
                return JsonResponse({
                    'error': 'Session expired',
                    'message': 'Please restart your payment process'
                }, status=400)
            
            # Try to update an existing pending booking if available
            try:
                booking = Booking.objects.filter(user=request.user, status='pending').latest('booking_date')
                booking.status = 'confirmed'
                booking.save()
            except Booking.DoesNotExist:
                # Create booking if not available; ensure required fields are present in payment data
                required_fields = ['start_date', 'end_date', 'tour_package_id']
                for field in required_fields:
                    if field not in payment_data:
                        raise ValueError(f"Missing required booking field: {field}")

                booking = Booking.objects.create(
                    user=request.user,
                    tour_package_id=payment_data['tour_package_id'],
                    start_date=datetime.strptime(payment_data['start_date'], '%Y-%m-%d').date(),
                    end_date=datetime.strptime(payment_data['end_date'], '%Y-%m-%d').date(),
                    total_price=payment_data['amount'],
                    status='confirmed',
                    booking_date=timezone.now().date(),
                    passengers=payment_data.get('passengers', 1),
                    special_requests=payment_data.get('special_requests', '')
                )
                logger.info(f"Created new booking {booking.id} for user {request.user.id}")

            transaction_id = f"{payment_data['payment_method'].upper()}-{uuid.uuid4().hex[:8]}"
            transaction_obj = PaymentTransaction.objects.create(
                user=request.user,
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method'],
                transaction_id=transaction_id,
                status='completed',
                raw_response={
                    'user_id': request.user.id,
                    'booking_id': booking.id,
                    'tour_package_id': booking.tour_package_id,
                    'ticket_type': payment_data.get('ticket_type', 'general')
                }
            )
            
            ticket = Ticket.objects.create(
                booking=booking,
                ticket_type=payment_data.get('ticket_type', 'general'),
                status='confirmed',
                payment_transaction=transaction_obj
            )
            logger.info(f"Created ticket {ticket.ticket_number} for booking {booking.id}")
            
            email_sent = self._send_confirmation_email(request.user, transaction_obj, ticket, booking)
            self._clear_payment_session(request)
            
            return JsonResponse({
                'status': 'success',
                'ticket_id': ticket.id,
                'booking_id': booking.id,
                'transaction_id': transaction_obj.transaction_id,
                'redirect_url': reverse('payment_success') + f'?ticket_id={ticket.id}',
                'email_sent': email_sent
            })
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return JsonResponse({
                'error': 'validation_error',
                'message': str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"Payment processing failed: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': 'payment_processing_error',
                'message': 'We encountered an error processing your payment',
                'details': str(e)
            }, status=400)

    def _send_confirmation_email(self, user, transaction_obj, ticket, booking):
        try:
            send_mail(
                subject=f'Booking Confirmation #{ticket.ticket_number}',
                message=self._get_confirmation_message(user, transaction_obj, ticket, booking),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
            return False

    def _get_confirmation_message(self, user, transaction_obj, ticket, booking):
        tour_package_name = 'N/A'
        if hasattr(booking, 'tour_package') and booking.tour_package:
            tour_package_name = booking.tour_package.name

        start_date = booking.start_date.strftime('%d %b %Y') if booking.start_date else 'N/A'
        end_date = booking.end_date.strftime('%d %b %Y') if booking.end_date else 'N/A'
        
        return f"""Dear {user.get_full_name()},

Thank you for your booking! Here are your details:

Booking Summary:
- Booking ID: {getattr(booking, 'uid', booking.id)}
- Ticket Number: {ticket.ticket_number}
- Ticket Type: {ticket.get_ticket_type_display()}
- Status: {ticket.get_status_display()}
- Tour Package: {tour_package_name}
- Travel Dates: {start_date} to {end_date}

Payment Details:
- Amount Paid: ₹{transaction_obj.amount:.2f}
- Payment Method: {transaction_obj.get_payment_method_display()}
- Transaction ID: {transaction_obj.transaction_id}
- Date: {transaction_obj.created_at.strftime('%d %b %Y %I:%M %p')}

If you have any questions, please contact our support team.

Best regards,
{settings.SITE_NAME} Team"""

    def _clear_payment_session(self, request):
        for key in ['payment_data', 'payment_intent_id', 'booking_id']:
            if key in request.session:
                del request.session[key]
        request.session.modified = True

##########################################################################
# Stripe Webhook Handling
##########################################################################
@csrf_exempt
def stripe_webhook(request):
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                _handle_successful_payment(payment_intent)
                
            return HttpResponse(status=200)
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}", exc_info=True)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}", exc_info=True)
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}", exc_info=True)
            return HttpResponse(status=500)
    return HttpResponse(status=405)

def _handle_successful_payment(payment_intent):
    try:
        if PaymentTransaction.objects.filter(transaction_id=payment_intent.id).exists():
            return
        
        user_id = payment_intent.metadata.get('user_id')
        if not user_id:
            logger.error("No user_id in payment intent metadata")
            return
        
        transaction_obj = PaymentTransaction.objects.create(
            user_id=user_id,
            amount=payment_intent.amount / 100,
            payment_method='card',
            transaction_id=payment_intent.id,
            status='completed',
            raw_response=payment_intent
        )
        
        pending_booking = Booking.objects.filter(user_id=user_id, status='pending').first()
        if pending_booking:
            Ticket.objects.create(
                booking=pending_booking,
                payment_transaction=transaction_obj,
                ticket_type=payment_intent.metadata.get('ticket_type', 'general'),
                status='confirmed'
            )
        
        logger.info(f"Processed successful payment {payment_intent.id}")
    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}", exc_info=True)

##########################################################################
# Payment Success / Failed Views
##########################################################################
@login_required
def payment_success(request):
    try:
        ticket_id = request.GET.get('ticket_id')
        if not ticket_id:
            return redirect('payment_failed')
        ticket = Ticket.objects.get(id=ticket_id, booking__user=request.user)
        return render(request, 'registration/payment_success.html', {
            'ticket': ticket,
            'transaction': ticket.payment_transaction
        })
    except Ticket.DoesNotExist:
        logger.error(f"Ticket not found: {ticket_id}")
        return redirect('payment_failed')
    except Exception as e:
        logger.error(f"Success page error: {str(e)}", exc_info=True)
        return redirect('payment_failed')

@login_required
def payment_failed(request):
    return render(request, 'registration/payment_failed.html')

##########################################################################
# CreateBookingView: Create a Pending Booking Prior to Payment
##########################################################################
@method_decorator(login_required, name='dispatch')
class CreateBookingView(View):
    def post(self, request):
        try:
            tour_package_id = request.POST.get('tour_package_id')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            ticket_type = request.POST.get('ticket_type')
            if not all([tour_package_id, start_date, end_date, ticket_type]):
                raise ValueError("Missing required booking information")

            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            amount = settings.TICKET_PRICES.get(ticket_type, 500)
            
            request.session['payment_data'] = {
                'amount': amount,
                'ticket_type': ticket_type,
                'tour_package_id': tour_package_id,
                'start_date': start_date_obj.isoformat(),
                'end_date': end_date_obj.isoformat(),
                'passengers': request.POST.get('passengers'),
                'special_requests': request.POST.get('special_requests')
            }
            
            booking = Booking.objects.create(
                user=request.user,
                tour_package_id=tour_package_id,
                start_date=start_date_obj,
                end_date=end_date_obj,
                total_price=amount,
                status='pending',
                booking_date=timezone.now().date()
            )
            
            request.session['booking_id'] = booking.id
            return redirect('payment_page')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('create_booking')
        except Exception as e:
            logger.error(f"Booking creation error: {str(e)}", exc_info=True)
            messages.error(request, "Error creating booking")
            return redirect('tour_packages')

#-----------------------------------------------------------------------------------------------------------

@login_required
def user_tickets(request):
    user = request.user  # Get the logged-in user
    tickets = Ticket.objects.filter(user=user)  # Show only this user's tickets
    
    return render(request, "tickets.html", {"tickets": tickets})

#-----------------------------------------------------------------------------------------------------------
def contact(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')  # Fetch all messages
    return render(request, 'registration/contact.html', {'messages_list': messages_list})

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Send email (optional)
        send_mail(
            f'New Contact Form Submission from {name}',
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Add a success message
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return redirect('contact')