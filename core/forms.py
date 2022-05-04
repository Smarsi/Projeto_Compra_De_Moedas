from django.forms import ModelForm
from django import forms

from .models import Solicitacao_Compra, Solicitacao_Venda, Moeda_Usuario, Saque, Solicitacao_Deposito


class SaqueForm(ModelForm):
    class Meta:
        model = Saque
        fields = ['valor_saque', 'destino_saque']

class DepositoForm(ModelForm):
    class Meta:
        model = Solicitacao_Deposito
        fields = ['quantidade_reais_deposito']

class CompraForm(ModelForm):
    class Meta:
        model = Solicitacao_Compra
        fields = ['moeda_compra', 'quantidade_reais_compra']


class VendaForm(ModelForm):
    #posses = Moeda_Usuario.objects.all()
    #moeda = forms.ChoiceField()
    #quantidade_venda = forms.DecimalField(label='Quantidade a Vender', max_digits=24, decimal_places=8)

    class Meta:
        model = Solicitacao_Venda
        fields = ['moeda', 'quantidade_venda']

  
    def __init__(self, id_user = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moeda'].queryset = Moeda_Usuario.objects.filter(usuario=id_user)

