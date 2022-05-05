from django.views.generic import TemplateView, FormView
from django.views import generic
from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Solicitacao_Compra, Solicitacao_Venda, Moeda_Usuario, Saque, Solicitacao_Deposito
from .forms import CompraForm, VendaForm, DepositoForm, SaqueForm



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
def NovaVenda(request):
    template_name = 'forms/venda.html'
    form = VendaForm(request.user.id, request.POST or None)

    if(request.method == 'POST'):
        form = VendaForm( request.user.id, request.POST)

        if(form.is_valid()):
            cliente_venda = request.user
            moeda = form.cleaned_data['moeda']
            quantidade_venda = form.cleaned_data['quantidade_venda']        

            nova_venda = Solicitacao_Venda(cliente_venda=cliente_venda, moeda=moeda, quantidade_venda=quantidade_venda)
            nova_venda.save()

            messages.success(request, 'Solicitação de venda enviada com sucesso')

            return redirect('profile')

    elif(request.method == 'GET'):
        return render(request, 'forms/venda.html', {'form': form})


@login_required
def NovoDeposito(request):
    template_name = 'forms/depoisto.html'   
    form = DepositoForm(request.POST)

    if(request.method == 'POST'):
        form = DepositoForm(request.POST)

        if (form.is_valid()):
            cliente_deposito = request.user
            quantidade_reais_deposito = form.cleaned_data['quantidade_reais_deposito']
            status_deposito = 'waiting'

            novo_deposito = Solicitacao_Deposito(cliente_deposito=cliente_deposito, quantidade_reais_deposito=quantidade_reais_deposito, status_deposito=status_deposito)
            novo_deposito.save()

            return redirect('profile')

    elif(request.method == 'GET'):
        return render(request, 'forms/deposito.html', {'form': form})

@login_required
def NovoSaque(request):
    template_name = 'forms/saque.html'   
    form = SaqueForm(request.POST)

    if(request.method == 'POST'):
        form = SaqueForm(request.POST)

        if(form.is_valid()):
            cliente_saque = request.user
            valor_saque = form.cleaned_data['valor_saque']
            destino_saque = form.cleaned_data['destino_saque']

            novo_saque = Saque(cliente_saque=cliente_saque, valor_saque=valor_saque, destino_saque=destino_saque)
            novo_saque.save()

            return redirect('profile')

    elif(request.method == 'GET'):
        return render(request, 'forms/saque.html', {'form': form})
