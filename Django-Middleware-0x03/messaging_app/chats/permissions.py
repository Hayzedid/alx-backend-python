from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check if user is a participant of the conversation"""
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Custom permission to allow message sender or conversation participants to access messages.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check if user is the sender or a participant of the conversation"""
        if isinstance(obj, Message):
            # Allow if user is the sender
            if obj.sender.user_id == request.user.user_id:
                return True
            # Allow if user is a participant in the conversation
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission to ensure only conversation participants can perform actions.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check if user is a participant of the conversation"""
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        return False
