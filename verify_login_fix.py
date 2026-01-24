import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

username_input = '0757924041'
password_input = 'admin123'

print(f"Attempting to authenticate with: {username_input} / {password_input}")

try:
    user = authenticate(username=username_input, password=password_input)
    if user:
        print(f"Authentication SUCCESS! Logged in as: {user.username} (ID: {user.id})")
    else:
        print("Authentication FAILED (Invalid credentials or logic error)")
except Exception as e:
    print(f"Authentication ERROR (Still crashing?): {e}")
    import traceback
    traceback.print_exc()
