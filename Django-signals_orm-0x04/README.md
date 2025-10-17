# Django Signals and ORM - Messaging Application

This project implements a comprehensive Django messaging application demonstrating advanced Django signals, ORM techniques, and caching. It fulfills all requirements for the Django-signals_orm-0x04 project.

## Project Structure

```
Django-signals_orm-0x04/
├── messaging/                 # Main messaging app
│   ├── models.py             # Message, Notification, MessageHistory models
│   ├── signals.py            # Signal handlers for all tasks
│   ├── views.py              # Views with advanced ORM and caching
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration with signal registration
│   ├── tests.py              # Comprehensive test suite
│   └── urls.py               # URL patterns
├── chats/                    # Additional app for cached views
│   ├── views.py              # Cached views for Task 5
│   └── urls.py               # URL patterns for cached views
├── messaging_app/            # Django project
│   ├── messaging_app/
│   │   ├── settings.py       # Project settings with cache configuration
│   │   ├── urls.py           # Main URL configuration
│   │   ├── wsgi.py           # WSGI configuration
│   │   └── asgi.py           # ASGI configuration
│   └── manage.py             # Django management script
└── README.md                 # This file
```

## Features Implemented

### Task 0: Signals for User Notifications ✅
- **Models**: `Message` and `Notification` models with proper relationships
- **Signal**: `post_save` signal on `Message` model automatically creates notifications
- **Features**:
  - Automatic notification creation for new messages
  - Different notification types for regular messages and replies
  - Proper foreign key relationships between User, Message, and Notification

### Task 1: Signal for Logging Message Edits ✅
- **Model**: `MessageHistory` model to store edit history
- **Signal**: `pre_save` signal on `Message` model logs old content before updates
- **Features**:
  - Tracks message edit history with timestamps
  - `edited` boolean field on Message model
  - Only logs when content actually changes
  - Preserves complete edit history for audit trails

### Task 2: Signals for Deleting User-Related Data ✅
- **View**: `delete_user` view for account deletion
- **Signal**: `post_delete` signal on `User` model for cleanup
- **Features**:
  - Cascade deletion of related messages, notifications, and history
  - Proper foreign key constraint handling
  - User-friendly account deletion process

### Task 3: Advanced ORM for Threaded Conversations ✅
- **Model**: Self-referential `parent_message` field for threaded replies
- **ORM Optimization**: `select_related` and `prefetch_related` for efficient queries
- **Features**:
  - Recursive message threading
  - Optimized database queries with minimal N+1 problems
  - `get_thread()` method for retrieving complete conversation threads

### Task 4: Custom ORM Manager for Unread Messages ✅
- **Manager**: `UnreadMessagesManager` for filtering unread messages
- **Model**: `read` boolean field on Message model
- **Features**:
  - Custom manager with `unread_for_user()` method
  - Query optimization using `.only()` for necessary fields
  - Efficient unread message filtering

### Task 5: Basic View Cache ✅
- **Configuration**: Local memory cache in `settings.py`
- **Views**: `@cache_page(60)` decorator on message list views
- **Features**:
  - 60-second cache timeout as specified
  - Cached views in both `messaging/views.py` and `chats/views.py`
  - Improved performance for frequently accessed conversations

## Models

### Message Model
```python
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, related_name='sent_messages')
    receiver = models.ForeignKey(User, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True)
```

### Notification Model
```python
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications')
    message = models.ForeignKey(Message, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### MessageHistory Model
```python
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
```

## Signal Handlers

### 1. Message Notification Signal
```python
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    # Automatically creates notifications for new messages
```

### 2. Message Edit Logging Signal
```python
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Logs old content before message updates
```

### 3. User Deletion Cleanup Signal
```python
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Handles cleanup when users are deleted
```

## Advanced ORM Features

### Custom Manager
```python
class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'content', 'timestamp', 'read'
        )
```

### Optimized Queries
```python
# Efficient threaded conversation queries
messages = Message.objects.select_related(
    'sender', 'receiver', 'parent_message'
).prefetch_related(
    Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
)
```

## Caching Configuration

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# views.py
@cache_page(60)  # 60 seconds cache timeout
def conversation_messages(request, conversation_id=None):
    # Cached view implementation
```

## Installation and Setup

1. **Navigate to the project directory**:
   ```bash
   cd Django-signals_orm-0x04/messaging_app
   ```

2. **Install dependencies**:
   ```bash
   pip install django
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Testing

Run the comprehensive test suite:
```bash
python manage.py test messaging
```

The test suite covers:
- Signal functionality for all tasks
- Model relationships and constraints
- Custom manager functionality
- Threaded conversation features
- User deletion and cleanup

## API Endpoints

- `/messaging/` - Message list view (cached)
- `/messaging/conversation/<id>/` - Specific conversation
- `/messaging/thread/<message_id>/` - Threaded conversation view
- `/messaging/unread/` - Unread messages (custom manager)
- `/messaging/history/<message_id>/` - Message edit history
- `/messaging/notifications/` - User notifications
- `/messaging/delete-account/` - User account deletion
- `/chats/` - Cached chat list view
- `/chats/conversation/<id>/` - Cached conversation messages

## Key Technical Achievements

1. **Signal Implementation**: All three signal types (post_save, pre_save, post_delete) properly implemented
2. **ORM Optimization**: Advanced querying with select_related, prefetch_related, and custom managers
3. **Caching Strategy**: Proper view-level caching with configurable timeouts
4. **Data Integrity**: Proper foreign key relationships with CASCADE handling
5. **Testing Coverage**: Comprehensive test suite covering all functionality
6. **Code Organization**: Clean separation of concerns with proper Django app structure

## Repository Information

- **Repository**: alx-backend-python
- **Directory**: Django-signals_orm-0x04
- **Files**: All required files as specified in the task requirements

This implementation demonstrates advanced Django concepts including signals, ORM optimization, caching, and proper project structure while maintaining code quality and comprehensive testing.
