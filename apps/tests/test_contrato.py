from django.test import TestCase
from apps.imoveis.models.imovel import Imovel
from apps.imoveis.models.locador import Locador
from apps.imoveis.models.contrato import Contrato
from apps.imoveis.models.cliente import Cliente
from django.urls import reverse
from django.contrib.auth.models import User

class TesteContrato(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'temporario@teste.com', 'temporario')
        self.data_cliente = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '920.223.820-05',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
            'nacionalidade': 'brasileira',
            'estado_civil': 'casado',
            'cidade_residencia_sede': 'colatina-es',
        }
        self.cliente_pk = Cliente.objects.create(**self.data_cliente).pk
        self.data_cliente_sem_cpf = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': None,
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
            'nacionalidade': 'brasileira',
            'estado_civil': 'casado',
            'cidade_residencia_sede': 'colatina-es',
        }
        self.cliente_sem_cpf_pk = Cliente.objects.create(**self.data_cliente_sem_cpf).pk
        self.data_imovel = {
            'tipo': 'apartamento',
            'numero': '100',
            'local': 'galeria',
            'cliente': Cliente.objects.get(id=self.cliente_pk),
            'valor': 100.0,
            'complemento': 'teste de complemento',
            'observacao': 'teste de observacao',
            'dia': 10,
        }
        self.imovel_pk = Imovel.objects.create(**self.data_imovel).pk
        self.data_locador = {
            'nome': 'John Doe',
            'cpf': '125.936.220-59',
            'residencia': 'colatina',
            'estado_civil': 'casado',
            'data_nascimento': '1978-01-01',
            'telefone': '1111111111',
            'email': 'teste@teste.com',
            'nacionalidade': 'brasileiro',
        }
        self.locador_pk = Locador.objects.create(**self.data_locador).pk
        self.data_cria_contrato = {
            'select_locador': self.locador_pk,
            'imovel_tipo':'apartamento',
            'imovel_local':'Travessa Onde Mora Locador 120',
            'imovel_numero':'205',
            'imovel_dia_pagamento':'10',
            'imovel_valor_aluguel':'1000.0',
            'cliente_nome':'João Locatário',
            'cliente_ci':'1234567 SSPES',
            'cliente_cpf_cnpj':'920.223.820-05',
            'cliente_estado_civil':'casado',
            'cliente_cidade_residencia_sede':'Colatina-ES',
            'cliente_nacionalidade':'Brasileiro',
            'uso_imovel':'residencial',
            'mes_inicio':'01',
            'ano_inicio':'2024',
            'mes_final':'12',
            'ano_final':'2024',
            'registro_id': self.imovel_pk
        }
        self.data_salva_contrato = {
            'imovel': Imovel.objects.get(id=self.imovel_pk),
            'data_impressao': '2024-01-01',
            'texto': '''
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOAO LOCADOR - 111.111.111-11 - LOCADOR</div>
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOSE LOCATARIO - 11.111.111/0001-11 - LOCATÁRIO</div>
            '''
        }
        self.contrato_pk = Contrato.objects.create(**self.data_salva_contrato).pk
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def test_contrato_form(self):
        self.autentica()
        self.data_imovel['cliente'] = Cliente.objects.get(id=self.cliente_pk)
        self.imovel_pk = Imovel.objects.create(**self.data_imovel).pk
        url = reverse('contrato_form', kwargs={'registro_id': self.imovel_pk})
        resposta = self.client.get(url)
        self.assertIn('<form method', resposta.content.decode("utf-8"))

    def test_contrato_form_sem_cpf(self):
        self.autentica()
        self.data_imovel['cliente'] = Cliente.objects.get(id=self.cliente_sem_cpf_pk)
        self.imovel_pk = Imovel.objects.create(**self.data_imovel).pk
        url = reverse('contrato_form', kwargs={'registro_id': self.imovel_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn(
            'Cliente sem CPF ou CNPJ cadastrado, entre em Clientes e faça o cadastro.', 
            resposta.content.decode("utf-8")
        )    

    def test_contrato_pessoa_fisica(self):
        self.autentica()
        url = reverse('contrato', kwargs={'registro_id': self.cliente_pk})
        resposta = self.client.post(url, data=self.data_cria_contrato, follow=True)
        self.assertIn(
            'de um lado, JOHN DOE, brasileiro, casado, residente em colatina',
            resposta.content.decode('utf-8')
        )
        self.assertIn('JOHN DOE - 125.936.220-59 - LOCADOR', resposta.content.decode('utf-8'))
        self.assertIn('JOÃO LOCATÁRIO - 920.223.820-05 - LOCATÁRIO', resposta.content.decode('utf-8'))

    def test_contrato_pessoa_juridica(self):
        self.autentica()
        url = reverse('contrato', kwargs={'registro_id': self.cliente_pk})
        self.data_cria_contrato['cliente_nome'] = "João Locador LTDA"
        self.data_cria_contrato['cliente_cpf_cnpj'] = '47.911.555/0001-59'
        self.data_cria_contrato['cliente_ci'] = ''
        self.data_cria_contrato['cliente_estado_civil'] = ''
        resposta = self.client.post(url, data=self.data_cria_contrato, follow=True)
        self.assertIn(
            'JOÃO LOCADOR LTDA, CNPJ 47.911.555/0001-59, sediado(a) em Colatina-ES',
            resposta.content.decode('utf-8')
        )

    def test_contratos_listar(self):
        self.autentica()
        url = reverse('contratos_listar', kwargs={'imovel_id': self.imovel_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('JOSE LOCATARIO', resposta.content.decode('utf-8'))

    def test_contrato_imprimir_usando_metodo_post(self):
        self.autentica()
        url = reverse('contrato_imprimir', kwargs={'registro_id': self.imovel_pk})
        data = {
            'texto_pagina': '''
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOAO LOCADOR - 111.111.111-11 - LOCADOR</div>
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOSE LOCATARIO - 11.111.111/0001-11 - LOCATÁRIO</div>
            ''',
            'salvar_contrato': 'on'
        }
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn('paragrafo-contrato-assinatura', resposta.content.decode('utf-8'))

    def test_contrato_imprimir_usando_metodo_get(self):
        self.autentica()
        url = reverse('contrato_imprimir', kwargs={'registro_id': self.contrato_pk})
        data = {
            'contrato_id': self.contrato_pk,
            'texto_pagina': '''
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOAO LOCADOR - 111.111.111-11 - LOCADOR</div>
                <div class="paragrafo-contrato-assinatura">___________________________________________________________________
                </div>
                <div class="paragrafo-contrato-assinatura-dados">JOSE LOCATARIO - 11.111.111/0001-11 - LOCATÁRIO</div>
            ''',
        }
        resposta = self.client.get(url, data=data, follow=True)
        self.assertIn('paragrafo-contrato-assinatura', resposta.content.decode('utf-8'))