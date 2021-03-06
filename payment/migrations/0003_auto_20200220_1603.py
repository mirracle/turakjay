# Generated by Django 3.0.3 on 2020-02-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20200211_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
            options={
                'verbose_name': 'Курс валют',
                'verbose_name_plural': 'Курсы валют',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('kgs', 'сом'), ('usd', 'доллар')], default='kgs', max_length=4, verbose_name='Ваоюта'),
        ),
    ]
