from django.urls import path
from . import views

urlpatterns = [
    path('cv_save/', views.cv_save, name='cv_save'),
    path('index/', views.profile, name='index'),
    path('<int:id>/', views.resume, name='resume'),
    path('profile/<id>/', views.view_profile, name='profile'),


]
