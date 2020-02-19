from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer, UserDetailSerializer, UserShortSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer


class UserDetailView(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UserDetailSerializer


class UserShortView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserShortSerializer
