import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField

from app.enums import UserType


class UserManager(BaseUserManager):
    def create_participant(
        self, email, name, surname, password
    ):
        if not email:
            raise ValueError("A user must have an email")

        user = self.model(
            email=email,
            name=name,
            surname=surname,
            type=UserType.PARTICIPANT.value,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email,
        name,
        surname,
        type=UserType.PARTICIPANT.value,
        password=None,
        language="en",
    ):
        if not email:
            raise ValueError("A user must have an email")

        user = self.model(
            email=email, name=name, surname=surname, type=type, language=language
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password):
        user = self.create_user(
            email, name, surname, UserType.ORGANISER.value, password
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(verbose_name="First name", max_length=255)
    surname = models.CharField(verbose_name="Last name", max_length=255)

    email_verified = models.BooleanField(default=False)
    verify_key = models.CharField(max_length=127, blank=True, null=True)
    verify_expiration = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    type = models.PositiveSmallIntegerField(
        choices=((u.value, u.name) for u in UserType),
        default=UserType.PARTICIPANT.value,
    )

    language = models.CharField(max_length=2, default="en")

    # Personal information
    picture = VersatileImageField(
        "Image", upload_to="files/user"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    @property
    def full_name(self):
        return self.name + " " + self.surname

    @property
    def is_staff(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.full_name


class Message(models.Model):
    content = models.TextField(max_length=1000)
    language = models.CharField(max_length=2, default="en")
    tags = models.TextField(max_length=1000, default="")

    deleted = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    image = VersatileImageField(
        "Image", upload_to="files/message"
    )
    image_tags = models.TextField(max_length=1000, default="")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
