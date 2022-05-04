from django.db import models
import uuid

from django.core.exceptions import ValidationError
from stdimage.models import StdImageField
from usuarios.models import CustomUsuario

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


class Solicitacao_Deposito(Base):

    STATUS_CHOICES = (
        ('waiting', 'Esperando Pagamento'),
        ('done', 'Pagamento Confirmado'),
        ('canceled', 'Cancelado'),
    )

    cliente_deposito = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Cliente', on_delete=models.PROTECT)
    quantidade_reais_deposito = models.DecimalField('Quantidade (R$)', max_digits=16, decimal_places=2)
    status_deposito = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0], choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Solicitação de Deposito'
        verbose_name_plural = 'Solicitações de Deposito'

    def __str__(self):
        return str(self.cliente_deposito)

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
            
            if campos_alterados['status_deposito'] == True: #Ativando o valor na conta do usuário após o pagamento (saldo).
                if getattr(novo, 'status_deposito') == 'done' and getattr(antigo, 'status_deposito') == 'waiting': 
                    saldo_cliente = CustomUsuario.objects.get(username=self.cliente_deposito) #Se o deposito for marcado como "done" iremos somar o valor do deposito na conta do cliente
                    CustomUsuario.objects.filter(pk=saldo_cliente.pk).update(saldo = saldo_cliente.saldo + self.quantidade_reais_deposito)

            if campos_alterados['status_deposito'] == True:
                if getattr(novo, 'status_deposito') == 'canceled':
                    self.ativo = False
            
            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:

            if(self.quantidade_reais_deposito) > 0:
                super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
            else:
                raise ValidationError("Você não pode depositar este valor")
            


class Solicitacao_Compra(Base):

    STATUS_CHOICES = (
        ('waiting', 'Pendente'),
        ('done', 'Concluído'),
        ('canceled', 'Cancelado'),
    )

    nome_compra = models.CharField('Nome Compra', max_length=100, null=False, blank = False, editable=False, default = f'{uuid.uuid4()}')
    cliente_compra = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda_compra = models.ForeignKey('core.Moeda', verbose_name='Moeda Escolhida', on_delete=models.SET_NULL, null=True)
    quantidade_reais_compra = models.DecimalField('Quantidade (R$)', max_digits=16, decimal_places=2)
    quantidade_moeda = models.DecimalField('Quantidade', max_digits=24, decimal_places=8, blank=True, null=True)
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
                    
                    try:
                        moeda_cliente = Moeda_Usuario.objects.get(moeda=self.moeda_compra) #Tentando pegar se o usuário ja tem essa moeda nas posses
                    except:
                        moeda_cliente=False #se não existir na conta é setado o valor False
 
                    if moeda_cliente:
                        # Se o usuário já tiver essa moeda cadastrada nas posses
                        item = Moeda_Usuario.objects.get(moeda=self.moeda_compra)
                        Moeda_Usuario.objects.filter(moeda = self.moeda_compra).update(quantidade_moeda= item.quantidade_moeda+self.quantidade_moeda, ativo=True)
                    else:
                        # Se o usuário não tiver esse registro de moeda
                        moeda_cliente = Moeda_Usuario(
                            usuario = self.cliente_compra,
                            moeda = self.moeda_compra,
                            quantidade_moeda = self.quantidade_moeda,
                            solicitacao = self, #essa solicitação
                            )
                        moeda_cliente.save()

                else:
                    pass

            if campos_alterados['status_compra'] == True:
                if getattr(novo, 'status_compra') == 'canceled':
                    self.ativo = False  
                    cliente = CustomUsuario.objects.get(email = self.cliente_compra)
                    CustomUsuario.objects.filter(pk=cliente.pk).update(saldo = cliente.saldo + self.quantidade_reais_compra)

            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:
            #Ao solicitar a compra vamos checar se o saldo disponível é suficiente
            cliente = CustomUsuario.objects.get(email = self.cliente_compra)

            if(cliente.saldo < self.quantidade_reais_compra):
                raise ValidationError("Saldo insuficiente")
                return err
                err = "SALDO INSUFICIENTE"
            else:
                CustomUsuario.objects.filter(pk=cliente.pk).update(saldo = cliente.saldo - self.quantidade_reais_compra)
                super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django


class Moeda_Usuario(Base):
#Esta tabela atribui uma moeda a um usuário do sistema efetivamente (deve ser chamada automaticamente pela troca de status da tabela 'Compra')

    STATUS_CHOICES = (
        ('active', 'Ativo na Conta'),
        ('canceled', 'Reembolsado'),
    )

    usuario = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda = models.OneToOneField('core.Moeda', verbose_name='Moeda', unique=True, on_delete=models.PROTECT)
    quantidade_moeda = models.DecimalField('Quantidade', max_digits=24, decimal_places=8)
    status = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0][0], choices = STATUS_CHOICES)
    solicitacao = models.ForeignKey('core.Solicitacao_Compra', verbose_name='Compra', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Moeda_Usuario'
        verbose_name_plural = 'Moedas_Usuarios'

    def __str__(self):
        return str(self.moeda)

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

            if campos_alterados['quantidade_moeda'] == True:

                if getattr(novo, 'quantidade_moeda') <= 0 and getattr(antigo, 'quantidade_moeda') > 0:
                    self.ativo = False                    
                    
            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:
             super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django

    
class Solicitacao_Venda(Base):

    STATUS_CHOICES = (
        ('waiting', 'Solicitado'),
        ('done', 'Vendido'),
        ('canceled', 'Cancelado'),
    )

    nome_venda = models.CharField('Nome Venda', max_length=100, null=False, blank = False, default = f'{uuid.uuid4()}')
    cliente_venda = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    moeda = models.ForeignKey('core.Moeda_Usuario', verbose_name='Posse Escolhida', on_delete=models.SET_NULL, null=True)
    quantidade_venda = models.DecimalField('Quantidade', max_digits=24, decimal_places=8)
    valor_reais_venda = models.DecimalField('Valor (R$)', max_digits=16, decimal_places=2, default=0.00)
    status_venda = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)

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

            if campos_alterados['status_venda'] == True:

                if getattr(novo, 'status_venda') == 'done' and getattr(antigo, 'status_venda') == 'waiting':
                    user = CustomUsuario.objects.get(username=self.cliente_venda)
                    CustomUsuario.objects.filter(pk=user.pk).update(saldo = user.saldo + self.valor_reais_venda)

                if getattr(novo, 'status_venda') == 'canceled':
                    self.ativo = False  
                    saldo_moeda = Moeda_Usuario.objects.get(pk= self.moeda.pk, usuario = self.cliente_venda)
                    Moeda_Usuario.objects.filter(pk=saldo_moeda.pk).update(quantidade_moeda = saldo_moeda.quantidade_moeda + self.quantidade_venda)
                    print(self)

            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:

            #Se o item estiver sendo criado-> 
            # Vamos verificar se ele tem o saldo que está solicitando venda
            #Vamos subtrair o valor da venda da posse do usuário
        
            saldo_moeda = Moeda_Usuario.objects.get(pk= self.moeda.pk, usuario = self.cliente_venda)

            if(saldo_moeda.quantidade_moeda < self.quantidade_venda):
                raise ValidationError("Quantidade de cripto insuficiente")
                err = "SALDO CRIPTO INSUFICIENTE"
                return err
            else:
                Moeda_Usuario.objects.filter(pk=saldo_moeda.pk).update(quantidade_moeda = saldo_moeda.quantidade_moeda - self.quantidade_venda)
                if((saldo_moeda.quantidade_moeda - self.quantidade_venda) == 0):
                    Moeda_Usuario.objects.filter(pk=saldo_moeda.pk).update(ativo=False)
                super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django

class Saque(Base):
    STATUS_CHOICES = (
        ('waiting', 'Solicitado'),
        ('done', 'Efetuado'),
        ('canceled', 'Cancelado'),
    )

    nome_saque = models.CharField('Nome Saque', max_length=100, null=False, blank = False, default = f'{uuid.uuid4()}')
    valor_saque = models.DecimalField('Valor a ser sacado', max_digits=16, decimal_places=2)
    destino_saque = models.TextField('Descrição do Saque', max_length=1000, blank=False, null=False)
    cliente_saque = models.ForeignKey('usuarios.CustomUsuario', verbose_name='Usuario', on_delete=models.CASCADE)
    status_saque = models.CharField('Status', max_length=100, null = False, blank = False, default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Solicitação de Saque'
        verbose_name_plural = 'Solicitações de Saque'

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

            #if campos_alterados['status_saque'] == True:

            super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
        else:
            if(self.valor_saque) > 0: #Prevenindo o saque negativo
                saldo_cliente = CustomUsuario.objects.get(email=self.cliente_saque)
                if((saldo_cliente.saldo - self.valor_saque) > 0):
                    CustomUsuario.objects.filter(pk=saldo_cliente.pk).update(saldo = saldo_cliente.saldo - self.valor_saque)
                    super().save(*args, **kwargs) #chamando o método de salvamento padrão do Django
                else:
                    raise ValidationError("Está tentando sacar um valor maior que o disponível em conta")
            else:
                raise ValidationError("Você não pode sacar este valor")
            
