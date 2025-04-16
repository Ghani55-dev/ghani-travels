from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from myapp import views  # Import views from the app
from django.contrib.auth.views import LogoutView
from myapp.views import logout_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from .templates import registration
from django.conf import settings
from .views import RegisterUserView
from .views import CustomLoginView
from .views import AIChatView
from .views import login_view
from myapp.views import generate_ticket
from .views import dashboard
from .views import payment_failed
from .views import register
from .views import AIChatView, chat_interface
from django.conf.urls.static import static
from .views import (
    PaymentView,
    UpiPaymentView,
    ProcessPaymentView,
    stripe_webhook,
    payment_success,
    payment_failed,
    CreateBookingView,
    stripe_webhook,
    view_ticket,
    confirm_booking,
)


urlpatterns = [
    path('', views.home, name='home'),
    #path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('service/',views.service, name='service'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('tours/', views.tours, name='tours'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("login/", views.login_view, name="login"),
    path('', views.main_page, name='main_page'),  # Ensure this is added
   # path('register/', views.register_view, name='register'),
    
    #path('packages/', views.package_list, name='package_list'),
    #path('book/', booking, name='booking'),
    path('book/', views.book_package, name='book_package'),
    # path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('payment/create-checkout-session/<int:package_id>/', views.create_checkout_session, name='create_checkout'),
    path('reviews/add/<int:package_id>/', views.add_review, name='add_review'),
    path('package/<int:package_id>/review/', views.add_review, name='add_review'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('tours/', views.tours, name='tour-list'),
    path('tours/<int:pk>/', views.TourDetailView, name='tour-detail'),
    path('bookings/', views.BookingForm, name='booking-list'),

    # path('ai/chat/', views.AIChatView, name='ai-chat'),
    path('auth/login/', views.login_view, name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    #path('register/', views.register_view, name='register'),
    path('register/', views.register, name='register'),
    path("register/", views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('login/', login_view, name='login'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    
    path('generate-ticket/<int:booking_id>/', generate_ticket, name='generate_ticket'),
    
    # # path('payment/', views.payment_page, name='payment'),
    # path('process-payment/', views.process_payment, name='process_payment'),
    # path('process-payment/', process_payment, name='process_payment'),
    # path('payment_failed/', payment_failed, name='payment_failed'),
    # path('payment-success/', views.payment_success, name='payment_success'),
    # path('webhook/payment/', views.payment_webhook, name='payment_webhook'),
    # path('stripe-webhook/', views.payment_webhook, name='stripe-webhook'),
    # # path('payment/', payment_page, name='payment'),
    # path('payment/', payment_page, name='payment_page'),
    # # path('ticket-selection/', views.ticket_selection, name='ticket_selection'),
    # # path('payment-failed/', views.payment_failed, name='payment_failed'),
    # path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    
    
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    
    path('ai-chat/', AIChatView.as_view(), name='ai_chat'),
    path('chat/', chat_interface, name='chat_interface'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('registration_success/', views.registration_success, name='registration_success'),
    # path('payment/', PaymentView.as_view(), name='payment_page'),
    # path('payment/upi/', UpiPaymentView.as_view(), name='upi_payment'),
    # path('payment/save_upi_session/', SaveUpiSessionView.as_view(), name='save_upi_sessio'),
    # path('payment/process/', ProcessPaymentView.as_view(), name='process_payment'),
    # path('payment/success/', payment_success, name='payment_success'),
    # path('payment/failed/', payment_failed, name='payment_failed'),
    # path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('view-ticket/', view_ticket, name='view_ticket'),
    path('booking/<int:booking_id>/confirm/', confirm_booking, name='confirm_booking'),
    
    
    # Payment views
    path('payment/', PaymentView.as_view(), name='payment_page'),
    path('upi-payment/', UpiPaymentView.as_view(), name='upi_payment'),
    path('process-payment/', ProcessPaymentView.as_view(), name='process_payment'),
    
    # Webhook for Stripe events
    path('stripe-webhook/', stripe_webhook, name='stripe_webhook'),
    
    # Payment outcome pages
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-failed/', payment_failed, name='payment_failed'),
    
    # Create booking prior to payment
    path('create-booking/', CreateBookingView.as_view(), name='create_booking'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)