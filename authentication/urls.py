from django.urls import path
from .views import customlogin, customlogout, customregister
urlpatterns = [
    path('login/' , customlogin , name='login'),
    path('register/' , customregister , name='register'),
    path('logout/' , customlogout , name='logout'),
]
