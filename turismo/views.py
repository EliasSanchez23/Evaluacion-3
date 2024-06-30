from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import InicioSesionForm, CrearUsuarioForm
import logging
from .models import Usuario

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'turismo/index.html'

def createuser(request):
    return render(request, 'turismo/createuser.html')

def nuestroservicios(request):
    return render(request, 'turismo/nuestroservicios.html')

def quienesomos(request):
    return render(request, 'turismo/quienesomos.html')
    

def productos(request):
    return render(request, 'turismo/productos.html')
    
def pagar(request):
    return render(request, 'turismo/pagar.html')

def procesar_formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        numero = request.POST.get('numero')
    
        try:
            nuevo_usuario = Usuario.objects.create_user(nombre=nombre, apellido=apellido, correo=correo, password=password, numero=numero)
            nuevo_usuario.save()
            return render(request, 'turismo/login.html')
        except IntegrityError:
            return render(request, 'turismo/createuser.html', {'error': 'El usuario ya existe.'})

    return render(request, 'turismo/index.html')

class IniciarSesion(FormView):
    template_name = 'turismo/login.html'
    form_class = InicioSesionForm
    success_url = reverse_lazy('turismo:index')

    def form_valid(self, form):
        correo = form.cleaned_data['correo']
        password = form.cleaned_data['password']

        user = authenticate(request=self.request, username=correo, password=password)

        if user is None:
            user = authenticate(request=self.request, username=correo, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Credenciales inválidas. Por favor, verifica tus datos.')
            return self.form_invalid(form)

        return super().form_valid(form)
    
def procesar_formulario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Intenta guardar el usuario
                return redirect('ruta_de_redireccion')  # Redirige a alguna página de éxito
            except IntegrityError:
                # Manejar el error de unicidad de correo
                return render(request, 'turismo/createuser.html', {'error': 'El correo electrónico ya está en uso.'})
        else:
            # Manejar el caso donde el formulario no es válido
            return render(request, 'turismo/createuser.html', {'form': form})
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'turismo/createuser.html', {'form': form})