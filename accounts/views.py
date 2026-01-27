from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Save phone number to profile
            # Profile is created by signal, so we get it and update it
            if hasattr(user, 'profile'):
                user.profile.phone = form.cleaned_data.get('phone')
                user.profile.save()
                
            # Specify the backend since multiple are configured
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Check if profile exists; signal should have created it, but safe to check
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
            
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

def custom_password_reset(request):
    error = None
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone', '').strip()
        
        # Try to find user by email or phone
        user = None
        if '@' in email_or_phone:
            # It's an email
            try:
                user = User.objects.get(email=email_or_phone)
            except User.DoesNotExist:
                error = "No account found with this email address."
        else:
            # It's a phone number
            profile = Profile.objects.filter(phone=email_or_phone).first()
            if profile:
                user = profile.user
            else:
                error = "No account found with this phone number."
        
        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = request.build_absolute_uri(
                f'/accounts/reset/{uid}/{token}/'
            )
            
            # Send email if user has email
            if user.email:
                try:
                    send_mail(
                        'Password Reset Request',
                        f'Click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    # If email fails, still show success message for security
                    pass
            
            # For phone, you would integrate SMS service here
            # For now, we'll just redirect to done page
            
            return redirect('password_reset_done')
    
    return render(request, 'accounts/password_reset.html', {'error': error})
