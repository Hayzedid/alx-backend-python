#!/bin/bash

# Docker Setup Script for Messaging App
# This script automates the Docker setup process

echo "🐳 Docker Setup for Messaging App"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update the credentials if needed."
else
    echo "✅ .env file already exists"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker images built successfully"
else
    echo "❌ Failed to build Docker images"
    exit 1
fi

echo "🚀 Starting services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Services started successfully"
else
    echo "❌ Failed to start services"
    exit 1
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

# Test web service
echo "🌐 Testing web service..."
if curl -f http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Web service is responding"
else
    echo "⚠️  Web service might still be starting up"
fi

echo ""
echo "🎉 Docker setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Access your application at: http://localhost:8000"
echo "2. View logs: docker-compose logs -f"
echo "3. Stop services: docker-compose down"
echo "4. Run migrations: docker-compose exec web python manage.py migrate"
echo "5. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo ""
echo "📚 For more information, see DOCKER_README.md"
