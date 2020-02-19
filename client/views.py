from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer, UserDetailSerializer, UserShortSerializer


class UserView(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    lookup_field = 'pk'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('full_name', 'position')


class UserDetailView(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    lookup_field = 'pk'
    serializer_class = UserDetailSerializer


class UserShortView(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserShortSerializer
