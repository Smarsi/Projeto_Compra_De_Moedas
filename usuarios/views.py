from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUsuarioCreateForm

#from .models import Produto

# Create your views here.
class ContasView(TemplateView):
    template_name = 'contas.html'

    def get_context_data(self, **kwargs):
        context = super(ContasView, self).get_context_data(**kwargs)
        

        #context['produtos'] = Produto.objects.all()

        return context

class register(generic.CreateView):
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'