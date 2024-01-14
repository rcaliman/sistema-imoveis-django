from django.test import TestCase
from apps.imoveis.models import Imovel, Cliente
from apps.imoveis.forms import FormImovel
from apps.imoveis.forms import FormCliente
from django.contrib.auth.models import User
from django.urls import reverse

class TesteImovel(TestCase):
    def setUp(self, *args, **kwargs):
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
            'cliente': '',
            'valor': 100.0,
            'complemento': 'teste de complemento',
            'observacao': 'teste de observacao',
            'dia': 10,
        }
        self.user = User.objects.create_user('temporario', 'teste@teste.com', 'temporario')
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def insere_imovel(self, numero=100):
        url = reverse('imoveis_lista')
        self.data_imovel['numero'] = numero
        return self.client.post(url, data=self.data_imovel, follow=True)
    
    def test_view_lista_imoveis(self):
        self.autentica()
        url = reverse('imoveis_lista')
        resposta = self.client.get(url)
        self.assertNotIn('Você não está autenticado!', resposta.content.decode('utf-8'))
        self.assertEqual(resposta.status_code, 200)

    def test_view_lista_imoveis_adicionar(self):
        self.autentica()
        resposta = self.insere_imovel()
        self.assertIn('Imóvel adicionado com sucesso.', resposta.content.decode('utf-8'))

    def test_view_lista_imoveis_atualizar(self):
        self.autentica()
        self.insere_imovel()
        url = reverse('imoveis_lista')
        self.data_imovel['id'] = 1
        self.data_imovel['valor'] = 125.5
        resposta = self.client.post(url, data=self.data_imovel, follow=True)
        self.assertIn('Imóvel atualizado com sucesso.', resposta.content.decode('utf-8'))

    def test_view_imovel_formulario_inserir(self):
        self.autentica()
        url = reverse('imovel_inserir')
        form = FormImovel()
        resposta = self.client.get(url, data={'form': form})
        self.assertIn(
            '<form class="formulario" method="post" action="/imoveis/lista/">',
            resposta.content.decode('utf-8')
        )
    def test_view_imovel_alterar(self):
        self.autentica()
        self.insere_imovel()        
        url = reverse('imovel_alterar', kwargs={'id_do_registro': 1})
        form = FormImovel()
        resposta = self.client.get(url, data={'form': form})
        self.assertIn(
            ' <input type="hidden" name="id" value="1">',
            resposta.content.decode('utf-8')
        )

    def test_view_imovel_apagar(self):
        self.autentica()
        self.insere_imovel()
        url = reverse('imovel_apagar', kwargs={'id_do_registro': 1})
        resposta = self.client.get(url, follow=True)
        self.assertIn('Imóvel apagado com sucesso.', resposta.content.decode("utf-8"))

    def test_view_imovel_ordenador(self):
        self.autentica()
        self.insere_imovel(102)
        self.insere_imovel(101)
        self.insere_imovel(103)
        url = reverse('imoveis_ordenados', kwargs={'ordenador': 'numero'})
        resposta = self.client.get(url)
        self.assertIn('<td class="number">101</td>', resposta.content.decode('utf-8'))
        self.assertIn('<td class="number">102</td>', resposta.content.decode('utf-8'))
        self.assertIn('<td class="number">103</td>', resposta.content.decode('utf-8'))

    def test_imoveis_recibos(self):
        self.autentica()
        FormCliente(self.data_cliente).save()
        self.data_imovel['cliente'] = Cliente.objects.get(id=1)
        url = reverse('imoveis_recibos')
        data = {'imprimir': ['1'], 'locatario': '', 'recibo_mes': 'janeiro', 'recibo_ano': '2024'}
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn('RECIBO', resposta.content.decode('utf-8'))

