from django.urls import path

from .views import PaymentView

urlpatterns = [
    path('list/', PaymentView.as_view({'get': 'list'})),

]
