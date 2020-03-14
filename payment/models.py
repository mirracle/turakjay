from django.db import models
from django.contrib.auth import get_user_model

from client.models import User


class Payment(models.Model):

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    CURRENCY_TYPES = (
        ('kgs', 'сом'),
        ('usd', 'доллар')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='user_payments', null=True)
    amount = models.PositiveIntegerField('Сумма', default=0)
    amount_kgs = models.PositiveIntegerField('Сумма Сом', default=0)
    amount_usd = models.PositiveIntegerField('Сумма Usd', default=0)
    pay_date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    currency = models.CharField('Ваоюта', choices=CURRENCY_TYPES, default='kgs', max_length=4)

    def __str__(self):
        return f'{self.amount}'


class ExchangeRates(models.Model):

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курсы валют'

    course = models.DecimalField(max_digits=5, decimal_places=2)
