from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a new message is created.
    This implements Task 0: Automatically notify users when they receive a new message.
    """
    if created:  # Only trigger for new messages, not updates
        # Determine notification type
        notification_type = 'reply' if instance.parent_message else 'message'
        
        # Create notification content
        if notification_type == 'reply':
            content = f"{instance.sender.username} replied to your message: {instance.content[:50]}..."
        else:
            content = f"New message from {instance.sender.username}: {instance.content[:50]}..."
        
        # Create the notification
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type=notification_type,
            content=content
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler to log message edits before they are saved.
    This implements Task 1: Log when a user edits a message and save the old content.
    Display the message edit history in the user interface, allowing users to view previous versions of their messages.
    """
    if instance.pk:  # Only for existing messages (updates, not new messages)
        try:
            # Get the old version of the message
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if the content has actually changed
            if old_message.content != instance.content:
                # Save the old content to history with editor information
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.edited_by or instance.sender  # Use edited_by if set, otherwise sender
                )
                
                # Mark the message as edited and set edit timestamp
                instance.edited = True
                from django.utils import timezone
                instance.edited_at = timezone.now()
                
        except Message.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler to clean up user-related data when a user is deleted.
    This implements Task 2: Automatically clean up related data when a user deletes their account.
    A post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.
    """
    # Delete all messages sent by the user
    sent_messages = Message.objects.filter(sender=instance)
    sent_messages.delete()
    
    # Delete all messages received by the user
    received_messages = Message.objects.filter(receiver=instance)
    received_messages.delete()
    
    # Delete all notifications for the user
    user_notifications = Notification.objects.filter(user=instance)
    user_notifications.delete()
    
    # Delete all message histories related to the user's messages
    # (This will be handled by CASCADE, but we can also do it explicitly)
    user_message_histories = MessageHistory.objects.filter(
        message__sender=instance
    )
    user_message_histories.delete()
    
    # Additional cleanup for message histories of received messages
    received_message_histories = MessageHistory.objects.filter(
        message__receiver=instance
    )
    received_message_histories.delete()
    
    # Log the deletion
    print(f"User {instance.username} and all related data has been deleted")


# Alternative signal for custom user deletion tracking
@receiver(pre_save, sender=User)
def track_user_deletion_preparation(sender, instance, **kwargs):
    """
    Optional signal to track when a user is about to be deleted.
    This can be used to perform additional cleanup or logging before deletion.
    """
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            # Add any pre-deletion logic here if needed
        except User.DoesNotExist:
            pass
