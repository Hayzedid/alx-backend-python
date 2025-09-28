import django_filters
from django.db import models
from .models import Message, Conversation, User


class MessageFilter(django_filters.FilterSet):
    """Filter for messages with time range and user filtering"""
    
    # Date range filtering
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    
    # User filtering
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains')
    sender_name = django_filters.CharFilter(field_name='sender__first_name', lookup_expr='icontains')
    
    # Conversation filtering
    conversation_id = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    
    # Message content filtering
    message_contains = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    
    # Date range for specific day
    sent_on = django_filters.DateFilter(field_name='sent_at', lookup_expr='date')
    
    class Meta:
        model = Message
        fields = [
            'conversation', 'sender', 'sent_at', 'sent_after', 'sent_before',
            'sender_email', 'sender_name', 'conversation_id', 'message_contains', 'sent_on'
        ]


class ConversationFilter(django_filters.FilterSet):
    """Filter for conversations"""
    
    # Participant filtering
    participant_email = django_filters.CharFilter(field_name='participants__email', lookup_expr='icontains')
    participant_name = django_filters.CharFilter(field_name='participants__first_name', lookup_expr='icontains')
    
    # Date filtering
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_on = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    
    # Message count filtering
    has_messages = django_filters.BooleanFilter(field_name='messages', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = Conversation
        fields = [
            'participants', 'created_at', 'participant_email', 'participant_name',
            'created_after', 'created_before', 'created_on', 'has_messages'
        ]


class UserFilter(django_filters.FilterSet):
    """Filter for users"""
    
    # Name filtering
    name_contains = django_filters.CharFilter(method='filter_name_contains')
    
    # Email filtering
    email_contains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    # Date filtering
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    def filter_name_contains(self, queryset, name, value):
        """Filter by first name or last name containing the value"""
        return queryset.filter(
            models.Q(first_name__icontains=value) | 
            models.Q(last_name__icontains=value)
        )
    
    class Meta:
        model = User
        fields = [
            'role', 'created_at', 'name_contains', 'email_contains',
            'created_after', 'created_before'
        ]
