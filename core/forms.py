from django import forms

class ContratacaoForm(forms.Form):
    cliente = forms.CharField()
    moeda = forms.CharField()
    quantidade = forms.DecimalField()
    valor_moeda = forms.DecimalField
    valor_total = quantidade * valor_moeda