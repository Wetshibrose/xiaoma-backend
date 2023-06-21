from uuid import uuid4, UUID
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.utils import timezone

from countries.models import Country
from genders.models import Gender


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str = None, phone_number: str = None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError(
                "Either Email or phone number needs to be provided")

        if email and phone_number:
            email = self.normalize_email(email)
            user: CustomUser = self.model(
                email=email, phone_number=phone_number, **extra_fields)
        elif email:
            email = self.normalize_email(email)
            user: CustomUser = self.model(email=email, **extra_fields)
        else:
            user: CustomUser = self.model(
                phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email: str = None, phone_number: str = None, password=None, otp_code: str = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email=email, phone_number=phone_number, password=password, otp_code=otp_code, **extra_fields,)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        default_related_name = "users"
        indexes = [
            models.Index(fields=["id", "email", "phone_number", "is_online"],)
        ]
        ordering = ["-created_at"]
        permissions = (
            ("can_change_ratings_user", "Can edit user"),
        )
        verbose_name = "user"
        verbose_name_plural = "users"

    id = models.UUIDField(default=uuid4, primary_key=True,
                          editable=False, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, unique=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    cor = models.ForeignKey(verbose_name="country_of_origin",
                            to=Country, on_delete=models.PROTECT, null=True)
    ratings = models.DecimalField(decimal_places=1, max_digits=3, default=0)
    is_online = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ["email",]

    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
