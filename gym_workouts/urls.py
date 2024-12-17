from gym_app.views import home
from django.urls import path
from . import views

app_name = 'gym_workouts'

urlpatterns = [
    path('', home, name='home'),
    path('select_subscription/', views.select_subscription, name='select_subscription'),
    path('workouts/', views.workouts, name='workouts'),
    path('enroll_user/', views.enroll_user, name='enroll_user'),
    path('leave_routine/', views.leave_routine, name='leave_routine'),
]