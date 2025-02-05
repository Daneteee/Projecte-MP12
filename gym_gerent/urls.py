from django.urls import path
from . import views

app_name = 'gym_gerent'

urlpatterns = [
    path('users/', views.user_list, name='user_list'), 
]