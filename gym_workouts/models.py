from django.contrib.auth.models import User
from gym_trainer.models import Schedule, Routine
from django.conf import settings
from django.db import models

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('1_routine', '1 rutina a la setmana - 15€ al mes'),
        ('3_routines', '3 rutines a la setmana - 30€ al mes'),
        ('unlimited', 'Rutines il·limitades - 50€ al mes'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES)
    price = models.FloatField()
    
    # Les rutines màximes, serà "None" si el pla és il·limitat
    max_routines = models.PositiveIntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.get_name_display()} - {self.price}€"