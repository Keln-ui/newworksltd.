import os
import django
import sys
from django.test import Client

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

def verify_multi_login():
    # Setup Test User
    username = 'multi_login_user'
    email = 'multi@example.com'
    phone = '5551234567'
    password = 'multipassword'
    
    # Cleanup
    User.objects.filter(username=username).delete()
    
    # Create User using Django's create_user helper (handles password hashing)
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Create/Update Profile with phone
    # Note: create_user might trigger signal creating empty profile, check/update it
    if hasattr(user, 'profile'):
        user.profile.phone = phone
        user.profile.save()
    else:
        Profile.objects.create(user=user, phone=phone)
        
    print(f"User created: {username} | {email} | {phone}")

    c = Client()
    
    # 1. Login with Username
    print("\n--- Testing Login with Username ---")
    resp = c.post('/accounts/login/', {'username': username, 'password': password})
    if resp.status_code == 302: # Redirect on success
        print("SUCCESS: Logged in with Username")
    else:
        print(f"FAILURE: Could not login with Username. Status: {resp.status_code}")
        
    c.logout()

    # 2. Login with Email
    print("\n--- Testing Login with Email ---")
    resp = c.post('/accounts/login/', {'username': email, 'password': password})
    if resp.status_code == 302:
        print("SUCCESS: Logged in with Email")
    else:
        print(f"FAILURE: Could not login with Email. Status: {resp.status_code}")
        
    c.logout()

    # 3. Login with Phone
    print("\n--- Testing Login with Phone ---")
    resp = c.post('/accounts/login/', {'username': phone, 'password': password})
    if resp.status_code == 302:
        print("SUCCESS: Logged in with Phone")
    else:
        print(f"FAILURE: Could not login with Phone. Status: {resp.status_code}")

if __name__ == '__main__':
    try:
        verify_multi_login()
    except Exception as e:
        print(f"An error occurred: {e}")
