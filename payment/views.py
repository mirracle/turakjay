from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

from .serializers import PaymentSerializer
from .models import Payment


class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()
    lookup_field = 'pk'
    serializer_class = PaymentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        with transaction.atomic():
            user = instance.user
            user.total_payed -= instance.amount
            parent = user.invited
            user_lost = int(instance.amount / 100 * 10)
            if parent:
                parent_get = int(instance.amount / 100 * parent.bonus)
                parent.bonus_count -= parent_get
                parent.contribution -= parent_get
                parent.square = int(parent.contribution / parent.price)
                user.contribution -= instance.amount - user_lost
                user.self_contribution -= instance.amount - user_lost
                user.lost -= user_lost
                user.square = int(user.contribution / user.price)
                parent.save()
                user.save()
            else:
                user.contribution -= instance.amount - user_lost
                user.self_contribution -= instance.amount - user_lost
                user.lost -= user_lost
                user.square = int(user.contribution / user.price)
                user.save()
            instance.delete()
