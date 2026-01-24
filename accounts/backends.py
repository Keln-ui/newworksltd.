from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
        
        try:
            # Check if the username matches username, email, or profile phone
            # Use filter() instead of get() to handle potential duplicates
            users = User.objects.filter(
                Q(username=username) | 
                Q(email=username) | 
                Q(profile__phone=username)
            )
            
            for user in users:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            return None
            
        except User.DoesNotExist:
            return None
