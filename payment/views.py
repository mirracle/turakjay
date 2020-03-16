from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

from .serializers import PaymentSerializer, ExchangeRatesSerializer
from .models import Payment, ExchangeRates


class ExchangeRatesView(ModelViewSet):
    queryset = ExchangeRates.objects.all()
    serializer_class = ExchangeRatesSerializer

    def get_object(self):
        return ExchangeRates.objects.all().first()


class PaymentView(ModelViewSet):
    queryset = Payment.objects.filter(user__isnull=False)
    lookup_field = 'pk'
    serializer_class = PaymentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        with transaction.atomic():
            user = instance.user
            user.total_payed -= instance.amount_kgs
            user.total_payed_usd -= instance.amount_usd
            parent = user.invited
            user_lost_kgs = int(instance.amount_kgs / 100 * 10)
            user_lost_usd = int(instance.amount_usd / 100 * 10)
            if parent:
                parent_get_kgs = int(instance.amount_kgs / 100 * parent.bonus)
                parent_get_usd = int(instance.amount_usd / 100 * parent.bonus)
                parent.bonus_count -= parent_get_kgs
                parent.bonus_count_usd -= parent_get_usd
                parent.contribution -= parent_get_kgs
                parent.contribution_usd -= parent_get_usd
                parent.square = int(parent.contribution / parent.price)
                user.contribution -= instance.amount_kgs - user_lost_kgs
                user.contribution_usd -= instance.amount_usd - user_lost_usd
                user.self_contribution -= instance.amount_kgs - user_lost_kgs
                user.self_contribution_usd -= instance.amount_usd - user_lost_usd
                user.lost -= user_lost_kgs
                user.lost_usd -= user_lost_usd
                user.square = int(user.contribution / user.price)
                parent.save()
                user.save()
            else:
                user.contribution -= instance.amount_kgs - user_lost_kgs
                user.contribution_usd -= instance.amount_usd - user_lost_usd
                user.self_contribution -= instance.amount_kgs - user_lost_kgs
                user.self_contribution_usd -= instance.amount_usd - user_lost_usd
                user.lost -= user_lost_kgs
                user.lost_usd -= user_lost_usd
                user.square = int(user.contribution / user.price)
                user.save()
            instance.delete()
