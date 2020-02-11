from django.db import models
from django.contrib.auth import get_user_model

from client.models import User


class Payment(models.Model):

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='user_payments', null=True)
    amount = models.PositiveIntegerField('Сумма', default=0)
    pay_date = models.DateTimeField('Дата оплаты', auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name} {self.amount}'
