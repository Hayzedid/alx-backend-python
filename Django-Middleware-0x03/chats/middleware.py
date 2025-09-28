import logging
from datetime import datetime
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict, deque
import time


class RequestLoggingMiddleware:
    """
    Middleware to log user requests with timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('requests.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def __call__(self, request):
        # Get user information
        user = getattr(request, 'user', None)
        user_info = user.email if user and hasattr(user, 'email') else 'Anonymous'
        
        # Log the request
        self.logger.info(f"{datetime.now()} - User: {user_info} - Path: {request.path}")
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to messaging app during certain hours (9PM to 6AM).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_hour = datetime.now().hour
        
        # Check if current time is between 9PM (21) and 6AM (6)
        if current_hour >= 21 or current_hour < 6:
            return JsonResponse({
                'error': 'Access denied',
                'message': 'Messaging app is not available between 9PM and 6AM',
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, status=403)
        
        # Allow access during allowed hours
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send within a time window.
    Implements rate limiting: 5 messages per minute per IP address.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP address
        self.request_counts = defaultdict(lambda: deque())
        self.max_requests = 5  # Maximum requests per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests (message creation)
        if request.method == 'POST':
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            while (self.request_counts[ip_address] and 
                   current_time - self.request_counts[ip_address][0] > self.time_window):
                self.request_counts[ip_address].popleft()
            
            # Check if user has exceeded the limit
            if len(self.request_counts[ip_address]) >= self.max_requests:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'You can only send {self.max_requests} messages per minute',
                    'retry_after': int(self.time_window - (current_time - self.request_counts[ip_address][0]))
                }, status=429)
            
            # Record this request
            self.request_counts[ip_address].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware that checks user roles before allowing access to specific actions.
    Only admin and moderator roles are allowed to access certain endpoints.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define restricted paths that require admin/moderator access
        self.restricted_paths = [
            '/api/conversations/',
            '/api/messages/',
            '/api/users/'
        ]
    
    def __call__(self, request):
        # Check if the request path requires role-based access
        if any(request.path.startswith(path) for path in self.restricted_paths):
            user = getattr(request, 'user', None)
            
            # Check if user is authenticated and has required role
            if not user or not user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'message': 'You must be logged in to access this resource'
                }, status=401)
            
            # Check if user has admin or moderator role
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return JsonResponse({
                    'error': 'Access denied',
                    'message': 'You must be an admin or moderator to access this resource',
                    'current_role': user_role
                }, status=403)
        
        response = self.get_response(request)
        return response
