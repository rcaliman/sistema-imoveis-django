from django.test import TestCase
from django.contrib.auth.models import User
from apps.imoveis.models import Locador
from apps.imoveis.forms import FormLocador
from django.urls import reverse

class TesteLocador(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'teste@teste.com', 'temporario')
        self.data_locador = {
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

    def test_model_locador_retorna_nome_como__str__(self):
        locador = Locador(**self.data_locador)
        self.assertEqual(str(locador), 'John Doe')

    def test_view_locadores_lista(self):
        self.autentica()
        url = reverse('locadores_lista')
        resposta = self.client.get(url)
        self.assertNotIn('Você não está autenticado!', resposta.content.decode('utf-8'))
        self.assertEqual(resposta.status_code, 200)

    def test_view_locadores_lista_inserir(self):
        self.autentica()
        url = reverse('locadores_lista')
        resposta = self.client.post(url, data=self.data_locador, follow=True)
        self.assertIn('locador adicionado com sucesso', resposta.content.decode('utf-8'))

    def test_view_locadores_lista_erro_ao_inserir(self):
        self.autentica()
        url = reverse('locadores_lista')
        self.data_locador['data_nascimento'] = '2023-30-30'
        resposta = self.client.post(url, data=self.data_locador, follow=True)
        self.assertIn('erro ao adicionar locador', resposta.content.decode('utf-8'))

    def test_view_locadores_lista_update(self):
        self.autentica()
        url = reverse('locadores_lista')
        self.client.post(url, data=self.data_locador, follow=True)
        self.data_locador['id'] = 1
        self.data_locador['nome'] = 'Joe Doe'
        resposta = self.client.post(url, data=self.data_locador, follow=True)
        self.assertIn('locador atualizado com sucesso', resposta.content.decode('utf-8'))

    def test_view_formulario_locador_inserir(self):
        self.autentica()
        form = FormLocador()
        url = reverse('locador_inserir')
        resposta = self.client.get(url, data={'form': form})
        self.assertIn('<form', resposta.content.decode('utf-8'))

    def test_view_locador_alterar(self):
        self.autentica()
        url = reverse('locadores_lista')
        self.client.post(url, data=self.data_locador, follow=True)
        url = reverse('locador_alterar', kwargs={'id_do_registro': 1})
        form = FormLocador()
        resposta = self.client.get(url, data={'form': form})
        self.assertIn(
            '<input type="text" name="nome" value="John Doe"', resposta.content.decode('utf-8')
        )

    def test_view_locador_apagar(self):
        self.autentica()
        url = reverse('locadores_lista')
        self.client.post(url, data=self.data_locador, follow=True)
        url = reverse('locador_apagar', kwargs={'id_do_registro': 1})
        resposta = self.client.get(url, follow=True)
        self.assertIn('locador apagado com sucesso', resposta.content.decode('utf-8'))

        



        