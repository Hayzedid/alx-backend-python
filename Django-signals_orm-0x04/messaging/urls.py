from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Message views
    path('', views.message_list, name='message_list'),
    path('conversation/<int:conversation_id>/', views.message_list, name='conversation_detail'),
    path('thread/<uuid:message_id>/', views.threaded_conversation, name='threaded_conversation'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('history/<uuid:message_id>/', views.message_history, name='message_history'),
    
    # Notification views
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<uuid:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # User management views
    path('delete-account/', views.delete_user, name='delete_user'),
    path('account-deleted/', views.account_deleted, name='account_deleted'),
]
