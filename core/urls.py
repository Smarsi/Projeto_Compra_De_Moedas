from django.urls import path, include

from .views import IndexView, ProtocolosView, SobreView, ContatoView, NegociarView, NovaCompra, NovaVenda, NovoSaque, NovoDeposito

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('protocolos/', ProtocolosView.as_view(), name='protocolos'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('negociar/', NegociarView.as_view(), name='negociar'),
    path('nova-compra/', NovaCompra, name='nova_compra'),
    path('nova-venda/', NovaVenda, name='nova_venda'),
    path('novo-deposito/', NovoDeposito, name='novo_deposito'),
    path('novo-saque/', NovoSaque, name='novo_saque'),
]
 