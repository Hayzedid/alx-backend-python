from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """Custom pagination for messages"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ConversationPagination(PageNumberPagination):
    """Custom pagination for conversations"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserPagination(PageNumberPagination):
    """Custom pagination for users"""
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100
