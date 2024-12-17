from gym_trainer.models import Schedule
from .models import Subscription
from django import forms

class SubscriptionForm(forms.Form):
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all(), empty_label="Selecciona una suscripción")


class EnrollForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())