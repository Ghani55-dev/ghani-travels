import logging
from django.utils import timezone
logger = logging.getLogger(__name__)

class PaymentSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if we're in a payment flow
        if 'payment_data' in request.session:
            # Update last active timestamp
            request.session['last_active'] = str(timezone.now())
            request.session.modified = True
            
        return response
        
        # # Verify session for payment routes
        # if request.path.startswith('/payment/'):
        #     if 'payment_data' not in request.session:
        #         logger.warning(f"Missing payment_data in session for {request.path}")
        
        # return response