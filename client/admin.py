from django.contrib import admin

from .models import User
from payment.models import Payment, ExchangeRates

admin.site.register(User)
admin.site.register(Payment)
admin.site.register(ExchangeRates)
