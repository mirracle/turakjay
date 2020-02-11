from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    pay_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user = serializers.StringRelatedField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'pay_date', 'id', 'user_id')

    def get_user_id(self, obj):
        return obj.user.pk

