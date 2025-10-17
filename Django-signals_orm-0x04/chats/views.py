from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q
from messaging.models import Message


@cache_page(60)  # Cache for 60 seconds as required in Task 5
@login_required
def conversation_messages(request, conversation_id=None):
    """
    Cached view that displays a list of messages in a conversation.
    This implements Task 5: Basic view cache with 60 seconds timeout.
    
    The cache_page decorator caches the entire view response for 60 seconds,
    improving performance for frequently accessed conversations.
    """
    # Get messages for the current user
    messages_queryset = Message.objects.select_related(
        'sender', 'receiver'
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    
    # If conversation_id is provided, filter messages for that specific conversation
    if conversation_id:
        try:
            # Assuming conversation_id represents the other user's ID
            from django.contrib.auth.models import User
            other_user = get_object_or_404(User, id=conversation_id)
            
            messages_queryset = messages_queryset.filter(
                Q(sender=request.user, receiver=other_user) |
                Q(sender=other_user, receiver=request.user)
            )
        except Exception:
            # If conversation_id is invalid, show all messages
            pass
    
    # Order messages by timestamp (newest first)
    messages_queryset = messages_queryset.order_by('-timestamp')
    
    # Paginate the results
    paginator = Paginator(messages_queryset, 25)  # 25 messages per page
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)
    
    context = {
        'messages': page_messages,
        'conversation_id': conversation_id,
        'total_messages': messages_queryset.count(),
    }
    
    return render(request, 'chats/conversation_messages.html', context)


@cache_page(60)  # Cache for 60 seconds
@login_required 
def chat_list(request):
    """
    Cached view that displays a list of all conversations for the current user.
    This view is also cached for 60 seconds to improve performance.
    """
    # Get all unique conversations for the current user
    # This is a simplified approach - in a real app you might have a Conversation model
    from django.contrib.auth.models import User
    
    # Get all users that the current user has exchanged messages with
    sent_to_users = Message.objects.filter(
        sender=request.user
    ).values_list('receiver', flat=True).distinct()
    
    received_from_users = Message.objects.filter(
        receiver=request.user
    ).values_list('sender', flat=True).distinct()
    
    # Combine and get unique user IDs
    all_user_ids = set(list(sent_to_users) + list(received_from_users))
    
    # Get user objects
    conversation_users = User.objects.filter(id__in=all_user_ids)
    
    # Get the latest message for each conversation
    conversations = []
    for user in conversation_users:
        latest_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        
        if latest_message:
            conversations.append({
                'user': user,
                'latest_message': latest_message,
                'unread_count': Message.objects.filter(
                    sender=user,
                    receiver=request.user,
                    read=False
                ).count()
            })
    
    # Sort conversations by latest message timestamp
    conversations.sort(key=lambda x: x['latest_message'].timestamp, reverse=True)
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'chats/chat_list.html', context)


@cache_page(60)  # Cache for 60 seconds
def public_messages(request):
    """
    Cached view for displaying public messages (if any).
    This demonstrates another cached view with 60 seconds timeout.
    """
    # Get recent public messages (this is a conceptual example)
    # In a real app, you might have a 'public' flag on messages
    recent_messages = Message.objects.select_related(
        'sender'
    ).order_by('-timestamp')[:50]  # Last 50 messages
    
    context = {
        'messages': recent_messages,
    }
    
    return render(request, 'chats/public_messages.html', context)
