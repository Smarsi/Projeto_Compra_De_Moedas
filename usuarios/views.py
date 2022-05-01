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

            

'''
class ContasView(TemplateView):
    template_name = 'contas.html'

    def get_context_data(self, **kwargs):
        context = super(ContasView, self).get_context_data(**kwargs)
        

        #context['produtos'] = Produto.objects.all()

        return context
'''

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        context['moedas'] = Moeda_Usuario.objects.filter(usuario=self.request.user)
        print(context)

        return context

class register(generic.CreateView):
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'