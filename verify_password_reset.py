import os
import django
import sys
from django.test import Client

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from django.contrib.auth.models import User

def verify_password_reset():
    # Ensure test user exists
    user, created = User.objects.get_or_create(
        username='reset_test_user',
        email='reset@example.com',
        defaults={'password': 'originalpassword'}
    )
    if created:
        user.set_password('originalpassword')
        user.save()

    c = Client()
    
    # 1. Check Login Page for Link
    response = c.get('/accounts/login/')
    if b'Forgot Password?' in response.content:
        print("SUCCESS: 'Forgot Password?' link found on login page.")
    else:
        print("FAILURE: 'Forgot Password?' link NOT found.")

    # 2. Check Password Reset Page Load
    response = c.get('/accounts/password_reset/')
    if response.status_code == 200:
        print("SUCCESS: Password reset page loaded (200 OK).")
    else:
        print(f"FAILURE: Password reset page failed with status {response.status_code}")

    # 3. Submit Password Reset Request
    response = c.post('/accounts/password_reset/', {'email': 'reset@example.com'})
    if response.status_code == 302 and response.url == '/accounts/password_reset/done/':
        print("SUCCESS: Password reset request redirected to done page.")
    else:
        print(f"FAILURE: Password reset request failed. Status: {response.status_code}, URL: {getattr(response, 'url', 'N/A')}")
        if 'form' in response.context:
            print(f"Form Errors: {response.context['form'].errors}")

if __name__ == '__main__':
    verify_password_reset()
