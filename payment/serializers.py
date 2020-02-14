from rest_framework import serializers
from django.db import transaction

from .models import Payment
from client.models import User


class PaymentSerializer(serializers.ModelSerializer):
    pay_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'pay_date', 'id', 'user_name')

    def create(self, validated_data):
        with transaction.atomic():
            payment = Payment.objects.create(**validated_data)
            client = validated_data.get('user')
            parent = client.invited
            client.total_payed += validated_data.get('amount')
            client_lost = int(validated_data.get('amount') / 100 * 10)
            if parent:
                parent_get = int(validated_data.get('amount') / 100 * parent.bonus)
                parent.contribution += parent_get
                parent.bonus_count += parent_get
                parent.square = int(parent.contribution / parent.price)
                client.self_contribution += validated_data.get('amount') - parent_get
                client.contribution += validated_data.get('amount') - parent_get
                client.lost += parent_get
                client.square = int(client.self_contribution / client.price)
                parent.save()
            else:
                client.self_contribution += validated_data.get('amount') - client_lost
                client.contribution += validated_data.get('amount') - client_lost
                client.lost += client_lost
                client.square = int(client.self_contribution / client.price)
            client.save()
        return payment

    @staticmethod
    def get_user_name(obj):
        return obj.user.full_name
