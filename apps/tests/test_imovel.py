from django.test import TestCase
from apps.imoveis.forms.imovel import FormImovel
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.urls import reverse
from apps.imoveis.models.imovel import Imovel
from apps.imoveis.models.cliente import Cliente
from apps.imoveis.models.locador import Locador

class TesteImovel(TestCase):
    def setUp(self, *args, **kwargs):
        self.data_cliente = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '19605692791',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
            'nacionalidade': 'brasileira',
            'estado_civil': 'casado',
            'cidade_residencia_sede': 'colatina-es',
        }
        self.cliente_pk = Cliente.objects.create(**self.data_cliente).pk
        self.data_locador = {
            'nome': 'John Doe',
            'cpf': '66755631736',
            'residencia': 'colatina',
            'estado_civil': 'casado',
            'data_nascimento': '1978-01-01',
            'telefone': '1111111111',
            'email': 'teste@teste.com',
            'principal': True,
        }
        self.locador_pk = Locador.objects.create(**self.data_locador).pk 
        self.data_imovel = {
            'tipo': 'apartamento',
            'numero': '100',
            'local': 'galeria',
            'cliente': Cliente.objects.last(),
            'valor': 100.0,
            'complemento': 'teste de complemento',
            'observacao': 'teste de observacao',
            'dia': 10,
            'iptu_inscricao': '1234567',
            'iptu_titular': Locador.objects.last(),
            'elfsm_inscricao': '1234567',
            'elfsm_titular': Locador.objects.last(),
        }
        self.imovel_pk = Imovel.objects.create(**self.data_imovel).pk
        self.user = User.objects.create_user('temporario', 'teste@teste.com', 'temporario')
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)
    
    def test_view_lista_imoveis(self):
        self.autentica()
        url = reverse('imoveis_lista')
        resposta = self.client.get(url)
        self.assertNotIn('Você não está autenticado!', resposta.content.decode('utf-8'))
        self.assertEqual(resposta.status_code, 200)


    def test_inserir_imovel(self):
        self.autentica()
        url = reverse('imoveis_lista')
        self.data_imovel['cliente'] = Cliente.objects.last().pk
        self.data_imovel['iptu_titular'] = Locador.objects.last().pk
        self.data_imovel['elfsm_titular'] = Locador.objects.last().pk
        resposta = self.client.post(url, data=self.data_imovel, follow=True)
        self.assertIn('Imóvel adicionado com sucesso', resposta.content.decode('utf-8'))

    def test_view_lista_imoveis_atualizar(self):
        self.autentica()
        url = reverse('imoveis_lista')
        imovel = model_to_dict(Imovel.objects.last())
        imovel['dia'] = 25
        resposta = self.client.post(url, data=imovel, follow=True)
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
        url = reverse('imovel_alterar', kwargs={'id_do_registro': self.imovel_pk})
        form = FormImovel()
        resposta = self.client.get(url, data={'form': form})
        self.assertIn(
            f'<input type="hidden" name="id" value="{self.imovel_pk}">',
            resposta.content.decode('utf-8')
        )

    def test_view_imovel_apagar(self):
        self.autentica()
        url = reverse('imovel_apagar', kwargs={'id_do_registro': self.imovel_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('Imóvel apagado com sucesso.', resposta.content.decode("utf-8"))

    def test_view_imovel_ordenador(self):
        self.autentica()
        for i in range(100, 104):
            self.data_imovel['numero'] = i
            Imovel.objects.create(**self.data_imovel)
        url = reverse('imoveis_ordenados', kwargs={'ordenador': 'numero'})
        resposta = self.client.get(url)
        self.assertIn('101', resposta.content.decode('utf-8'))
        self.assertIn('102', resposta.content.decode('utf-8'))
        self.assertIn('103', resposta.content.decode('utf-8'))
