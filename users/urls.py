from .views import *
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('user/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('new-profile/', new_profile, name='new-profile'),
    path('logout/', user_logout, name='logout'),
    path('auth/', auth, name='auth'),
    path('', get_phone, name='get-phone'),
    path('register/', register, name='register'),
    path('ent/', entrance, name='entrance')
]