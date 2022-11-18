from django.db import models

# Create your models here.

# 모델은 어플리케이션에서 데이터의 모양을 묘사하는 것이다.
# 모델로 데이터를 설명할 수 있어야 한다.
# 어떤 종류의 데이터이고 , 다른 앱들과는 어떤 상호작용을 할 수 있는가.
# PositiveIntegerField() 양수만.


class House(models.Model):

    '''   House model Definition   '''

    name = models.CharField(
        max_length=100,
    )
    price = models.PositiveIntegerField(
        help_text="하루 이용 금액",
    )
    description = models.TextField(

    )
    address = models.CharField(
        max_length=150,
    )
    pets_allowed = models.BooleanField(
        verbose_name="반려동물 동반 가능 여부",
        help_text="반려동물 동반 가능하면 체크하세요.",
        default=True,
    )

    # 집 주인 계정이 삭제되면 같이 삭제.
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,

    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name
