from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from allauth.account.utils import user_field
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    full_name = models.CharField('ФИО', max_length=256)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField('Номер телефона')
    invited = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    square = models.PositiveIntegerField('Площадь', blank=True, null=True, default=0)
    price = models.PositiveIntegerField('Цена за кв.м', default=1, blank=True)
    bonus = models.PositiveSmallIntegerField('Бонус', blank=True, null=True, default=10)
    contribution = models.PositiveIntegerField('Вклад', blank=True, null=True, default=0)
    contribution_usd = models.PositiveIntegerField('Вклад', blank=True, null=True, default=0)
    self_contribution = models.PositiveIntegerField('Свой Вклад', blank=True, null=True, default=0)
    self_contribution_usd = models.PositiveIntegerField('Свой Вклад', blank=True, null=True, default=0)
    total_payed = models.PositiveIntegerField('Всего оплаченно', blank=True, null=True, default=0)
    total_payed_usd = models.PositiveIntegerField('Всего оплаченно', blank=True, null=True, default=0)
    lost = models.PositiveIntegerField('Начисленно родителю', blank=True, null=True, default=0)
    lost_usd = models.PositiveIntegerField('Начисленно родителю', blank=True, null=True, default=0)
    bonus_count = models.PositiveIntegerField('Заработанно бонусов', blank=True, null=True, default=0)
    bonus_count_usd = models.PositiveIntegerField('Заработанно бонусов', blank=True, null=True, default=0)
    position = models.CharField('Должность', max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = None

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user_field(user, 'username', data['email'])
        user_field(user, 'email', data['email'])
        user.full_name = data['full_name']
        user.phone_number = data['phone_number']
        user.invited = data['invited']
        user.price = data['price']
        user.bonus = data['bonus']
        user.position = data['position']
        if 'password1' in data:
            user.set_password(data["password1"])
        if commit:
            user.save()
        return user

    def __str__(self):
        return str(self.full_name)

