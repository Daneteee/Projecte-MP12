"""
URL configuration for gym_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gym_app.urls', namespace='gym_app')),
    path('gym_trainer/', include('gym_trainer.urls'), name='gym_trainer'),
    path('gym_admin/', include('gym_admin.urls'), name='gym_admin'),
    path('gym_gerent/', include('gym_gerent.urls'), name='gym_gerent'),
    path('gym_workouts/', include('gym_workouts.urls'), name='gym_workouts'),

]
