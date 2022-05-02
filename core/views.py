from django.views.generic import TemplateView

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Solicitacao_Compra, Solicitacao_Venda, Moeda_Usuario
from .forms import CompraForm, VendaForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        
        context = super(IndexView, self).get_context_data(**kwargs)

        return context


class ProtocolosView(TemplateView):
    template_name = 'paginas/protocolo-de-seguranca.html'

    def get_context_data(self, **kwargs):
        
        context = super(ProtocolosView, self).get_context_data(**kwargs)

        return context

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

    def get_context_data(self, **kwargs):
        
        context = super(SobreView, self).get_context_data(**kwargs)

        return context

class ContatoView(TemplateView):
    template_name = 'paginas/contato.html'

    def get_context_data(self, **kwargs):
        
        context = super(ContatoView, self).get_context_data(**kwargs)

        return context

class NegociarView(TemplateView):
    template_name = 'paginas/negociar.html'

    def get_context_data(self, **kwargs):
        
        context = super(NegociarView, self).get_context_data(**kwargs)

        return context

@login_required
def NovaCompra(request):

    form = CompraForm()

    if(request.method == 'POST'):
        form = CompraForm(request.POST)

        if(form.is_valid()):
            moeda_compra = form.cleaned_data['moeda_compra']
            quantidade_reais_compra = form.cleaned_data['quantidade_reais_compra']
            cliente_compra = request.user


            nova_compra = Solicitacao_Compra(cliente_compra=cliente_compra, moeda_compra=moeda_compra, quantidade_reais_compra=quantidade_reais_compra, status_compra='waiting')
            nova_compra.save()

            return redirect('profile')
        
    elif(request.method == 'GET'):
        return render(request, 'forms/compra.html', {'form': form})


@login_required
def NovaVenda(request, id):

    form = VendaForm()

    if(request.method == 'POST'):
        form = VendaForm(request.POST)

        if(form.is_valid()):
            posse = form.cleaned_data['posse']
            cliente_venda = request.user


            nova_venda = Solicitacao_Venda(posse=posse, cliente_venda=cliente_venda, status_venda='waiting')
            nova_venda.save()

            return redirect('profile')
        
    elif(request.method == 'GET'):

        nova_venda = Moeda_Usuario.objects.filter(id=id)

        print(nova_venda)

        return render(request, 'forms/venda.html', {'form': form, 'item': nova_venda})