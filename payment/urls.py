from django.urls import path

from .views import PaymentView

urlpatterns = [
    path('', PaymentView.as_view({'get': 'list', 'post': 'create'})),
    path('delete/<int:pk>/', PaymentView.as_view({'delete': 'destroy'})),
]
