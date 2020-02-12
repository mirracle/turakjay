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
            if client.invited:
                print(client.invited.bonus)
        return payment

    @staticmethod
    def get_user_name(obj):
        return obj.user.full_name
