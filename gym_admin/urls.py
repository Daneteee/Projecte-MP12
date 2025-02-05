from gym_app.views import home
from django.urls import path
from . import views

app_name = 'gym_admin'

urlpatterns = [
    path('', home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),  
    path('users/delete/', views.delete_user, name='delete_user'), 

]