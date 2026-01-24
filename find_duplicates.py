import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_works_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()
username_input = '0757924041'

print(f"Searching for users matching: {username_input}")

users = User.objects.filter(
    Q(username=username_input) | 
    Q(email=username_input) | 
    Q(profile__phone=username_input)
)

print(f"Found {users.count()} users:")
for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Phone: {user.profile.phone if hasattr(user, 'profile') else 'No Profile'}")
