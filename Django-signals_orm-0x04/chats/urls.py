from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    # Cached chat views for Task 5
    path('', views.chat_list, name='chat_list'),
    path('conversation/<int:conversation_id>/', views.conversation_messages, name='conversation_messages'),
    path('public/', views.public_messages, name='public_messages'),
]
