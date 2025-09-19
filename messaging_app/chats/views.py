from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, ConversationSerializer, ConversationListSerializer,
    MessageSerializer, MessageCreateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter users based on search parameters"""
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        role = self.request.query_params.get('role', None)
        
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role=role)
            
        return queryset


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model"""
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def get_queryset(self):
        """Filter conversations for the authenticated user"""
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related(
            'participants', 'messages__sender'
        )

    def create(self, request, *args, **kwargs):
        """Create a new conversation"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Add the current user as a participant
            conversation = serializer.save()
            conversation.participants.add(request.user)
            
            # Return the full conversation details
            response_serializer = ConversationSerializer(conversation)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to the conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response({'message': 'Participant added successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """Remove a participant from the conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.remove(user)
            return Response({'message': 'Participant removed successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model"""
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        """Filter messages for conversations the user participates in"""
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation', None)
        
        queryset = Message.objects.filter(
            conversation__participants=user
        ).select_related('sender', 'conversation')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        return queryset.order_by('sent_at')

    def create(self, request, *args, **kwargs):
        """Create a new message"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Ensure the sender is the authenticated user
            serializer.validated_data['sender_id'] = request.user.user_id
            
            # Verify the user is a participant in the conversation
            conversation_id = serializer.validated_data['conversation'].conversation_id
            conversation = get_object_or_404(
                Conversation.objects.filter(participants=request.user),
                conversation_id=conversation_id
            )
            
            message = serializer.save()
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        """Get messages for a specific conversation"""
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = get_object_or_404(
                Conversation.objects.filter(participants=request.user),
                conversation_id=conversation_id
            )
            messages = Message.objects.filter(conversation=conversation).select_related('sender')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
