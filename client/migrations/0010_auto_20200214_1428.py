# Generated by Django 3.0.3 on 2020-02-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20200214_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonus_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Заработанно бонусов'),
        ),
        migrations.AddField(
            model_name='user',
            name='lost',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Начисленно родителю'),
        ),
        migrations.AddField(
            model_name='user',
            name='total_payed',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Всего оплаченно'),
        ),
    ]
