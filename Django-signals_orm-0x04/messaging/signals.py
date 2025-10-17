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
    """
    if instance.pk:  # Only for existing messages (updates, not new messages)
        try:
            # Get the old version of the message
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if the content has actually changed
            if old_message.content != instance.content:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                
                # Mark the message as edited
                instance.edited = True
                
        except Message.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler to clean up user-related data when a user is deleted.
    This implements Task 2: Automatically clean up related data when a user deletes their account.
    
    Note: This signal will be triggered when a User is deleted.
    The CASCADE foreign key relationships will handle most cleanup automatically,
    but this signal can be used for additional custom cleanup logic.
    """
    # The CASCADE foreign key relationships will automatically delete:
    # - Messages sent by the user (sent_messages)
    # - Messages received by the user (received_messages)  
    # - Notifications for the user (notifications)
    # - MessageHistory entries (through message deletion)
    
    # Additional custom cleanup can be added here if needed
    # For example, logging the deletion or sending notifications to other users
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
