#!/usr/bin/env python
"""
Setup script for Django Signals ORM Project
This script helps set up the project for development and testing.
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Django Signals ORM Project")
    print("=" * 50)
    
    # Change to the messaging_app directory
    project_dir = os.path.join(os.path.dirname(__file__), 'messaging_app')
    if not os.path.exists(project_dir):
        print(f"❌ Project directory not found: {project_dir}")
        sys.exit(1)
    
    os.chdir(project_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Setup steps
    steps = [
        ("python manage.py makemigrations messaging", "Creating migrations for messaging app"),
        ("python manage.py makemigrations", "Creating all migrations"),
        ("python manage.py migrate", "Applying database migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    success_count = 0
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Setup Results: {success_count}/{len(steps)} steps completed successfully")
    
    if success_count == len(steps):
        print("\n🎉 Project setup completed successfully!")
        print("\nNext steps:")
        print("1. Create a superuser: python manage.py createsuperuser")
        print("2. Run the development server: python manage.py runserver")
        print("3. Run tests: python manage.py test messaging")
    else:
        print("\n⚠️  Some setup steps failed. Please check the errors above.")


if __name__ == "__main__":
    main()
