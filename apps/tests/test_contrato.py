from django.test import TestCase
from apps.imoveis.models import Locador, Cliente, Imovel
from django.urls import reverse

class TesteContrato(TestCase):
    def setUp(self, *args, **kwargs):
        self.data_cliente = {
            'nome': 'John Doe',
            'data_nascimento': '1978-05-17',
            'ci' : '111111',
            'cpf': '11111111111',
            'telefone_1': '2799999999',
            'telefone_2': '2799998888',
            'tipo': 'pessoa física',
            'nacionalidade': 'brasileira',
            'estado_civil': 'casado',
            'cidade_residencia_sede': 'colatina-es',
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

        self.data_locador = {
            'nome': 'John Doe',
            'cpf': '11111111111',
            'residencia': 'colatina',
            'estado_civil': 'casado',
            'data_nascimento': '1978-01-01',
            'telefone': '1111111111',
            'email': 'teste@teste.com',
            'nacionalidade': 'brasileiro',
        }
        Locador(**self.data_locador).save()
        self.data_contrato = {
            'select_locador': '1',
            'imovel_tipo':'apartamento',
            'imovel_local':'Travessa Onde Mora Locador 120',
            'imovel_numero':'205',
            'imovel_dia_pagamento':'10',
            'imovel_valor_aluguel':'1000.0',
            'cliente_nome':'João Locatário',
            'cliente_ci':'1234567 SSPES',
            'cliente_cpf_cnpj':'012.345.678-00',
            'cliente_estado_civil':'casado',
            'cliente_tipo_pessoa':'pessoa física',
            'cliente_cidade_residencia_sede':'Colatina-ES',
            'cliente_nacionalidade':'Brasileiro',
            'uso_imovel':'residencial',
            'mes_inicio':'01',
            'ano_inicio':'2024',
            'mes_final':'12',
            'ano_final':'2024',
        }
        return super().setUp(*args, **kwargs)
    
    def autentica(self):
        url = reverse('index')
        usuario = {'usuario': 'temporario', 'senha': 'temporario'}
        self.client.post(url, data=usuario, follow=True)

    def test_contrato_form(self):
        self.autentica()
        Cliente(**self.data_cliente).save()
        self.data_imovel['cliente'] = Cliente.objects.get(id=1)
        Imovel(**self.data_imovel).save()
        url = reverse('contrato_form', kwargs={'registro_id': 1})
        resposta = self.client.get(url)
        self.assertIn('<form target=', resposta.content.decode("utf-8"))

    def test_contrato_pessoa_fisica(self):
        self.autentica()
        url = reverse('contrato')
        resposta = self.client.post(url, data=self.data_contrato, follow=True)
        self.assertIn(
            'de um lado, JOHN DOE, brasileiro, casado, residente em colatina',
            resposta.content.decode('utf-8')
        )
        self.assertIn('JOHN DOE - 11111111111 - LOCADOR', resposta.content.decode('utf-8'))
        self.assertIn('JOÃO LOCATÁRIO - 012.345.678-00 - LOCATÁRIO', resposta.content.decode('utf-8'))

    def test_contrato_pessoa_juridica(self):
        self.autentica()
        url = reverse('contrato')
        self.data_contrato['cliente_nome'] = "João Locador LTDA"
        self.data_contrato['cliente_cpf_cnpj'] = '00.123.123/1234-12'
        self.data_contrato['cliente_ci'] = ''
        self.data_contrato['cliente_estado_civil'] = ''
        self.data_contrato['cliente_tipo_pessoa'] = 'pessoa jurídica'
        resposta = self.client.post(url, data=self.data_contrato, follow=True)
        self.assertIn(
            'JOÃO LOCADOR LTDA, CNPJ 00.123.123/1234-12, sediado(a) em Colatina-ES',
            resposta.content.decode('utf-8')
        )