from django.db import models
from django.conf import settings

class Schedule(models.Model):
    routine = models.ForeignKey('gym_trainer.Routine', on_delete=models.CASCADE) 
    day = models.CharField(max_length=10, choices=[
        ('Dilluns', 'Dilluns'),
        ('Dimarts', 'Dimarts'),
        ('Dimecres', 'Dimecres'),
        ('Dijous', 'Dijous'),
        ('Divendres', 'Divendres'),
    ])
    time = models.TimeField()
    room = models.CharField(max_length=255, default="Sala Principal")
    
    enrollments = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_schedules', 
        blank=True, 
    )

    class Meta:
        unique_together = ('day', 'time', 'room')  

    def __str__(self):
        return f"{self.routine.name} - {self.day} a les {self.time}"

    # Contem el usuaris incrits
    def count_enrolled(self):
        return self.enrollments.count()

    # Comprovem el màxim d'usuaris inscrits
    def clean(self):
        if self.count_enrolled() >= 10:
            raise ValidationError("No es poden inscriure més de 10 persones a la rutina.")


class Routine(models.Model):
    trainer = models.ForeignKey(
        'gym_app.User', 
        on_delete=models.CASCADE,
        related_name="assigned_routines", 
    )
    name = models.CharField(max_length=255)
    exercises = models.TextField()
    duration = models.DurationField()
    recommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name