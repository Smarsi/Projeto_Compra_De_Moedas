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


class Moeda(Base):

    nome_moeda = models.CharField('Moeda', max_length=10)

    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'

    def __str__(self):
        return self.nome_moeda


class Solicitacao_Compra(Base):

    STATUS_CHOICES = (
        ('waiting', 'Esperando Pagamento'),
        ('done', 'Pagamento Confirmado'),
        ('canceled', 'Cancelado'),
    )

    nome_compra = models.CharField('Nome Compra', max_length=100, null=False, blank = False, default = f'{uuid.uuid4()}')
    cliente_compra = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda_compra = models.ForeignKey('core.Moeda', verbose_name='Moeda Escolhida', on_delete=models.SET_NULL, null=True)
    quantidade_reais_compra = models.DecimalField('Quantidade (R$)', max_digits=16, decimal_places=2, default=0)
    status_compra = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0], choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Solicitação de Compra'
        verbose_name_plural = 'Solicitações de Compra'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):

        if self.pk:
            
            #Vamos pegar qual atributo foi alterado
            cls = self.__class__
            antigo = cls.objects.get(pk=self.pk) #Vamos pegar o status atual do item uma vez que ainda não salvamos a aleteração chamando o salvamento padrão
            novo = self

            campos_alterados = {}
            for campo in cls._meta.get_fields():
                field_name = campo.name
                try:
                    if getattr(antigo, field_name) != getattr(novo, field_name):
                        campos_alterados[field_name] = True
                    else:
                        campos_alterados[field_name] = False

                except Exception as ex: # Pega o erro "O campo não existe"
                    pass

            # Lógica de Salvamento para os campos alterados:

            if campos_alterados['status_compra'] == True: #Ativando a moeda na conta do usuário após o pagamento.
                if getattr(novo, 'status_compra') == 'done' and getattr(antigo, 'status_compra') == 'waiting':
                    moeda_cliente = Moeda_Usuario(
                        usuario = self.cliente_compra,
                        moeda = self.moeda_compra,
                        quantidade_reais_compra = self.quantidade_reais_compra,
                        solicitacao = self, #essa solicitação
                        )

                    moeda_cliente.save()
                    print(novo._meta.get_field('cliente_compra'))
                    
                else:
                    pass

            if campos_alterados['status_compra'] == True:
                if getattr(novo, 'status_compra') == 'canceled':
                    self.ativo = False

            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:
            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django


class Moeda_Usuario(Base):
#Esta tabela atribui uma moeda a um usuário do sistema efetivamente (deve ser chamada automaticamente pela troca de status da tabela 'Compra')

    STATUS_CHOICES = (
        ('active', 'Ativo na Conta'),
        ('sold', 'Vendido'),
        ('refunded', 'Reembolsado'),
    )

    usuario = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda = models.ForeignKey('core.Moeda', verbose_name='Moeda', on_delete=models.CASCADE)
    quantidade_reais_compra = models.DecimalField('Quantidade (R$)', max_digits=16, decimal_places=2, default=0)
    status = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0][0], choices = STATUS_CHOICES)
    solicitacao = models.ForeignKey('core.Solicitacao_Compra', verbose_name='Compra', on_delete=models.CASCADE, default = 0)

    class Meta:
        verbose_name = 'Moeda_Usuario'
        verbose_name_plural = 'Moedas_Usuarios'

    def __str__(self):
        return str(self.pk)

    
class Solicitacao_Venda(Base):

    STATUS_CHOICES = (
        ('waiting', 'Solicitado'),
        ('done', 'Vendido'),
        ('canceled', 'Cancelado'),
    )

    nome_venda = models.CharField('Nome Venda', max_length=100, null=False, blank = False, default = f'{uuid.uuid4()}')
    cliente_venda = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    posse = models.ForeignKey('core.Moeda_Usuario', verbose_name='Posse Escolhida', on_delete=models.SET_NULL, null=True)
    status_venda = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0], choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Solicitação de Venda'
        verbose_name_plural = 'Solicitações de Venda'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):

        if self.pk:
            
            #Vamos pegar qual atributo foi alterado
            cls = self.__class__
            antigo = cls.objects.get(pk=self.pk) #Vamos pegar o status atual do item uma vez que ainda não salvamos a aleteração chamando o salvamento padrão
            novo = self

            campos_alterados = {}
            for campo in cls._meta.get_fields():
                field_name = campo.name
                try:
                    if getattr(antigo, field_name) != getattr(novo, field_name):
                        campos_alterados[field_name] = True
                    else:
                        campos_alterados[field_name] = False

                except Exception as ex: # Pega o erro "O campo não existe"
                    pass

            # Lógica de Salvamento para os campos alterados:

            if campos_alterados['status_venda'] == True: #Alterando o status da moeda para Vendido.
                if getattr(novo, 'status_venda') == 'done' and getattr(antigo, 'status_venda') == 'waiting':
                    moeda_cliente = self.moeda_venda
                    moeda_cliente.status = 'sold'
                    moeda_cliente.save()
                    
                else:
                    pass

            if campos_alterados['status_venda'] == True:
                if getattr(novo, 'status_venda') == 'canceled':
                    self.ativo = False

            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:
            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django