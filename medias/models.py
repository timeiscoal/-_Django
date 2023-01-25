from django.db import models
from common.models import CommonModel
# Create your models here.


# 사진은 방 또는 활동에 올라간다
# 그렇기 때문에 둘 다 올라가지 않을 경우가 있기 때문에 이와 같이 속성을 넣었다.

class Photo(CommonModel):

    file = models.URLField(
        null=True,
        blank=True,

    )
    description = models.CharField(
        max_length=150,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,

    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.room.name} : {self.experience.name}"

# 에어비엔비를 참조하여 방에는 따로 영상이 올라가지 않았고, 활동에만 , 단 하나의 영상만 게시 되어있음을 참조하여 구조를 만듬.


class Video(CommonModel):

    file = models.URLField(
        null=True,
        blank=True,

    )
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",

    )

    def __str__(self) -> str:
        return f"{self.experience.name} : {self.file.name}"
