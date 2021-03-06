from django.urls import path

from .views import UserView, UserDetailView, UserShortView, UserPkShortView


urlpatterns = [
    path('list/', UserView.as_view({'get': 'list'})),
    path('<int:pk>/', UserDetailView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('tree/', UserDetailView.as_view({'get': 'list'})),
    path('list/short/', UserShortView.as_view({'get': 'list'})),
    path('list/short/<int:pk>/', UserPkShortView.as_view({'get': 'list'}))
]
