# Generated by Django 4.0.4 on 2022-05-05 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Moeda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome_moeda', models.CharField(max_length=10, verbose_name='Moeda')),
            ],
            options={
                'verbose_name': 'Moeda',
                'verbose_name_plural': 'Moedas',
            },
        ),
        migrations.CreateModel(
            name='Moeda_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('quantidade_moeda', models.DecimalField(decimal_places=8, max_digits=24, verbose_name='Quantidade')),
                ('status', models.CharField(choices=[('active', 'Ativo na Conta'), ('canceled', 'Reembolsado')], default='active', max_length=100, verbose_name='Status')),
                ('moeda', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.moeda', verbose_name='Moeda')),
            ],
            options={
                'verbose_name': 'Moeda_Usuario',
                'verbose_name_plural': 'Moedas_Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Solicitacao_Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome_venda', models.CharField(default='74a7708a-55e9-4630-8184-7ddaf56a4eec', max_length=100, verbose_name='Nome Venda')),
                ('quantidade_venda', models.DecimalField(decimal_places=8, max_digits=24, verbose_name='Quantidade')),
                ('valor_reais_venda', models.DecimalField(decimal_places=2, default=0.0, max_digits=16, verbose_name='Valor (R$)')),
                ('status_venda', models.CharField(choices=[('waiting', 'Solicitado'), ('done', 'Vendido'), ('canceled', 'Cancelado')], default='waiting', max_length=100, verbose_name='Status')),
                ('cliente_venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('moeda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.moeda_usuario', verbose_name='Posse Escolhida')),
            ],
            options={
                'verbose_name': 'Solicitação de Venda',
                'verbose_name_plural': 'Solicitações de Venda',
            },
        ),
        migrations.CreateModel(
            name='Solicitacao_Deposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('quantidade_reais_deposito', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Quantidade (R$)')),
                ('status_deposito', models.CharField(choices=[('waiting', 'Esperando Pagamento'), ('done', 'Pagamento Confirmado'), ('canceled', 'Cancelado')], default=('waiting', 'Esperando Pagamento'), max_length=100, verbose_name='Status')),
                ('cliente_deposito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Solicitação de Deposito',
                'verbose_name_plural': 'Solicitações de Deposito',
            },
        ),
        migrations.CreateModel(
            name='Solicitacao_Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome_compra', models.CharField(default='5bf6d8b5-4ffd-4c2b-8847-94accfe428dd', editable=False, max_length=100, verbose_name='Nome Compra')),
                ('quantidade_reais_compra', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Quantidade (R$)')),
                ('quantidade_moeda', models.DecimalField(blank=True, decimal_places=8, max_digits=24, null=True, verbose_name='Quantidade')),
                ('status_compra', models.CharField(choices=[('waiting', 'Pendente'), ('done', 'Concluído'), ('canceled', 'Cancelado')], default=('waiting', 'Pendente'), max_length=100, verbose_name='Status')),
                ('cliente_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('moeda_compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.moeda', verbose_name='Moeda Escolhida')),
            ],
            options={
                'verbose_name': 'Solicitação de Compra',
                'verbose_name_plural': 'Solicitações de Compra',
            },
        ),
        migrations.CreateModel(
            name='Saque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('nome_saque', models.CharField(default='7b0e98cf-bd23-453b-a438-6a19b192b6e4', max_length=100, verbose_name='Nome Saque')),
                ('valor_saque', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Valor a ser sacado')),
                ('destino_saque', models.TextField(max_length=1000, verbose_name='Descrição do Saque')),
                ('status_saque', models.CharField(choices=[('waiting', 'Solicitado'), ('done', 'Efetuado'), ('canceled', 'Cancelado')], default='waiting', max_length=100, verbose_name='Status')),
                ('cliente_saque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Solicitação de Saque',
                'verbose_name_plural': 'Solicitações de Saque',
            },
        ),
        migrations.AddField(
            model_name='moeda_usuario',
            name='solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.solicitacao_compra', verbose_name='Compra'),
        ),
        migrations.AddField(
            model_name='moeda_usuario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
