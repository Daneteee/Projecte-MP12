from django import forms
from .models import Routine
from django.core.exceptions import ValidationError

# Formulari per la rutina
class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'exercises', 'duration', 'recommendations']
        
        labels = {
            'name': 'Nom',
            'exercises': 'Exercicis',
            'duration': 'Duració (minuts)',
            'recommendations': 'Recomanacions'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[fields].label})
            
    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            if Routine.objects.filter(name=name).exists():
                raise ValidationError("Ja hi ha una rutina amb aquest nom.")
        except Exception as e:
            raise ValidationError("Ja hi ha una rutina amb aquest nom.")
        return name
