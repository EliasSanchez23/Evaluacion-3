# turismo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('correo', 'password', 'nombre', 'apellido', 'numero')

class InicioSesionForm(forms.Form):
    correo = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)



