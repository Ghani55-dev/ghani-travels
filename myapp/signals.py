from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Booking
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_booking_confirmation():
    email_host = settings.EMAIL_HOST
    print(settings.EMAIL_HOST) 

@receiver(post_save, sender=Booking)
def send_booking_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = f"Booking Confirmation: {instance.tour_package.title}"
        message = render_to_string('registration/booking_confirmation.html', {'booking': instance})
        send_mail(
            subject,
            strip_tags(message),
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            html_message=message
        )
        logger.info(f"Sent booking confirmation to {instance.user.email}")