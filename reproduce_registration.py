import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\Misheck72\Desktop\new works1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_store.settings') # Speculating settings name, need to verify
# I'll try to find settings name first or assume 'store.settings' or similar. 
# Better to look at manage.py or similar to find settings module.

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Profile

def test_registration():
    print("Testing registration...")
    c = Client()
    
    # Clean up test user if exists
    email = "testuser@example.com"
    if User.objects.filter(email=email).exists():
        User.objects.get(email=email).delete()
        print(f"Deleted existing user {email}")

    response = c.post('/accounts/register/', {
        'first_name': 'Test',
        'last_name': 'User',
        'email': email,
        'phone': '1234567890',
        'password': 'password123',
        'confirm_password': 'password123'
    })

    if response.status_code == 302:
        print("Registration redirect success (likely successful)")
    else:
        print(f"Registration returned status {response.status_code}")
        # print(response.content.decode())

    # Verify User
    if User.objects.filter(email=email).exists():
        print("User created successfully.")
        user = User.objects.get(email=email)
        print(f"Username: {user.username}")
        
        # Verify Profile
        if hasattr(user, 'profile'):
            print(f"Profile exists. Phone: {user.profile.phone}")
            if user.profile.phone == '1234567890':
                print("Phone number saved correctly.")
            else:
                print(f"FAIL: Phone number mismatch. Expected 1234567890, got {user.profile.phone}")
        else:
            print("FAIL: Profile does not exist for user.")
    else:
        print("FAIL: User was not created.")

if __name__ == '__main__':
    try:
        test_registration()
    except Exception as e:
        print(f"An error occurred: {e}")
