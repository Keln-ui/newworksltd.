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

def verify_registration():
    # Clean up previous test user
    User.objects.filter(username='verify_user').delete()

    c = Client()
    response = c.post('/accounts/register/', {
        'username': 'verify_user',
        'first_name': 'Verify',
        'last_name': 'User',
        'email': 'verify@example.com',
        'phone': '9876543210',
        'password': 'verifypassword123',
        'confirm_password': 'verifypassword123'
    })

    print(f"Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")
    else:
        print("Form errors (if any):")
        # Trying to extract form errors from context if available
        if 'form' in response.context:
            print(response.context['form'].errors)

    # Check Database
    try:
        user = User.objects.get(username='verify_user')
        print(f"User created: {user.username}")
        print(f"First Name: {user.first_name}")
        print(f"Last Name: {user.last_name}")
        
        try:
            profile = user.profile
            print(f"Profile created: {profile}")
            print(f"Phone: {profile.phone}")
            
            if user.first_name == 'Verify' and user.last_name == 'User' and profile.phone == '9876543210':
                print("SUCCESS: Registration logic verified!")
            else:
                print("FAILURE: Data mismatch.")
        except Profile.DoesNotExist:
            print("FAILURE: Profile not created.")
            
    except User.DoesNotExist:
        print("FAILURE: User not created.")

if __name__ == '__main__':
    verify_registration()
