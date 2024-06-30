from django.urls import path
from . import views
from .views import IniciarSesion, IndexView

app_name = 'turismo'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', IniciarSesion.as_view(), name='login'),
    path('createuser/', views.createuser, name='createuser'),
    path('nuestroservicios/', views.nuestroservicios, name='nuestroservicios'),
    path('quienesomos/', views.quienesomos, name='quienesomos'),
    path('procesar/', views.procesar_formulario, name='procesar_formulario'),
    path('productos/',views.productos, name='productos'),
    path('pagar/', views.pagar, name='pagar')
]
