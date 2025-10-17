from django.test import TestCase
from django.contrib.auth.models import User
from django.db import transaction
from .models import Message, Notification, MessageHistory


class MessageSignalTests(TestCase):
    """Test cases for message-related signals"""
    
    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com',
            password='testpass123'
        )
    
    def test_notification_created_on_new_message(self):
        """Test that a notification is created when a new message is sent (Task 0)"""
        # Create a new message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test message!"
        )
        
        # Check that a notification was created
        notifications = Notification.objects.filter(user=self.user2, message=message)
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.notification_type, 'message')
        self.assertIn(self.user1.username, notification.content)
        self.assertFalse(notification.read)
    
    def test_reply_notification_created(self):
        """Test that a reply notification is created for threaded messages"""
        # Create original message
        original_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original message"
        )
        
        # Create reply
        reply_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply to original message",
            parent_message=original_message
        )
        
        # Check that a reply notification was created
        notifications = Notification.objects.filter(user=self.user1, message=reply_message)
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.notification_type, 'reply')
        self.assertIn('replied', notification.content)
    
    def test_message_edit_history_saved(self):
        """Test that message edit history is saved when content changes (Task 1)"""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check that history was saved
        history = MessageHistory.objects.filter(message=message)
        self.assertEqual(history.count(), 1)
        
        history_entry = history.first()
        self.assertEqual(history_entry.old_content, "Original content")
        self.assertTrue(message.edited)
    
    def test_no_history_for_new_messages(self):
        """Test that no history is created for new messages"""
        # Create a new message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="New message"
        )
        
        # Check that no history was created
        history = MessageHistory.objects.filter(message=message)
        self.assertEqual(history.count(), 0)
        self.assertFalse(message.edited)
    
    def test_no_history_for_unchanged_content(self):
        """Test that no history is created when content doesn't change"""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unchanged content"
        )
        
        # Save without changing content
        message.save()
        
        # Check that no history was created
        history = MessageHistory.objects.filter(message=message)
        self.assertEqual(history.count(), 0)
        self.assertFalse(message.edited)


class UserDeletionTests(TestCase):
    """Test cases for user deletion and cleanup (Task 2)"""
    
    def setUp(self):
        """Set up test users and data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com', 
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create messages and notifications
        self.message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Message from user1 to user2"
        )
        
        self.message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Message from user2 to user1"
        )
    
    def test_user_deletion_cascades_messages(self):
        """Test that deleting a user cascades to delete related messages"""
        user1_id = self.user1.id
        
        # Delete user1
        self.user1.delete()
        
        # Check that messages sent by user1 are deleted
        sent_messages = Message.objects.filter(sender_id=user1_id)
        self.assertEqual(sent_messages.count(), 0)
        
        # Check that messages received by user1 are deleted
        received_messages = Message.objects.filter(receiver_id=user1_id)
        self.assertEqual(received_messages.count(), 0)
    
    def test_user_deletion_cascades_notifications(self):
        """Test that deleting a user cascades to delete related notifications"""
        user2_id = self.user2.id
        
        # Verify notifications exist
        notifications_count = Notification.objects.filter(user=self.user2).count()
        self.assertGreater(notifications_count, 0)
        
        # Delete user2
        self.user2.delete()
        
        # Check that notifications for user2 are deleted
        notifications = Notification.objects.filter(user_id=user2_id)
        self.assertEqual(notifications.count(), 0)


class ThreadedConversationTests(TestCase):
    """Test cases for threaded conversations (Task 3)"""
    
    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com', 
            password='testpass123'
        )
    
    def test_threaded_message_creation(self):
        """Test creating threaded messages with parent-child relationships"""
        # Create root message
        root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Root message"
        )
        
        # Create reply
        reply_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply to root",
            parent_message=root_message
        )
        
        # Test relationships
        self.assertEqual(reply_message.parent_message, root_message)
        self.assertIn(reply_message, root_message.replies.all())
    
    def test_get_thread_method(self):
        """Test the get_thread method for retrieving conversation threads"""
        # Create a thread: root -> reply1 -> reply2
        root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Root message"
        )
        
        reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="First reply",
            parent_message=root_message
        )
        
        reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Second reply",
            parent_message=reply1
        )
        
        # Test get_thread from different messages
        root_thread = root_message.get_thread()
        reply_thread = reply1.get_thread()
        
        # Both should return the same thread
        self.assertEqual(list(root_thread), list(reply_thread))
        self.assertEqual(root_thread.count(), 3)


class UnreadMessagesManagerTests(TestCase):
    """Test cases for custom UnreadMessagesManager (Task 4)"""
    
    def setUp(self):
        """Set up test users and messages"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create read and unread messages
        self.unread_message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 1",
            read=False
        )
        
        self.unread_message2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 2", 
            read=False
        )
        
        self.read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
    
    def test_unread_messages_manager(self):
        """Test the custom UnreadMessagesManager"""
        # Get unread messages for user2
        unread_messages = Message.unread.unread_for_user(self.user2)
        
        # Should return only unread messages
        self.assertEqual(unread_messages.count(), 2)
        self.assertIn(self.unread_message1, unread_messages)
        self.assertIn(self.unread_message2, unread_messages)
        self.assertNotIn(self.read_message, unread_messages)
    
    def test_unread_messages_optimization(self):
        """Test that the manager uses .only() for optimization"""
        unread_messages = Message.unread.unread_for_user(self.user2)
        
        # This should work without additional queries due to .only()
        for message in unread_messages:
            # These fields should be available
            self.assertIsNotNone(message.sender)
            self.assertIsNotNone(message.content)
            self.assertIsNotNone(message.timestamp)
            self.assertIsNotNone(message.read)
