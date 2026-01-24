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

def verify_profile_update():
    # 1. Setup Test User
    username = 'profile_test_user'
    password = 'profilepassword'
    email = 'profile@example.com'
    
    User.objects.filter(username=username).delete()
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Ensure profile exists (signal should handle it, but for safety in test setup)
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    c = Client()
    c.login(username=username, password=password)

    # 2. Check Profile Page Access
    print("\n--- Testing Profile Page Access ---")
    response = c.get('/accounts/profile/')
    if response.status_code == 200:
        print("SUCCESS: Profile page loaded.")
    else:
        print(f"FAILURE: Profile page failed to load. Status: {response.status_code}")
        return

    # 3. Update Profile Info
    print("\n--- Testing Profile Update ---")
    new_data = {
        'username': username,
        'email': 'new_email@example.com',
        'first_name': 'Profile',
        'last_name': 'Tester',
        'address': '123 Test St',
        'phone': '1112223333'
    }
    
    response = c.post('/accounts/profile/', new_data)
    
    if response.status_code == 302: # Redirect back to profile on success
        print("SUCCESS: Profile update redirect works.")
        
        # Verify DB
        user.refresh_from_db()
        print(f"Verified Email: {user.email}")
        print(f"Verified First Name: {user.first_name}")
        
        try:
            profile = user.profile
            print(f"Verified Phone: {profile.phone}")
            print(f"Verified Address: {profile.address}")
            
            if (user.email == 'new_email@example.com' and 
                user.first_name == 'Profile' and 
                profile.phone == '1112223333' and
                profile.address == '123 Test St'):
                print("SUCCESS: Database updated correctly.")
            else:
                print("FAILURE: Database values mismatch.")
        except Profile.DoesNotExist:
             print("FAILURE: Profile missing.")

    else:
        print(f"FAILURE: Profile update failed. Status: {response.status_code}")
        if 'u_form' in response.context:
            print(f"User Form Errors: {response.context['u_form'].errors}")
        if 'p_form' in response.context:
            print(f"Profile Form Errors: {response.context['p_form'].errors}")

if __name__ == '__main__':
    verify_profile_update()
