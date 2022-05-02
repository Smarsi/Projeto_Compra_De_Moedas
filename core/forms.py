from django.forms import ModelForm
from django import forms

from .models import Solicitacao_Compra, Solicitacao_Venda


class CompraForm(ModelForm):
    class Meta:
        model = Solicitacao_Compra
        fields = ['moeda_compra', 'quantidade_reais_compra']
    

class VendaForm(ModelForm):

    usuario = forms.CharField

    class Meta:
        model = Solicitacao_Venda
        fields = ['posse']