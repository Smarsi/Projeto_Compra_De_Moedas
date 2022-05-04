from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUsuarioCreateForm

from django.contrib.auth.decorators import login_required

from core.models import Moeda_Usuario, Solicitacao_Venda, Solicitacao_Compra, Solicitacao_Deposito, Saque
from .models import CustomUsuario

#from .models import Produto

# Create your views here.

class ContasView(View):

    def get(self, request, *args, **kwargs):

        print(request.user.is_anonymous)

        if request.user.is_anonymous: #Se o usuário não estiver logado
            return render(request, 'contas.html')
        else:
            return redirect('profile')


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        moedas = Moeda_Usuario.objects.filter(usuario=self.request.user)
        solicitacoes_venda = Solicitacao_Venda.objects.filter(cliente_venda=self.request.user)
        solicitacoes_compra = Solicitacao_Compra.objects.filter(cliente_compra=self.request.user)
        solicitacoes_saque = Saque.objects.filter(cliente_saque=self.request.user)
        solicitacoes_deposito = Solicitacao_Deposito.objects.filter(cliente_deposito=self.request.user)

        moedas_ativas = []
        for m in moedas:
            if m.status == 'active':
                if m.ativo == True:
                    moedas_ativas.append(m)

        context['moedas_ativas'] = moedas_ativas
        context['solicitacoes_venda'] = solicitacoes_venda
        context['solicitacoes_saque'] = solicitacoes_saque
        context['solicitacoes_deposito'] = solicitacoes_deposito
        context['solicitacoes_compra'] = solicitacoes_compra

        return context

    def Vender(id):
        print("Entrou")

class register(generic.CreateView):
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'