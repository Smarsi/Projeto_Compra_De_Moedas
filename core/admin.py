from django.contrib import admin

from .models import Solicitacao_Compra, Moeda, Moeda_Usuario, Solicitacao_Venda, Solicitacao_Deposito

@admin.register(Solicitacao_Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = ['cliente_deposito', 'quantidade_reais_deposito', 'status_deposito',]

@admin.register(Solicitacao_Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente_compra', 'moeda_compra', 'quantidade_reais_compra', 'quantidade_moeda', 'status_compra']


@admin.register(Solicitacao_Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['nome_venda', 'cliente_venda', 'moeda', 'valor_vendido', 'status_venda']


@admin.register(Moeda)
class MoedaAdmin(admin.ModelAdmin):
    list_display = ['nome_moeda']

@admin.register(Moeda_Usuario)
class Moeda_UsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'moeda', 'status', 'quantidade_moeda']
    