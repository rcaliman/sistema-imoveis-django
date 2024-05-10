from django.test import TestCase
from django.contrib.auth.models import User
from apps.imoveis.models.energia import Energia
from apps.imoveis.forms.energia import FormEnergia
from django.urls import reverse

class TestaEnergia(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'teste@teste.com', 'temporario')

        self.data_energia1 = {
            'data': '2023-01-01',
            'relogio_1': 1100,
            'relogio_2': 2100,
            'relogio_3': 3100,
            'valor_kwh': 0.5555,
            'valor_conta': 250.0,
        }
        self.energia1_pk = Energia.objects.create(**self.data_energia1).pk

        self.data_energia2 = {
            'data': '2023-02-01',
            'relogio_1': 1200,
            'relogio_2': 2200,
            'relogio_3': 3200,
            'valor_kwh': 0.5555,
            'valor_conta': 260.0,
        }
        self.energia2_pk = Energia.objects.create(**self.data_energia2).pk

        self.data_energia3 = {
            'data': '2023-03-01',
            'relogio_1': 1300,
            'relogio_2': 2300,
            'relogio_3': 3300,
            'valor_kwh': 0.5555,
            'valor_conta': 270.0,
        }
        self.energia3_pk = Energia.objects.create(**self.data_energia3).pk

        self.data_energia4 = {
            'data': '2023-04-01',
            'relogio_1': 1400,
            'relogio_2': 2400,
            'relogio_3': 3400,
            'valor_kwh': 0.5555,
            'valor_conta': 280.0,
        }
        self.energia4_pk = Energia.objects.create(**self.data_energia4).pk

        self.data_energia5 = {
            'data': '2023-05-01',
            'relogio_1': 1500,
            'relogio_2': 2500,
            'relogio_3': 3500,
            'valor_kwh': 0.5555,
            'valor_conta': 290.0,
        }

        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def test_model_energia_retornando_data_como__str__(self):
        energia = Energia(**self.data_energia1)
        self.assertEqual(str(energia), '2023-01-01')

    def test_view_energia_lista(self):
        self.autentica()
        url = reverse('energia_lista')
        resposta = self.client.get(url)
        self.assertIn('01/02/2023', resposta.content.decode('utf-8'))

    def test_view_energia_lista_vazia(self):
        self.autentica()
        url = reverse('energia_lista')
        Energia.objects.get(id=self.energia1_pk).delete()
        Energia.objects.get(id=self.energia2_pk).delete()
        Energia.objects.get(id=self.energia3_pk).delete()
        Energia.objects.get(id=self.energia4_pk).delete()
        resposta = self.client.get(url)
        self.assertNotIn('01/02/2023', resposta.content.decode('utf-8'))


    def test_view_energia_lista_update(self):
        self.autentica()
        self.data_energia4['id'] = self.energia4_pk
        self.data_energia4['data'] = '2023-04-02'
        url = reverse('energia_lista')
        resposta = self.client.post(url, data=self.data_energia4, follow=True)
        self.assertIn('Registro atualizado com sucesso.', resposta.content.decode('utf-8'))

    def test_view_energia_lista_inserindo_novo_registro(self):
        self.autentica()
        url = reverse('energia_lista')
        resposta = self.client.post(url, data=self.data_energia5, follow=True)
        self.assertIn('Novo registro adicionado com sucesso.', resposta.content.decode('utf-8'))

    def test_view_energia_inserir_formulario(self):
        self.autentica()
        form = FormEnergia()
        url = reverse('energia_inserir')
        resposta = self.client.get(url, {'form': form})
        self.assertIn('input type', resposta.content.decode('utf-8'))

    def test_view_energia_editar(self):
        self.autentica()
        url = reverse('energia_editar', kwargs={'energia_id': self.energia1_pk})
        self.data_energia1['id'] = '1'
        resposta = self.client.get(url, data=self.data_energia1)
        self.assertIn('2023-01-01', resposta.content.decode('utf-8'))
