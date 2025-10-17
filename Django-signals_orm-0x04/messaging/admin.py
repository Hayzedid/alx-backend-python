from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model"""
    list_display = ['id', 'sender', 'receiver', 'content_preview', 'timestamp', 'edited', 'edited_by', 'read']
    list_filter = ['timestamp', 'edited', 'read', 'sender', 'receiver', 'edited_by']
    search_fields = ['content', 'sender__username', 'receiver__username']
    readonly_fields = ['id', 'timestamp', 'edited_at']
    raw_id_fields = ['sender', 'receiver', 'parent_message', 'edited_by']
    
    def content_preview(self, obj):
        """Show a preview of the message content"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model"""
    list_display = ['id', 'user', 'notification_type', 'content_preview', 'read', 'created_at']
    list_filter = ['notification_type', 'read', 'created_at', 'user']
    search_fields = ['content', 'user__username']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['user', 'message']
    
    def content_preview(self, obj):
        """Show a preview of the notification content"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """Admin interface for MessageHistory model"""
    list_display = ['id', 'message', 'old_content_preview', 'edited_by', 'edited_at']
    list_filter = ['edited_at', 'edited_by']
    search_fields = ['old_content', 'message__content', 'edited_by__username']
    readonly_fields = ['id', 'edited_at']
    raw_id_fields = ['message', 'edited_by']
    
    def old_content_preview(self, obj):
        """Show a preview of the old content"""
        return obj.old_content[:50] + "..." if len(obj.old_content) > 50 else obj.old_content
    old_content_preview.short_description = "Old Content Preview"
