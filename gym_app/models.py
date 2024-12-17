from django.contrib.auth.models import AbstractUser 
from django.db import models
from gym_workouts.models import Subscription

class User(AbstractUser ):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    subscription = models.CharField(max_length=100, null=True, blank=True)  # O ajusta según sea necesario

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    REQUIRED_FIELDS = ['role']
    USERNAME_FIELD = 'email'