from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = CharField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested relationships"""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_body = CharField(max_length=5000, required=True)
    conversation_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 
            'conversation_id', 'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        """Validate message body"""
        if not value or len(value.strip()) == 0:
            raise ValidationError("Message body cannot be empty.")
        return value

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        validated_data['sender'] = sender
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested relationships"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids',
            'messages', 'message_count', 'last_message', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """Get the count of messages in the conversation"""
        return obj.messages.count()

    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def validate_participant_ids(self, value):
        """Validate participant IDs"""
        if value and len(value) < 2:
            raise ValidationError("A conversation must have at least 2 participants.")
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            if participants.count() != len(participant_ids):
                raise ValidationError("Some participant IDs are invalid.")
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
    """Serializer for creating new messages with validation"""
    sender_id = serializers.UUIDField(required=True)
    message_body = CharField(max_length=5000, required=True)

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation', 'message_body']

    def validate_message_body(self, value):
        """Validate message body"""
        if not value or len(value.strip()) == 0:
            raise ValidationError("Message body cannot be empty.")
        return value

    def validate_sender_id(self, value):
        """Validate sender exists"""
        if not User.objects.filter(user_id=value).exists():
            raise ValidationError("Invalid sender ID.")
        return value

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        validated_data['sender'] = sender
        return super().create(validated_data)
