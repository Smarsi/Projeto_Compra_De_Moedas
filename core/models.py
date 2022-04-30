from django.db import models
import uuid

from stdimage.models import StdImageField

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

# Modelo Base (todas as tabelas irão herdar esse modelo)
class Base(models.Model):
    criado = models.DateField('Criação', auto_now_add = True)
    modificado = models.DateTimeField('Atualização', auto_now = True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Compra(Base):

    STATUS_CHOICES = (
        ('waiting', 'Esperando Pagamento'),
        ('done', 'Pagamento Confirmado'),
        ('canceled', 'Cancelado'),
    )

    cliente_compra = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda_compra = models.CharField('Moeda', max_length=50)
    valor_moeda_compra = models.DecimalField(max_digits=16, decimal_places=8)
    quantidade_moeda_compra = models.DecimalField(max_digits=16, decimal_places=8)
    status_compra = models.CharField('Status', max_length=20, null = False, blank = False, default=STATUS_CHOICES[0], choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
