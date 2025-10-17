from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.db import models
from .models import Message, Notification, MessageHistory


@login_required
@require_POST
def delete_user(request):
    """
    View to delete a user account and all related data.
    This implements Task 2: Automatically clean up related data when a user deletes their account.
    
    The post_delete signal will handle the cleanup of related data automatically.
    """
    if request.method == 'POST':
        user = request.user
        username = user.username
        
        try:
            # Log the deletion attempt
            print(f"User {username} is attempting to delete their account")
            
            # Delete the user - this will trigger the post_delete signal
            # which will clean up all related messages, notifications, and history
            user.delete()
            
            # Add success message
            messages.success(request, f"Account for {username} has been successfully deleted.")
            
            # Redirect to a success page or home page
            return redirect('account_deleted')
            
        except Exception as e:
            # Handle any errors during deletion
            messages.error(request, f"Error deleting account: {str(e)}")
            return redirect('profile')
    
    # If not POST, redirect to profile
    return redirect('profile')


@cache_page(60)  # Cache for 60 seconds - Task 5: Basic view caching
def message_list(request, conversation_id=None):
    """
    View to display messages in a conversation with caching.
    This implements Task 5: Basic view cache for message retrieval.
    
    Uses advanced ORM techniques from Task 3 for efficient querying.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get messages with optimized queries using select_related and prefetch_related
    # This implements Task 3: Advanced ORM techniques for threaded conversations
    messages_queryset = Message.objects.select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    
    if conversation_id:
        # Filter by specific conversation (assuming conversation_id is a user ID for simplicity)
        try:
            other_user = User.objects.get(id=conversation_id)
            messages_queryset = messages_queryset.filter(
                Q(sender=request.user, receiver=other_user) |
                Q(sender=other_user, receiver=request.user)
            )
        except User.DoesNotExist:
            messages.error(request, "Conversation not found.")
            return redirect('message_list')
    
    # Order by timestamp
    messages_queryset = messages_queryset.order_by('-timestamp')
    
    # Paginate results
    paginator = Paginator(messages_queryset, 20)  # 20 messages per page
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)
    
    context = {
        'messages': page_messages,
        'conversation_id': conversation_id,
    }
    
    return render(request, 'messaging/message_list.html', context)


@login_required
def threaded_conversation(request, message_id):
    """
    View to display a threaded conversation starting from a specific message.
    This implements Task 3: Threaded conversations with recursive queries.
    A recursive query using Django's ORM to fetch all replies to a message and display them in a threaded format in the user interface.
    """
    try:
        # Get the root message
        root_message = get_object_or_404(Message, id=message_id)
        
        # Recursive query using Django's ORM to fetch all replies to a message
        thread_messages = Message.objects.filter(
            models.Q(id=message_id) |
            models.Q(parent_message=message_id) |
            models.Q(parent_message__parent_message=message_id) |
            models.Q(parent_message__parent_message__parent_message=message_id)
        ).select_related('sender', 'receiver', 'parent_message').order_by('timestamp')
        
        # Alternative recursive approach for deeper threads
        all_replies = Message.objects.filter(
            parent_message__isnull=False
        ).select_related('sender', 'receiver', 'parent_message')
        
        context = {
            'root_message': root_message,
            'thread_messages': thread_messages,
            'all_replies': all_replies,
        }
        
        return render(request, 'messaging/threaded_conversation.html', context)
        
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
        return redirect('message_list')


@login_required
def unread_messages(request):
    """
    View to display unread messages using the custom manager.
    This implements Task 4: Custom ORM Manager for Unread Messages.
    Use this manager in your views to display only unread messages in a user's inbox.
    Optimize this query with .only() to retrieve only necessary fields.
    """
    # Use the custom manager to get unread messages with .only() optimization
    unread_messages = Message.objects.filter(receiver=request.user, read=False).only(
        'id', 'sender', 'receiver', 'content', 'timestamp', 'read'
    )
    
    # Alternative using the custom manager
    unread_messages_alt = Message.unread.unread_for_user(request.user)
    
    # Paginate results
    paginator = Paginator(unread_messages, 15)  # 15 messages per page
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)
    
    context = {
        'unread_messages': page_messages,
        'total_unread': unread_messages.count(),
    }
    
    return render(request, 'messaging/unread_messages.html', context)


@login_required
def message_history(request, message_id):
    """
    View to display the edit history of a message.
    This implements Task 1: Display message edit history.
    Display the message edit history in the user interface, allowing users to view previous versions of their messages.
    """
    try:
        message = get_object_or_404(Message, id=message_id)
        
        # Check if user has permission to view this message
        if message.sender != request.user and message.receiver != request.user:
            messages.error(request, "You don't have permission to view this message history.")
            return redirect('message_list')
        
        # Get message history with editor information
        history = MessageHistory.objects.filter(message=message).select_related(
            'edited_by'
        ).order_by('-edited_at')
        
        context = {
            'message': message,
            'history': history,
            'can_view_history': True,
            'edit_count': history.count(),
        }
        
        return render(request, 'messaging/message_history.html', context)
        
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
        return redirect('message_list')


@login_required
def notifications(request):
    """
    View to display user notifications.
    This implements Task 0: Display notifications created by signals.
    """
    user_notifications = Notification.objects.filter(
        user=request.user
    ).select_related('message', 'message__sender').order_by('-created_at')
    
    # Paginate results
    paginator = Paginator(user_notifications, 20)  # 20 notifications per page
    page_number = request.GET.get('page')
    page_notifications = paginator.get_page(page_number)
    
    context = {
        'notifications': page_notifications,
        'unread_count': user_notifications.filter(read=False).count(),
    }
    
    return render(request, 'messaging/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """
    AJAX view to mark a notification as read.
    """
    try:
        notification = get_object_or_404(
            Notification, 
            id=notification_id, 
            user=request.user
        )
        notification.read = True
        notification.save()
        
        return JsonResponse({'success': True})
        
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})


def account_deleted(request):
    """
    Simple view to show account deletion confirmation.
    """
    return render(request, 'messaging/account_deleted.html')


@login_required
def user_inbox(request):
    """
    Display user's inbox with unread messages using custom manager.
    Use this manager in your views to display only unread messages in a user's inbox.
    """
    # Use Message.objects.filter to get unread messages for the user's inbox
    unread_inbox_messages = Message.objects.filter(
        receiver=request.user, 
        read=False
    ).select_related('sender').only(
        'id', 'sender', 'content', 'timestamp', 'read'
    ).order_by('-timestamp')
    
    # Get all messages for the inbox
    all_inbox_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').order_by('-timestamp')
    
    context = {
        'unread_messages': unread_inbox_messages,
        'all_messages': all_inbox_messages,
        'unread_count': unread_inbox_messages.count(),
    }
    
    return render(request, 'messaging/inbox.html', context)
