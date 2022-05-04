from django.contrib import admin

from .models import Solicitacao_Compra, Moeda, Moeda_Usuario, Solicitacao_Venda, Solicitacao_Deposito, Saque
from usuarios.models import CustomUsuario

@admin.register(Solicitacao_Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = ['cliente_deposito', 'quantidade_reais_deposito', 'status_deposito',]

@admin.register(Solicitacao_Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente_compra', 'moeda_compra', 'quantidade_reais_compra', 'quantidade_moeda', 'status_compra']


@admin.register(Solicitacao_Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['cliente_venda', 'moeda', 'status_venda']

    '''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        usuario_logado = request.user.id
        if db_field.name == "cliente_venda":
            kwargs["queryset"] = CustomUsuario.objects.filter(id=usuario_logado)
        if db_field.name == "moeda":
            kwargs["queryset"] = Moeda_Usuario.objects.filter(usuario=usuario_logado)
        return super(VendaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    '''


@admin.register(Moeda)
class MoedaAdmin(admin.ModelAdmin):
    list_display = ['nome_moeda']

@admin.register(Moeda_Usuario)
class Moeda_UsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'moeda', 'status', 'quantidade_moeda']
    
@admin.register(Saque)
class SaqueAdmin(admin.ModelAdmin):
    list_display = ['cliente_saque', 'valor_saque']