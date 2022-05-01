from django.contrib import admin

from .models import Solicitacao_Compra, Moeda, Moeda_Usuario

@admin.register(Solicitacao_Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente_compra', 'moeda_compra', 'quantidade_reais_compra', 'status_compra']

@admin.register(Moeda)
class MoedaAdmin(admin.ModelAdmin):
    list_display = ['nome_moeda']

@admin.register(Moeda_Usuario)
class Moeda_UsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'moeda', 'status', 'quantidade_reais_compra']