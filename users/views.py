from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to a different page after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
            username=user.username,
            email=user.email,
            password=form.cleaned_data.get('password1')  # Store hashed password if needed
            )
            auth_login(request, user)
            return redirect('home')  # Redirect to a different page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')




def add_transaction(request):
    # Logic to add a new transaction
    return render(request, 'add_transaction.html')

def view_transactions(request):
    # Logic to view all transactions
    return render(request, 'view_transactions.html')


# Create your views here.
