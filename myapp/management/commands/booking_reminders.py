from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import Booking

class Command(BaseCommand):
    help = 'Send booking reminders'

    def handle(self, *args, **options):
        upcoming = Booking.objects.filter(
            start_date__range=(timezone.now(), timezone.now() + timezone.timedelta(days=3)),
            reminder_sent=False
        )
        
        for booking in upcoming:
            send_reminder_email(booking)
            booking.reminder_sent = True
            booking.save()
            self.stdout.write(f"Sent reminder to {booking.user.email}")