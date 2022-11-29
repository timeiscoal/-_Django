from django.db import models
from common.models import CommonModel
# Create your models here.


class Experience(CommonModel):

    class CountryChoices(models.TextChoices):
        DF = ("default", "나라 선택하기")
        KO = ("ko", "한국")
        USA = ("usa", "미국")
        JP = ("japan", "일본")

    country = models.CharField(
        max_length=150,
        default="default",
        choices=CountryChoices.choices,
    )

    city = models.CharField(max_length=100, default="서울",)
    name = models.CharField(max_length=200,)
    host = models.ForeignKey("user.User", on_delete=models.CASCADE,)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250,)
    start_at = models.TimeField(help_text="영업 시작 시간")
    end_at = models.TimeField(help_text="영업 종료 시간")
    description = models.TextField(

    )
    perk = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


# 특전
class Perk(CommonModel):

    name = models.CharField(max_length=100,)
    details = models.CharField(max_length=250,)
    explanation = models.TextField()

    def __str__(self):
        return self.name
