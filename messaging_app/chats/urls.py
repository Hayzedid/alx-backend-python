from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
# Using routers.DefaultRouter() from rest-framework to automatically create URLs
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Create nested router for messages within conversations
# Using NestedDefaultRouter for nested relationships
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
