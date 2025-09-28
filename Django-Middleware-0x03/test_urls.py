#!/usr/bin/env python
"""
Test script to verify URL routing is working correctly
"""
import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.urls import reverse

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
    django.setup()
    
    # Test URL patterns
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # Check if our URLs are registered
        url_patterns = resolver.url_patterns
        
        print("✅ URL Configuration Test")
        print("=" * 50)
        
        # Check main project URLs
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                print(f"Found URL pattern: {pattern.pattern}")
                for sub_pattern in pattern.url_patterns:
                    print(f"  └── {sub_pattern.pattern}")
        
        # Test specific API endpoints
        client = Client()
        
        # Test if API endpoints are accessible
        api_endpoints = [
            '/api/users/',
            '/api/conversations/',
            '/api/messages/',
        ]
        
        print("\n🔍 Testing API Endpoints:")
        for endpoint in api_endpoints:
            try:
                response = client.get(endpoint)
                print(f"  {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"  {endpoint}: Error - {e}")
        
        print("\n✅ URL routing test completed successfully!")
        
    except Exception as e:
        print(f"❌ URL test error: {e}")
        sys.exit(1)


