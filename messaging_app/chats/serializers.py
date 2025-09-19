from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        validated_data['sender'] = sender
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids',
            'messages', 'message_count', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """Get the count of messages in the conversation"""
        return obj.messages.count()

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for conversation listing"""
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'last_message',
            'message_count', 'created_at'
        ]

    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.messages.last()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'sender': last_message.sender.email,
                'message_body': last_message.message_body[:100] + '...' if len(last_message.message_body) > 100 else last_message.message_body,
                'sent_at': last_message.sent_at
            }
        return None

    def get_message_count(self, obj):
        """Get the count of messages in the conversation"""
        return obj.messages.count()


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new messages"""
    sender_id = serializers.UUIDField()

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation', 'message_body']

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        validated_data['sender'] = sender
        return super().create(validated_data)
