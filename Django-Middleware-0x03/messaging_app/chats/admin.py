from django.contrib import admin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at', 'get_participants')
    list_filter = ('created_at',)
    search_fields = ('participants__email',)
    ordering = ('-created_at',)

    def get_participants(self, obj):
        return ", ".join([p.email for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    list_filter = ('sent_at', 'conversation')
    search_fields = ('sender__email', 'message_body')
    ordering = ('-sent_at',)


