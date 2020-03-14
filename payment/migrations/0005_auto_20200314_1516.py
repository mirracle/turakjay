# Generated by Django 3.0.3 on 2020-03-14 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20200220_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount_kgs',
            field=models.PositiveIntegerField(default=0, verbose_name='Сумма Сом'),
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_usd',
            field=models.PositiveIntegerField(default=0, verbose_name='Сумма Usd'),
        ),
    ]
