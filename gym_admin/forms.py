from django.core.exceptions import ValidationError
from gym_app.models import User
from django import forms

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
        widgets = {
            'role': forms.Select(choices=[
                ('trainer', 'Entrenador'),
                ('user', 'Usuario'),
                ('admin', 'Admin'),
                ('gerent', 'Gerent'),
            ]),
        }

    # Validem email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if email and User.objects.exclude(id=self.instance.id).filter(email=email).exists():
                raise ValidationError("Aquest correu ja está registrat.")
        except Exception as e:
            raise ValidationError("Aquest correu ja está registrat.")
        return email

    # Validem nom d'usuari
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            if username and User.objects.exclude(id=self.instance.id).filter(username=username).exists():
                raise ValidationError("Aquest nom d'usuari ja està agafat.")
        except Exception as e:
            raise ValidationError("Aquest nom d'usuari ja està agafat.")
        return username