# Generated by Django 4.0.4 on 2022-05-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusuario',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16, verbose_name='Saldo (R$)'),
        ),
    ]
