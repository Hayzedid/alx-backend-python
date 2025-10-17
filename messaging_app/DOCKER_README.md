# Docker Setup for Messaging App

This document provides comprehensive instructions for containerizing and running the Django messaging application using Docker and Docker Compose.

## 🐳 Docker Configuration Overview

### Architecture
- **Web Service**: Django application running on Python 3.10
- **Database Service**: MySQL 8.0 with persistent storage
- **Network**: Custom bridge network for service communication
- **Volumes**: Persistent data storage for MySQL and static files

## 📋 Prerequisites

### Required Software
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for cloning repository)

### Installation Links
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Docker Engine (Linux)**: https://docs.docker.com/engine/install/

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables (optional)
nano .env
```

### 2. Build and Run
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### 3. Access Application
- **Web Application**: http://localhost:8000
- **MySQL Database**: localhost:3306

## 📁 Project Structure

```
messaging_app/
├── Dockerfile                 # Web service container definition
├── docker-compose.yml        # Multi-container orchestration
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── manage.py                # Django management script
├── messaging_app/           # Django project directory
│   ├── settings.py         # Django settings (env-aware)
│   ├── urls.py
│   └── wsgi.py
└── chats/                   # Django app directory
```

## 🔧 Configuration Files

### Dockerfile Features
- **Base Image**: Python 3.10 official image
- **System Dependencies**: MySQL client libraries
- **Python Dependencies**: Installed from requirements.txt
- **Static Files**: Collected automatically
- **Health Checks**: Database connection waiting
- **Production Server**: Gunicorn WSGI server
- **Port Exposure**: 8000 (configurable)

### Docker Compose Services

#### Web Service (`web`)
- **Build**: Local Dockerfile
- **Port Mapping**: 8000:8000
- **Environment**: Django configuration via .env
- **Volumes**: Source code and static files
- **Dependencies**: Waits for healthy database
- **Network**: messaging_network

#### Database Service (`db`)
- **Image**: MySQL 8.0 official image
- **Port Mapping**: 3306:3306
- **Environment**: Database credentials via .env
- **Volume**: Persistent MySQL data storage
- **Health Check**: MySQL ping verification
- **Network**: messaging_network

## 🌍 Environment Variables

### Django Configuration
```env
DEBUG=True                    # Development mode
SECRET_KEY=your-secret-key   # Django secret key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0  # Allowed hosts
```

### MySQL Configuration
```env
MYSQL_DATABASE=messaging_app_db      # Database name
MYSQL_USER=messaging_user            # Database user
MYSQL_PASSWORD=secure_password       # User password
MYSQL_ROOT_PASSWORD=root_password    # Root password
```

### Database Connection
```env
DB_ENGINE=django.db.backends.mysql   # Database backend
DB_NAME=messaging_app_db             # Database name
DB_USER=messaging_user               # Connection user
DB_PASSWORD=secure_password          # Connection password
DB_HOST=db                          # Service hostname
DB_PORT=3306                        # Database port
```

## 📊 Volume Management

### Persistent Volumes
- **mysql_data**: Database files persistence
- **static_volume**: Django static files storage

### Volume Commands
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect messaging_app_mysql_data

# Remove volumes (⚠️ DATA LOSS)
docker-compose down -v
```

## 🔨 Docker Commands

### Basic Operations
```bash
# Build services
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f web
```

### Development Commands
```bash
# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Access container shell
docker-compose exec web bash
docker-compose exec db mysql -u root -p

# Restart specific service
docker-compose restart web
```

### Database Operations
```bash
# Access MySQL shell
docker-compose exec db mysql -u messaging_user -p messaging_app_db

# Backup database
docker-compose exec db mysqldump -u root -p messaging_app_db > backup.sql

# Restore database
docker-compose exec -T db mysql -u root -p messaging_app_db < backup.sql
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database health
docker-compose ps

# View database logs
docker-compose logs db

# Restart database service
docker-compose restart db
```

#### Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3306

# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use different host port
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Reset Docker permissions
docker-compose down
docker system prune -f
```

#### Build Failures
```bash
# Clean build
docker-compose build --no-cache

# Remove old images
docker image prune -f

# Complete cleanup
docker system prune -a -f
```

### Health Checks
```bash
# Check service status
docker-compose ps

# Test web service
curl http://localhost:8000/

# Test database connection
docker-compose exec web python manage.py dbshell
```

## 🔒 Security Considerations

### Production Deployment
1. **Environment Variables**: Use secure, unique passwords
2. **Secret Key**: Generate new Django secret key
3. **Debug Mode**: Set DEBUG=False in production
4. **Allowed Hosts**: Restrict to actual domain names
5. **Database Access**: Limit MySQL user permissions
6. **SSL/TLS**: Configure HTTPS in production

### Environment Security
```bash
# Generate secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Secure file permissions
chmod 600 .env
```

## 📈 Performance Optimization

### Production Settings
```yaml
# docker-compose.prod.yml
services:
  web:
    command: gunicorn --workers 4 --bind 0.0.0.0:8000 messaging_app.wsgi:application
    environment:
      - DEBUG=False
```

### Database Optimization
```yaml
services:
  db:
    command: --innodb-buffer-pool-size=256M --max-connections=200
```

## 🧪 Testing

### Run Tests in Container
```bash
# Run Django tests
docker-compose exec web python manage.py test

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **MySQL Docker Hub**: https://hub.docker.com/_/mysql

## ✅ Verification Checklist

- [ ] Docker and Docker Compose installed
- [ ] .env file configured with secure credentials
- [ ] Services build without errors
- [ ] Web application accessible at http://localhost:8000
- [ ] Database connection successful
- [ ] Django migrations applied
- [ ] Static files served correctly
- [ ] Volumes persist data across restarts

## 🎯 Next Steps

1. **Development**: Start building your messaging features
2. **Testing**: Implement comprehensive test suite
3. **CI/CD**: Set up automated deployment pipeline
4. **Monitoring**: Add logging and monitoring solutions
5. **Scaling**: Consider Kubernetes for production scaling

---

**Status**: ✅ Docker containerization complete and ready for development!
