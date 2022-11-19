from django.db import models
from common.models import CommonModel


# Create your models here.

class Category(CommonModel):

    class CategoryKindChoices(models.TextChoices):
        ROOM = ("rooms", "Rooms")
        EXPERIENCE = ("experiences", "Experiences")

    name = models.CharField(
        max_length=100,
    )
    kind = models.CharField(
        max_length=15,
    )

    def __str__(self):
        return f"{self.kind.title()}:{self.name}"

    class Meta:
        verbose_name_plural = "Categories"
