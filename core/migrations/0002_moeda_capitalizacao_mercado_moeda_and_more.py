# Generated by Django 4.0.4 on 2022-04-29 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moeda',
            name='capitalizacao_mercado_moeda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Capitalização de Mercado'),
        ),
        migrations.AddField(
            model_name='moeda',
            name='valor_mercado_moeda_diluido',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Capitalização de Mercado'),
        ),
        migrations.AddField(
            model_name='moeda',
            name='variacao_percent_moeda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Variação %'),
        ),
    ]
