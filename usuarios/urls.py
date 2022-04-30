from django.urls import path, include

from django.views.generic.base import TemplateView
from .views import register

urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')), #Adicionando as rotas do módulo de usuários padrão do DJango
    path('registrar/', register.as_view(), name='registrar'),
    path('', TemplateView.as_view(template_name='client_index.html'), name='client_index'), #Chamando uma template view padrão.
]