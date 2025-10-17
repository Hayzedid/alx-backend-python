# Use Python 3.10 as base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose port 8000
EXPOSE 8000

# Create a script to wait for database and run migrations
RUN echo '#!/bin/bash\n\
echo "Waiting for database..."\n\
while ! nc -z db 3306; do\n\
  sleep 0.1\n\
done\n\
echo "Database started"\n\
\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
\n\
echo "Creating superuser if not exists..."\n\
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='\''admin@example.com'\'').exists() or User.objects.create_superuser('\''admin'\'', '\''admin@example.com'\'', '\''admin123'\'')" || true\n\
\n\
echo "Starting server..."\n\
exec "$@"' > /app/entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "messaging_app.wsgi:application"]
