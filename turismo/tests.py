from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            nombre='Test',
            apellido='User',
            correo='testuser@example.com',
            password='testpassword123',
            numero='123456789'
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.apellido, 'User')
        self.assertEqual(self.usuario.correo, 'testuser@example.com')
        self.assertTrue(self.usuario.check_password('testpassword123'))

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_user_url = reverse('turismo:createuser')
        self.login_url = reverse('turismo:login')
        self.index_url = reverse('turismo:index')
        self.nuestroservicios_url = reverse('turismo:nuestroservicios')
        self.quienesomos_url = reverse('turismo:quienesomos')
        self.procesar_formulario_url = reverse('turismo:procesar_formulario')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/index.html')

    def test_createuser_view(self):
        response = self.client.get(self.create_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/createuser.html')

    def test_nuestroservicios_view(self):
        response = self.client.get(self.nuestroservicios_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/nuestroservicios.html')

    def test_quienesomos_view(self):
        response = self.client.get(self.quienesomos_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/quienesomos.html')

    def test_procesar_formulario_view_get(self):
        response = self.client.get(self.procesar_formulario_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/index.html')

    def test_procesar_formulario_view_post(self):
        data = {
            'nombre': 'New',
            'apellido': 'User',
            'correo': 'newuser@example.com',
            'password': 'newpassword123',
            'numero': '987654321'
        }
        response = self.client.post(self.procesar_formulario_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/login.html')
        self.assertTrue(Usuario.objects.filter(correo='newuser@example.com').exists())

class IniciarSesionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('turismo:login')
        self.index_url = reverse('turismo:index')
        self.usuario = Usuario.objects.create_user(
            nombre='Existing',
            apellido='User',
            correo='existinguser@example.com',
            password='password123',
            numero='123456789'
        )

    def test_iniciar_sesion_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/login.html')

    def test_iniciar_sesion_view_post_valid(self):
        data = {
            'correo': 'existinguser@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.index_url)

    def test_iniciar_sesion_view_post_invalid(self):
        data = {
            'correo': 'wronguser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'turismo/login.html')
        self.assertContains(response, 'Credenciales inválidas. Por favor, verifica tus datos.')
