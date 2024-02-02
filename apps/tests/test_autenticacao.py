from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class TestAutenticacao(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'temporario@teste.com', 'temporario')
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        resultado = self.client.post(url, data=usuario, follow=True)
        return resultado


    def test_index_autenticado(self):
        resultado = self.autentica()
        self.assertIn('Logout', resultado.content.decode('utf-8'))

    def test_login_com_senha_errada(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'senhaerrada'}
        resultado = self.client.post(url, data=usuario, follow=True)
        self.assertIn(
            'Erro ao tentar autenticar usuário, verifique sua senha',
            resultado.content.decode('utf-8'))
        
    def test_login_verifica_autenticacao(self):
        url = reverse('clientes_lista')
        resultado = self.client.get(url, follow=True)
        self.assertIn('Você não está autenticado!', resultado.content.decode('utf-8'))

    def test_logout(self):
        self.autentica()
        url = reverse('imoveis_logout')
        resultado = self.client.get(url, follow=True)
        self.assertIn('Logout efetuado com sucesso.', resultado.content.decode('utf-8'))