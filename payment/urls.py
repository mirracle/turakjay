from django.urls import path

from .views import PaymentView, ExchangeRatesView

urlpatterns = [
    path('', PaymentView.as_view({'get': 'list', 'post': 'create'})),
    path('delete/<int:pk>/', PaymentView.as_view({'delete': 'destroy'})),
    path('exchange/', ExchangeRatesView.as_view({'get': 'list'})),
    path('exchange/<int:pk>/', ExchangeRatesView.as_view({'put': 'update'}))
]
