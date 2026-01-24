import os
import django
import sys
from django.conf import settings

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from django.urls import get_resolver

def verify_media_urls():
    print(f"DEBUG Setting: {settings.DEBUG}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    resolver = get_resolver()
    url_patterns = resolver.url_patterns
    
    media_served = False
    for pattern in url_patterns:
        # Check if one of the patterns handles MEDIA_URL
        # Django's static() helper creates a re_path that usually starts with ^media/
        if hasattr(pattern, 'pattern') and hasattr(pattern.pattern, 'regex'):
            regex = pattern.pattern.regex.pattern
            if settings.MEDIA_URL.lstrip('/') in regex:
                media_served = True
                print(f"Found media pattern: {regex}")
    
    if media_served:
        print("SUCCESS: Media URL pattern found in urlpatterns.")
    else:
        print("FAILURE: Media URL pattern NOT found.")

if __name__ == '__main__':
    verify_media_urls()
