from rest_framework.viewsets import ModelViewSet

from .serializers import PaymentSerializer
from .models import Payment


class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()
    lookup_field = 'pk'
    serializer_class = PaymentSerializer
