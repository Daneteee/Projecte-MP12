from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afegim classes per  l'estil i plachefolders
        for fields in self.fields:
            self.fields[fields].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[fields].label})