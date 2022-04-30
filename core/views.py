from django.views.generic import TemplateView

#from .models import myModel

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