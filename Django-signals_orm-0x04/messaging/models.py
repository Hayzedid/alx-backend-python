from django.contrib.auth.models import User
from django.db import models
import uuid


class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user"""
    
    def unread_for_user(self, user):
        """Return unread messages for a specific user"""
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'content', 'timestamp', 'read'
        )


class Message(models.Model):
    """Model for storing messages between users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    # Custom manager for unread messages
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'read']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['parent_message']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
    
    def get_thread(self):
        """Get all messages in this thread using recursive query"""
        if self.parent_message:
            # If this is a reply, get the root message's thread
            return self.parent_message.get_thread()
        else:
            # This is the root message, get all replies recursively
            return Message.objects.filter(
                models.Q(id=self.id) | 
                models.Q(parent_message=self.id) |
                models.Q(parent_message__parent_message=self.id) |
                models.Q(parent_message__parent_message__parent_message=self.id)
            ).select_related('sender', 'receiver', 'parent_message').order_by('timestamp')


class Notification(models.Model):
    """Model for storing user notifications"""
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('reply', 'Message Reply'),
        ('mention', 'Mention'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='message')
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"


class MessageHistory(models.Model):
    """Model for storing message edit history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"
    
    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"
