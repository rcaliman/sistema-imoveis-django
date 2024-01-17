from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from apps.imoveis.forms import FormCliente
from apps.imoveis.models import Cliente
from django.contrib.auth import logout

class TestClientes(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'temporario@teste.com', 'temporario')
        self.cliente_data = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '11111111111',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
        }
        self.cliente_pk = Cliente.objects.create(**self.cliente_data).pk
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        resultado = self.client.post(url, data=usuario, follow=True)
        return resultado
    
    def test_clientes_lista(self):
        self.autentica()
        url = reverse('clientes_lista')
        resultado = self.client.get(url)
        self.assertIn('John Doe', resultado.content.decode("utf-8"))

    def test_clientes_adiciona_novo(self):
        self.autentica()
        url = reverse('clientes_lista')
        resultado = self.client.post(url, data=self.cliente_data, follow=True)
        self.assertIn('Novo cliente adicionado com sucesso.', resultado.content.decode("utf-8"))

    def test_clientes_erro_adiciona_novo(self):
        self.autentica()
        url = reverse('clientes_lista')
        del self.cliente_data['nome']
        resultado = self.client.post(url, data=self.cliente_data, follow=True)
        self.assertIn('Erro ao tentar adicionar novo cliente.', resultado.content.decode("utf-8"))

    def test_clientes_atualiza_cliente(self):
        self.autentica()
        url = reverse('clientes_lista')
        self.cliente_data['id'] = self.cliente_pk
        resultado = self.client.post(url, data=self.cliente_data, follow=True)
        self.assertIn('Cliente atualizado com sucesso.', resultado.content.decode("utf-8"))

    def test_clientes_erro_atualiza_cliente(self):
        self.autentica()
        url = reverse('clientes_lista')
        self.cliente_data['id'] = '5'
        resultado = self.client.post(url, data=self.cliente_data, follow=True)
        self.assertIn('Erro ao tentar atualizar cliente.', resultado.content.decode("utf-8"))

    def test_cliente_inserir(self):
        self.autentica()
        url = reverse('cliente_inserir')
        form = {'form': FormCliente}
        resultado = self.client.get(url, data=form)
        self.assertIn('form class="formulario', resultado.content.decode('utf-8'))

    def test_cliente_alterar(self):
        self.autentica()
        url = reverse('cliente_alterar', kwargs={'id_do_registro': 1})
        resultado = self.client.get(url)
        self.assertIn('John Doe', resultado.content.decode('utf-8'))

    def test_cliente_apagar(self):
        self.autentica()
        url = reverse('cliente_apagar', kwargs={'id_do_registro': self.cliente_pk})
        resultado = self.client.get(url, follow=True)
        self.assertIn('alert-success', resultado.content.decode('utf-8'))

    def test_cliente_erro_apagar(self):
        self.autentica()
        url = reverse('cliente_apagar', kwargs={'id_do_registro': 10})
        resultado = self.client.get(url, follow=True)
        self.assertIn('Erro ao tentar apagar cliente', resultado.content.decode('utf-8'))

    def test_model_cliente_returnando_nome_como__str__(self):
        cliente = Cliente(**self.cliente_data)
        self.assertEqual(str(cliente), 'John Doe')

        