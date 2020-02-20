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
    invited = serializers.CharField(allow_blank=True)
    price = serializers.IntegerField(write_only=True, required=False)
    bonus = serializers.IntegerField(write_only=True, required=False)
    position = serializers.CharField(write_only=True, required=False)
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

    def validate_price(self, price):
        return price

    def validate_bonus(self, bonus):
        return bonus

    def validate_position(self, position):
        return position

    def validate_phone_number(self, phone_number):
        return phone_number

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'bonus': self.validated_data.get('bonus', 10),
            'price': self.validated_data.get('price', 450),
            'position': self.validated_data.get('position', ''),
            'invited': self.validated_data.get('invited', ''),
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
    invited_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'phone_number', 'invited', 'square', 'price', 'bonus', 'id', 'contribution',
                  'self_contribution', 'invited_name', 'total_payed', 'lost', 'bonus_count', 'position')
        extra_kwargs = {
            'bonus_count': {'read_only': True},
            'lost': {'read_only': True},
            'total_payed': {'read_only': True},
            'self_contribution': {'read_only': True},
            'contribution': {'read_only': True},
            'square': {'read_only': True},
        }

    @staticmethod
    def get_invited_name(obj):
        if obj.invited:
            return obj.invited.full_name
        else:
            return None


class UserDetailSerializer(UserSerializer):

    def get_fields(self):
        fields = super(UserDetailSerializer, self).get_fields()
        fields['children'] = UserDetailSerializer(many=True, read_only=True)
        fields['user_payments'] = PaymentSerializer(many=True, read_only=True)
        return fields


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('full_name', 'id')


class TokenSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    moder = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = TokenModel
        fields = ('key', 'pk', 'moder', 'name')

    @staticmethod
    def get_name(obj):
        return obj.user.full_name

    @staticmethod
    def get_pk(obj):
        return obj.user.pk

    @staticmethod
    def get_moder(obj):
        return obj.user.is_superuser
