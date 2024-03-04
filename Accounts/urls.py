from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.home, name='home'),
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('reset/<int:token>/', views.user_reset, name='reset'),
    path('forget/', views.forget_password, name='forget_pass'),
    path('logout/', views.user_logout, name='logout'),
    path('verify/', views.verify_acc, name='verify'),

]