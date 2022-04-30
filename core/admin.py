from django.contrib import admin

from .models import Compra

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente_compra', 'moeda_compra', 'valor_moeda_compra', 'quantidade_moeda_compra', 'status_compra']
