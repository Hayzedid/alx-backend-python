from django.contrib.auth.models import User
from django.db import models
import uuid
from .managers import UnreadMessagesManager


class Message(models.Model):
    """Model for storing messages between users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='edited_messages',
        help_text="User who last edited this message"
    )
    edited_at = models.DateTimeField(null=True, blank=True)
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
    """
    Model for storing message edit history.
    Display the message edit history in the user interface, allowing users to view previous versions of their messages.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='message_edit_history',
        help_text="User who made this edit"
    )
    edited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"
    
    def __str__(self):
        editor = self.edited_by.username if self.edited_by else "Unknown"
        return f"History for message {self.message.id} edited by {editor} at {self.edited_at}"
