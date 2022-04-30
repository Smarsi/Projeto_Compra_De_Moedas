from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUsuarioCreateForm


class register(generic.CreateView):
    form_class = CustomUsuarioCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'