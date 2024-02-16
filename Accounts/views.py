from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")
        else:
            messages.success(request, "There was an problem logging in! Please try again")
            return redirect("login")
    return render(request, 'accounts/login.html', {})


def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')

        if password == password1:
            if User.objects.filter(username=name).exists():
                messages.success(request, "Username already exist try another")
            user = User.objects.create_user(username=name, email=email, password=password)
            #user.set_password(password)
            user.save()
            messages.success(request, "Register successfully")
            return redirect('login')
        else:
            messages.success(request, "Password don't matched")
    return render(request, 'accounts/register.html')

def user_reset(request):
    return render(request, 'accounts/resetpass.html')

def home(request):
    return render(request, 'accounts/home.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect("login")
