from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('reset/', views.user_reset, name='reset'),
    path('logout/', views.user_logout, name='logout'),

]