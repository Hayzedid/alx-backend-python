# Django Messaging App

A Django REST Framework based messaging application with user management, conversations, and real-time messaging capabilities.

## Features

- **User Management**: Custom user model with roles (guest, host, admin)
- **Conversations**: Multi-participant conversation management
- **Messages**: Real-time messaging within conversations
- **REST API**: Full REST API with Django REST Framework
- **Authentication**: Built-in Django authentication system

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Conversations
- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `POST /api/conversations/{id}/add_participant/` - Add participant
- `POST /api/conversations/{id}/remove_participant/` - Remove participant

### Messages
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send a new message
- `GET /api/messages/by_conversation/?conversation_id={id}` - Get messages by conversation

## Database Schema

### User Model
- `user_id` (UUID, Primary Key)
- `first_name` (VARCHAR, NOT NULL)
- `last_name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, UNIQUE, NOT NULL)
- `phone_number` (VARCHAR, NULL)
- `role` (ENUM: 'guest', 'host', 'admin', NOT NULL)
- `created_at` (TIMESTAMP)

### Conversation Model
- `conversation_id` (UUID, Primary Key)
- `participants` (Many-to-Many with User)
- `created_at` (TIMESTAMP)

### Message Model
- `message_id` (UUID, Primary Key)
- `sender` (Foreign Key to User)
- `conversation` (Foreign Key to Conversation)
- `message_body` (TEXT, NOT NULL)
- `sent_at` (TIMESTAMP)

## Usage

1. Register users through the API or Django admin
2. Create conversations by adding participants
3. Send messages within conversations
4. Use the REST API to integrate with frontend applications
