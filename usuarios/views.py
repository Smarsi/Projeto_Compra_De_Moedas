from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUsuarioCreateForm

from core.models import Moeda_Usuario

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

        moedas_vendidas = []
        moedas_ativas = []
        for m in moedas:
            if m.status != 'active':
                moedas_vendidas.append(m)
            else:
                moedas_ativas.append(m)

        context['moedas_ativas'] = moedas_ativas
        context['moedas_vendidas'] = moedas_vendidas

        return context

class register(generic.CreateView):
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'