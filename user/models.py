from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):

    '''  User model definition   '''

    class GenderChoices(models.TextChoices):
        MALE = ("male", "남자")
        FEMAIL = ("female", "여자")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "한국어")
        EN = ("en", "영어")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "원")
        USD = ("usd", "달러")

    first_name = models.CharField(
        max_length=150,
        blank=True,
        editable=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        editable=True,
    )
    name = models.CharField(
        max_length=100,
        default=""
    )
    is_host = models.BooleanField(
        default=False,
    )

    profile_photo = models.ImageField(
        null=True,
        blank=True,
        help_text="프로필 사진을 추가 해보세요",
        verbose_name="프로필 사진"
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=10,
        choices=CurrencyChoices.choices,
    )
