# authapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import UserProfile  # Import the UserProfile model

def register_view(request):
    if request.method == 'POST':
        # Get user input from the registration form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username or email already exist
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            # Handle duplicate username or email errors
            return redirect('register')  # Redirect back to the registration page with an error message if needed

        # Create a new user using Django's User model
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create a UserProfile associated with the user
        UserProfile.objects.create(user=user, name=username)
        
        # Log in the user after registration
        login(request, user)
        
        # Redirect to the profile page after successful registration
        return redirect('profile')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
