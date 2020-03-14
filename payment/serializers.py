from rest_framework import serializers
from django.db import transaction

from .models import Payment, ExchangeRates
from client.models import User


class ExchangeRatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRates
        fields = ('course', 'id')


class PaymentSerializer(serializers.ModelSerializer):
    pay_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_name = serializers.SerializerMethodField()
    amount_kgs = serializers.IntegerField(read_only=True)
    amount_usd = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'pay_date', 'id', 'user_name', 'currency', 'amount_kgs', 'amount_usd')

    def create(self, validated_data):
        with transaction.atomic():
            payment = Payment.objects.create(**validated_data)
            client = validated_data.get('user')
            if validated_data.get('currency') == 'kgs':
                amount_kgs = validated_data.get('amount')
                amount_usd = int(validated_data.get('amount') / ExchangeRates.objects.all().first().course)
                payment.amount_kgs = amount_kgs
                payment.amount_usd = amount_usd
            else:
                amount_usd = validated_data.get('amount')
                amount_kgs = int(validated_data.get('amount') * ExchangeRates.objects.all().first().course)
                payment.amount_kgs = amount_kgs
                payment.amount_usd = amount_usd
            payment.save()
            parent = client.invited
            client.total_payed += amount_kgs
            client.total_payed_usd += amount_usd
            client_lost_kgs = int(amount_kgs / 100 * 10)
            client_lost_usd = int(amount_usd / 100 * 10)
            if parent:
                parent_get_kgs = int(amount_kgs / 100 * parent.bonus)
                parent_get_usd = int(amount_usd / 100 * parent.bonus)
                parent.contribution += parent_get_kgs
                parent.contribution_usd += parent_get_usd
                parent.bonus_count += parent_get_kgs
                parent.bonus_count_usd += parent_get_usd
                parent.square = int(parent.contribution / parent.price)
                client.self_contribution += amount_kgs - parent_get_kgs
                client.self_contribution_usd += amount_usd - parent_get_usd
                client.contribution += amount_kgs - parent_get_kgs
                client.contribution_usd += amount_usd - parent_get_usd
                client.lost += parent_get_kgs
                client.lost_usd += parent_get_usd
                client.square = int(client.contribution / client.price)
                parent.save()
            else:
                client.self_contribution += amount_kgs - client_lost_kgs
                client.self_contribution_usd += amount_usd - client_lost_usd
                client.contribution += amount_kgs - client_lost_kgs
                client.contribution_usd += amount_usd - client_lost_usd
                client.lost += client_lost_kgs
                client.lost_usd += client_lost_usd
                client.square = int(client.contribution / client.price)
            client.save()
        return payment

    @staticmethod
    def get_user_name(obj):
        return obj.user.full_name
