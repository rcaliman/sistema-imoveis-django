from django.test import TestCase
from apps.imoveis.forms.recibos import FormRecibos
from apps.imoveis.models import Locador
from apps.imoveis.models import Imovel
from apps.imoveis.models import Cliente
from django.contrib.auth.models import User
from django.urls import reverse

class TesteRecibos(TestCase):
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
        self.data_cliente = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '11111111111',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
        }
        self.data_imovel = {
            'tipo': 'apartamento',
            'numero': '100',
            'local': 'galeria',
            'cliente': Cliente(**self.data_cliente).save(),
            'valor': 100.0,
            'complemento': 'teste de complemento',
            'observacao': 'teste de observacao',
            'dia': 10,
        }
        return super().setUp(*args, **kwargs)
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def test_locadores_lista(self):
        Locador(**self.data_locador).save()
        locadores = FormRecibos.choices_locadores()
        self.assertEqual([('John Doe', 'John Doe')], locadores)

    def test_codigos_imoveis(self):
        self.imovel1_pk = Imovel.objects.create(**self.data_imovel).pk
        self.imovel2_pk = Imovel.objects.create(**self.data_imovel).pk
        codigos_imoveis = FormRecibos.codigos_imoveis()
        self.assertEqual([(self.imovel1_pk, ''), (self.imovel2_pk, '')], codigos_imoveis)

    def test_imoveis_recibos(self):
        self.autentica()
        self.locador_pk = Locador.objects.create(**self.data_locador).pk
        locador = Locador.objects.get(id=self.locador_pk)
        self.cliente_pk = Cliente.objects.create(**self.data_cliente).pk
        self.data_imovel['cliente'] = Cliente.objects.get(id=self.cliente_pk)
        self.imovel_pk = Imovel.objects.create(**self.data_imovel).pk
        self.data_imovel['tipo'] = 'condomínio'
        self.condominio_pk = Imovel.objects.create(**self.data_imovel).pk
        url = reverse('imoveis_recibos')
        data = {'imprimir': [self.imovel_pk, self.condominio_pk], 'select_locador': locador, 'select_mes': 'janeiro', 'select_ano': '2024'}
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn('referente ao aluguel do(a) <b>apartamento</b>', resposta.content.decode('utf-8'))
        self.assertIn('referente ao condominio do mês de <b>janeiro</b>', resposta.content.decode('utf-8'))

    def test_imoveis_recibos_sem_selecionar_imovel(self):
        self.autentica()
        self.locador_pk = Locador.objects.create(**self.data_locador).pk
        locador = Locador.objects.get(id=self.locador_pk)
        url = reverse('imoveis_recibos')
        data = {'imprimir': [], 'select_locador': locador, 'select_mes': 'janeiro', 'select_ano': '2024'}
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn(
            'Você não selecionou nenhum cliente para imprimir recibo.',
            resposta.content.decode('utf-8')
        )


    def test_imoveis_recibos_sem_dados(self):
        self.autentica()
        url = reverse('imoveis_recibos')
        resposta = self.client.get(url, follow=True)
        self.assertIn('<span id="titulo">Imóveis & Aluguéis</span>', resposta.content.decode('utf-8'))

