from django.test import TestCase
from apps.imoveis.models.locador import Locador
from apps.imoveis.models.cliente import Cliente
from apps.imoveis.models.imovel import Imovel
from apps.imoveis.forms.locador import FormLocador
from apps.imoveis.forms.imovel import FormImovel
from apps.imoveis.forms.cliente import FormCliente
from helper import calcula_proxima_data, Recibos

class TestHelper(TestCase):
    def setUp(self, *args, **kwargs):
        self.data_locador = {
            'nome': 'John Doe',
            'cpf': '11111111111',
            'residencia': 'colatina',
            'estado_civil': 'casado',
            'data_nascimento': '1978-01-01',
            'telefone': '1111111111',
            'email': 'teste@teste.com',
        }
        FormLocador(self.data_locador).save()
        self.data_cliente = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '11111111111',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
        }
        FormCliente(self.data_cliente).save()
        self.data_imovel = {
            'tipo': 'apartamento',
            'numero': '100',
            'local': 'galeria',
            'cliente': Cliente.objects.get(id=1),
            'valor': 100.0,
            'complemento': 'teste de complemento',
            'observacao': 'teste de observacao',
            'dia': 10,
        }
        FormImovel(self.data_imovel).save()
        self.data_imovel = {
            'tipo': 'condomínio',
            'numero': '100',
            'local': 'galeria',
            'cliente': Cliente.objects.get(id=1),
            'valor': 100.0,
            'complemento': '',
            'observacao': '',
            'dia': 10,
        }
        FormImovel(self.data_imovel).save()
        self.locador = Locador.objects.get(id=1)
        self.registros_imoveis = Imovel.objects.all()
        return super().setUp(*args, **kwargs)
    
    def test_calcula_proxima_data(self):
        resultado = calcula_proxima_data('janeiro', '2023')
        self.assertEqual({'mes': 'fevereiro', 'ano': '2023'}, resultado)
        resultado = calcula_proxima_data('dezembro', '2023')
        self.assertEqual({'mes': 'janeiro', 'ano': '2024'}, resultado)


    def test_gerador_recibos(self):
        resposta = Recibos.gerador(self.registros_imoveis, self.locador, 'janeiro', '2024')
        self.assertIn('Recebi de <b>John Doe</b>', resposta)


