from django.db import models

# Create your models here.


class CommonModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # DB에 저장되지 않게 지정.
    # abstract을 통해서 model이 DB에서 실제 데이터로 사용되지 않음을 지정
    class Meta:
        abstract = True
