from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    This implements Task 4: Custom ORM Manager for Unread Messages.
    """
    
    def unread_for_user(self, user):
        """
        Return unread messages for a specific user.
        Uses .only() to retrieve only necessary fields for optimization.
        """
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'receiver', 'content', 'timestamp', 'read'
        )
    
    def get_unread_count(self, user):
        """
        Get the count of unread messages for a user.
        """
        return self.filter(receiver=user, read=False).count()
    
    def mark_as_read(self, user, message_ids=None):
        """
        Mark messages as read for a specific user.
        If message_ids is provided, only mark those specific messages.
        """
        queryset = self.filter(receiver=user, read=False)
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        return queryset.update(read=True)
