from django.test import TestCase
from django.contrib.auth.models import User
from apps.imoveis.models import Locatario
from apps.imoveis.forms import FormLocatario
from django.urls import reverse

class TesteLocatario(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'teste@teste.com', 'temporario')
        self.data_locatario = {
            'nome': 'John Doe',
            'cpf': '11111111111',
            'residencia': 'colatina',
            'estado_civil': 'casado',
            'data_nascimento': '1978-01-01',
            'telefone': '1111111111',
            'email': 'teste@teste.com',
        }
        return super().setUp(*args, **kwargs)
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def test_model_locatario_retorna_nome_como__str__(self):
        locatario = Locatario(**self.data_locatario)
        self.assertEqual(str(locatario), 'John Doe')

    def test_view_locatarios_lista(self):
        self.autentica()
        url = reverse('locatarios_lista')
        resposta = self.client.get(url)
        self.assertNotIn('Você não está autenticado!', resposta.content.decode('utf-8'))
        self.assertEqual(resposta.status_code, 200)

    def test_view_locatarios_lista_inserir(self):
        self.autentica()
        url = reverse('locatarios_lista')
        resposta = self.client.post(url, data=self.data_locatario, follow=True)
        self.assertIn('locatário adicionado com sucesso', resposta.content.decode('utf-8'))

    def test_view_locatarios_lista_erro_ao_inserir(self):
        self.autentica()
        url = reverse('locatarios_lista')
        self.data_locatario['data_nascimento'] = '2023-30-30'
        resposta = self.client.post(url, data=self.data_locatario, follow=True)
        self.assertIn('erro ao adicionar locatário', resposta.content.decode('utf-8'))

    def test_view_locatarios_lista_update(self):
        self.autentica()
        url = reverse('locatarios_lista')
        self.client.post(url, data=self.data_locatario, follow=True)
        self.data_locatario['id'] = 1
        self.data_locatario['nome'] = 'Joe Doe'
        resposta = self.client.post(url, data=self.data_locatario, follow=True)
        self.assertIn('locatário atualizado com sucesso', resposta.content.decode('utf-8'))

    def test_view_formulario_locatario_inserir(self):
        self.autentica()
        form = FormLocatario()
        url = reverse('locatario_inserir')
        resposta = self.client.get(url, data={'form': form})
        self.assertIn('<form', resposta.content.decode('utf-8'))

    def test_view_locatario_alterar(self):
        self.autentica()
        url = reverse('locatarios_lista')
        self.client.post(url, data=self.data_locatario, follow=True)
        url = reverse('locatario_alterar', kwargs={'id_do_registro': 1})
        form = FormLocatario()
        resposta = self.client.get(url, data={'form': form})
        self.assertIn(
            '<input type="text" name="nome" value="John Doe"', resposta.content.decode('utf-8')
        )

    def test_view_locatario_apagar(self):
        self.autentica()
        url = reverse('locatarios_lista')
        self.client.post(url, data=self.data_locatario, follow=True)
        url = reverse('locatario_apagar', kwargs={'id_do_registro': 1})
        resposta = self.client.get(url, follow=True)
        self.assertIn('locatário apagado com sucesso', resposta.content.decode('utf-8'))
        



        