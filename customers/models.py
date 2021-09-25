# ADD A CUSTOM URL AND: 1-SELECT USER 2-SET USER.AGE TO SOMETHING! # <-This comment is too old and I won't delete it :)
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, PositiveIntegerField, EmailField, BooleanField
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator, RegexValidator
from django.db.models.fields.related import ForeignKey
from django_countries import Countries
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from picturic.fields import PictureField


class Messages:
    INVALID_USERNAME="Username can have [A-Z, a-z, 0-9, _] chars only."

class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an Username')

        user = self.model(
            username=username.strip(),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        """
        Creates and saves a staff user with the given username and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser):
    username = CharField(max_length=120, unique=True, validators=[RegexValidator('^[a-zA-z0-9_]+$',message=Messages.INVALID_USERNAME),MinLengthValidator(5)])
    email = EmailField(verbose_name='Email address', unique=True, max_length=100, null=True, blank=True)
    first_name = CharField(max_length=120, null=True, blank=True)
    last_name = CharField(max_length=120, null=True, blank=True)
    phone_number = CharField(max_length=32, validators=[MinLengthValidator(4)], null=True, blank=True)
    age = PositiveIntegerField(validators=[MinValueValidator(8), MaxValueValidator(120)], null=True, blank=True)
    profile_image = PictureField(use_upload_to_func=True,make_thumbnail=True,blank=True,default='defaults/customer_profile/cat.jpg')
    is_active = BooleanField(default=True)
    staff = BooleanField(default=False)  # a admin user; non super-user
    admin = BooleanField(default=False)  # a superuser

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # USERNAME_FIELD & Password are required by default.

    objects = CustomerManager()

    def __str__(self):
        return self.username or self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else (self.username or self.email)

    def get_short_name(self):
        return self.last_name or self.first_name or self.username or self.email

    def has_perm(self, perm, obj=None) -> bool:
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label) -> bool:
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self) -> bool:
        return self.staff

    @property
    def is_admin(self) -> bool:
        return self.admin


class Address(Model):
    country = CountryField(default="IR")
    city = CharField(max_length=60)
    street = CharField(max_length=255)
    postal_code = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    customer = ForeignKey(to=Customer, on_delete=CASCADE)
