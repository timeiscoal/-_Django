from django.db import models
from common.models import CommonModel
# Create your models here.


class ChatRoom(CommonModel):

    name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    participants = models.ManyToManyField(
        'user.User',
    )

    def __str__(self):
        return f"{self.name}"


class Message(CommonModel):

    text = models.TextField(

    )
    participants = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    chatrooms = models.ForeignKey(
        'direct_messages.ChatRoom',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.text[:20]}..."
