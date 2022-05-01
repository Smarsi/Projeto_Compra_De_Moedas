from django.urls import path, include

from django.views.generic.base import TemplateView
from .views import register, ContasView, ProfileView

urlpatterns = [
    path('', include('django.contrib.auth.urls')), #Adicionando as rotas do módulo de usuários padrão do DJango
    path('registrar/', register.as_view(), name='registrar'),
    path('', ContasView.as_view(), name='client_index'), #Chamando uma template view padrão.
    path('perfil/', ProfileView.as_view(), name='profile'),
]