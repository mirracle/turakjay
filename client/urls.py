from django.urls import path

from .views import UserView, UserDetailView


urlpatterns = [
    path('list/', UserView.as_view({'get': 'list'})),
    path('<int:pk>/', UserDetailView.as_view({'get': 'retrieve'})),
    path('tree/', UserDetailView.as_view({'get': 'list'})),
]
