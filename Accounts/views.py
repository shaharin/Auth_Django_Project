from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
import random


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'cv/index.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        '''if user.is_superuser:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")'''
        if user is not None:
            prof = Profile.objects.get(user=user)
            if prof.is_verified == True:
                login(request, user)
                #messages.success(request, "You have been logged in")
                return redirect("index")

            else:
                messages.success(request, "Please verify your account")
        else:
            messages.success(request, "There was an problem logging in! Please try again")
            return redirect("login")
    return render(request, 'accounts/login.html', {})


def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')

        if password == password1:
            if User.objects.filter(username=name).exists():
                messages.success(request, "Username already exist try another")
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.set_password(password)
                user.save()
                otp = random.randint(0000, 9999)
                prof = Profile(user=user, token=otp)
                prof.save()
                subject = 'Your Account Verification OTP'
                message = f'Hi here is your account verification OTP: {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient = [email]
                send_mail(subject, message, email_from, recipient)
                messages.success(request, "to create account check your email for verify")
                return redirect('verify')
        else:
            messages.success(request, "Password don't matched")
    return render(request, 'accounts/register.html')


def user_reset(request, token):
    prof = Profile.objects.get(token=token)
    if request.method == 'POST':
        password1 = request.POST.get('new_password')
        password2 = request.POST.get('confirm_new_password')
        user_id = request.POST.get('user_id')
        if password1 == password2:
            user = User.objects.get(id=user_id)
            if user_id is not None:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password reset successfully")
                return redirect('login')
            else:
                messages.success(request, "No user id found")
                return redirect(f'/reset/{token}/')
        else:
            messages.success(request, "Password not match")
            return redirect(f'/reset/{token}/')
    return render(request, 'accounts/resetpass.html', locals())

def forget_password(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('username')
            if not User.objects.filter(username=name).first():
                messages.success(request, "User not found")
                return redirect('forget_pass')
            else:
                user = User.objects.get(username=name)
                prof = Profile.objects.get(user=user)
                subject = 'Your forget password link'
                message = f'Hi click on the link to reset your password http://127.0.0.1:8000/reset/{prof.token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient = [user.email]
                send_mail(subject, message, email_from, recipient)
                messages.success(request, "to reset password check your email for verify")
                return redirect('forget_pass')
    except:
        messages.success(request, "Please try again")
        return redirect('forget_pass')
    return render(request, 'accounts/forgotpass.html')
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect("login")
def verify_acc(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            prof = Profile.objects.get(token=otp)
            prof.is_verified = True
            prof.save()
            messages.success(request, "You Profile verified successfully")
            return redirect('login')
        except:
            messages.success(request, "Wrong OTP")
            return redirect('verify')
    return render(request, 'accounts/verify.html')

