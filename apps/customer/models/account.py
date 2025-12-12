from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.customer.validators import email_or_phone_validator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email_or_phone, password=None, role="customer", **extra_fields):
        if not email_or_phone:
            raise ValueError("Users must have an email or phone number")

        user = self.model(
            email_or_phone=email_or_phone,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Safety checks
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email_or_phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("dealer", "Dealer"),
        ("customer", "Customer"),
    )

    email_or_phone = models.CharField(
        max_length=100,
        unique=True,
        validators=[email_or_phone_validator],
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)



    objects = UserManager()

    USERNAME_FIELD = "email_or_phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email_or_phone

    # Helpers
    @property
    def is_email(self):
        return "@" in self.email_or_phone


    def is_phone(self):
        return self.email_or_phone.replace("+", "").isdigit()
