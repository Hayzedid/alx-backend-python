# Django Middleware Implementation

This project demonstrates the implementation of custom Django middleware for a messaging application, showcasing various middleware patterns and use cases.

## 🚀 Middleware Components

### 1. RequestLoggingMiddleware
**Purpose:** Logs all user requests with timestamp, user information, and request path.

**Features:**
- Logs to both file (`requests.log`) and console
- Captures user email or "Anonymous" for unauthenticated users
- Records request path and timestamp

**Usage:**
```python
# Logs: "2024-09-28 21:30:45 - User: john@example.com - Path: /api/messages/"
```

### 2. RestrictAccessByTimeMiddleware
**Purpose:** Restricts access to the messaging app during certain hours (9PM to 6AM).

**Features:**
- Blocks access between 9PM and 6AM
- Returns 403 Forbidden with error message
- Shows current time in error response

**Response:**
```json
{
    "error": "Access denied",
    "message": "Messaging app is not available between 9PM and 6AM",
    "current_time": "2024-09-28 21:30:45"
}
```

### 3. OffensiveLanguageMiddleware (Rate Limiting)
**Purpose:** Implements rate limiting to prevent spam - 5 messages per minute per IP address.

**Features:**
- Tracks POST requests per IP address
- 5 messages per minute limit
- Automatic cleanup of old requests
- Returns 429 Too Many Requests when limit exceeded

**Response:**
```json
{
    "error": "Rate limit exceeded",
    "message": "You can only send 5 messages per minute",
    "retry_after": 45
}
```

### 4. RolePermissionMiddleware
**Purpose:** Enforces role-based access control for admin and moderator roles.

**Features:**
- Restricts access to specific API endpoints
- Requires admin or moderator role
- Returns 401 for unauthenticated users
- Returns 403 for insufficient permissions

**Response:**
```json
{
    "error": "Access denied",
    "message": "You must be an admin or moderator to access this resource",
    "current_role": "guest"
}
```

## 📁 Project Structure

```
Django-Middleware-0x03/
├── chats/
│   ├── middleware.py          # All custom middleware classes
│   ├── models.py              # User, Conversation, Message models
│   ├── views.py               # API viewsets
│   └── ...
├── messaging_app/
│   ├── settings.py            # Middleware configuration
│   └── ...
├── requests.log               # Generated log file
└── new folder/                # Manual review
```

## ⚙️ Configuration

### Middleware Order in settings.py:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolePermissionMiddleware',
]
```

## 🧪 Testing

### 1. Test Request Logging
```bash
# Make any request to see logs in requests.log
curl http://localhost:8000/api/messages/
```

### 2. Test Time Restriction
```bash
# Access between 9PM-6AM to see 403 error
curl http://localhost:8000/api/messages/
```

### 3. Test Rate Limiting
```bash
# Send multiple POST requests quickly
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/messages/ \
    -H "Content-Type: application/json" \
    -d '{"conversation": "uuid", "message_body": "Test message"}'
done
```

### 4. Test Role Permissions
```bash
# Access with guest role to see 403 error
curl http://localhost:8000/api/conversations/
```

## 🔧 Implementation Details

### Middleware Class Structure
Each middleware follows the standard Django pattern:
```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        # Process response
        return response
```

### Key Features:
- **Request Processing:** Intercept and modify incoming requests
- **Response Processing:** Modify outgoing responses
- **Error Handling:** Return appropriate HTTP status codes
- **Logging:** Track and log request information
- **Rate Limiting:** Implement time-based request limits
- **Access Control:** Enforce role-based permissions

## 📊 Generated Files

- **`requests.log`** - Contains all request logs with timestamps and user information
- **Console output** - Real-time logging of requests

## 🚀 Running the Application

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start the server:**
   ```bash
   python manage.py runserver
   ```

4. **Test middleware:**
   - Make requests to see logging
   - Test time restrictions
   - Test rate limiting
   - Test role permissions

## 📝 Best Practices Demonstrated

- **Single Responsibility:** Each middleware has one clear purpose
- **Error Handling:** Proper HTTP status codes and error messages
- **Performance:** Efficient data structures for rate limiting
- **Logging:** Comprehensive request logging
- **Security:** Role-based access control
- **Documentation:** Clear comments and docstrings

---

**Developed as part of ALX Backend Python Specialization - Django Middleware Project**