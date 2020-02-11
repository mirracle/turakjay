from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from rest_auth.models import TokenModel

from client.models import User
from payment.serializers import PaymentSerializer


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    invited = serializers.CharField(source='invited_id', allow_blank=True)
    square = serializers.IntegerField(write_only=True, allow_null=True)
    price = serializers.IntegerField(write_only=True)
    bonus = serializers.IntegerField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(_("Пользователь с таким электронным адресом уже существует"))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("Два поля с паролями не совпадают."))
        return data

    def validate_full_name(self, full_name):
        return full_name

    def validate_invited(self, invited):
        if invited:
            return User.objects.get(id=int(invited))
        else:
            return None

    def validate_square(self, square):
        return square

    def validate_price(self, price):
        return price

    def validate_bonus(self, bonus):
        return bonus

    def validate_phone_number(self, phone_number):
        return phone_number

    def get_cleaned_data(self):
        print(self.validated_data.get('full_name', ''))
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'bonus': self.validated_data.get('bonus', ''),
            'price': self.validated_data.get('price', ''),
            'square': self.validated_data.get('square', ''),
            'invited': self.validated_data.get('invited', None),
            'full_name': self.validated_data.get('full_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.save_user(request, user, self)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'phone_number', 'invited', 'square', 'price', 'bonus', 'id')


class UserDetailSerializer(UserSerializer):

    def get_fields(self):
        fields = super(UserDetailSerializer, self).get_fields()
        fields['children'] = UserDetailSerializer(many=True)
        fields['user_payments'] = PaymentSerializer(many=True)
        return fields
