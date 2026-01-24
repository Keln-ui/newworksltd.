import os
import django
import sys
from django.test import Client

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from django.contrib.auth.models import User

def verify_admin_link():
    # 1. Setup Data
    superuser_name = 'verify_admin'
    superuser_pass = 'adminpass'
    normal_name = 'verify_normal'
    normal_pass = 'normalpass'

    User.objects.filter(username__in=[superuser_name, normal_name]).delete()
    
    User.objects.create_superuser(username=superuser_name, email='admin@test.com', password=superuser_pass)
    User.objects.create_user(username=normal_name, email='normal@test.com', password=normal_pass)

    c = Client()

    # 2. Test Superuser
    print("\n--- Testing Superuser ---")
    c.login(username=superuser_name, password=superuser_pass)
    response = c.get('/') # Home page
    if b'Admin Dashboard' in response.content:
        print("SUCCESS: Admin link visible for superuser.")
    else:
        print("FAILURE: Admin link NOT visible for superuser.")
    c.logout()

    # 3. Test Normal User
    print("\n--- Testing Normal User ---")
    c.login(username=normal_name, password=normal_pass)
    response = c.get('/')
    if b'Admin Dashboard' not in response.content:
        print("SUCCESS: Admin link hidden for normal user.")
    else:
        print("FAILURE: Admin link visible for normal user (Should be hidden).")
    c.logout()
    
    # 4. Test Anonymous User
    print("\n--- Testing Anonymous User ---")
    response = c.get('/')
    if b'Admin Dashboard' not in response.content:
        print("SUCCESS: Admin link hidden for anonymous user.")
    else:
        print("FAILURE: Admin link visible for anonymous user.")

if __name__ == '__main__':
    verify_admin_link()
