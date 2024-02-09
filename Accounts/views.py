from django.shortcuts import render

# Create your views here.

def user_login(request):
    return render(request, 'accounts/login.html')

def user_register(request):
    return render(request, 'accounts/register.html')

def user_reset(request):
    return render(request, 'accounts/resetpass.html')
