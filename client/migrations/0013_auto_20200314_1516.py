# Generated by Django 3.0.3 on 2020-03-14 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_auto_20200220_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonus_count_usd',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Заработанно бонусов'),
        ),
        migrations.AddField(
            model_name='user',
            name='contribution_usd',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Вклад'),
        ),
        migrations.AddField(
            model_name='user',
            name='lost_usd',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Начисленно родителю'),
        ),
        migrations.AddField(
            model_name='user',
            name='self_contribution_usd',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Свой Вклад'),
        ),
        migrations.AddField(
            model_name='user',
            name='total_payed_usd',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Всего оплаченно'),
        ),
    ]
