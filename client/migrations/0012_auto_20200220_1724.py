# Generated by Django 3.0.3 on 2020-02-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_user_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Должность'),
        ),
    ]
