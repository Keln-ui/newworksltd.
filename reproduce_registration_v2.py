import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\Misheck72\Desktop\new works1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Profile

def test_registration():
    print("Testing registration...")
    c = Client()
    
    email = "testuser@example.com"
    # Clean up
    if User.objects.filter(email=email).exists():
        User.objects.filter(email=email).delete()
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
        print(f"Registration status: {response.status_code}")
        if 'form' in response.context:
            print("Form errors:", response.context['form'].errors)

    # Verify
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        print(f"User created. Username: {user.username}")
        
        if hasattr(user, 'profile'):
            print(f"Profile exists. Phone: {user.profile.phone}")
            if user.profile.phone == '1234567890':
                print("SUCCESS: Registration logic verified!")
            else:
                print(f"FAIL: Phone number mismatch. Got {user.profile.phone}")
        else:
            print("FAIL: Profile does not exist.")
    else:
        print("FAIL: User not created.")

if __name__ == '__main__':
    test_registration()
