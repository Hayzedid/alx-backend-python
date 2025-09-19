from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[
            ('guest', 'Guest'),
            ('host', 'Host'),
            ('admin', 'Admin'),
        ],
        null=False,
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Override username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Model for tracking conversations between users"""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-created_at']

    def __str__(self):
        participant_names = ", ".join([p.email for p in self.participants.all()])
        return f"Conversation {self.conversation_id} - {participant_names}"


class Message(models.Model):
    """Model for storing messages in conversations"""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['sender', 'sent_at']),
        ]

    def __str__(self):
        return f"Message from {self.sender.email} in {self.conversation.conversation_id}"
