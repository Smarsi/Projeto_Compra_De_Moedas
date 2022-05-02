from django import forms

from .models import Solicitacao_Compra

class ContratacaoForm(forms.Form):
    class Meta:
        model = Solicitacao_Compra
        fields = 'cliente_compra', 'moeda_compra', 'quantidade_reais_compra'