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
            instance.delete()
