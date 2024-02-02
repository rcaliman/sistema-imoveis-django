from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def extrai_locatario(value):
    texto = value.split('<div class="paragrafo-contrato-assinatura-dados">')
    texto = texto[2].split('</div>')
    return texto[0]
    
