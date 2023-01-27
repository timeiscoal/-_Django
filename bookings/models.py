from django.db import models
from common.models import CommonModel
# Create your models here.


class Booking(CommonModel):

    class BookingKindChoice(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    kind = models.CharField(
        max_length=20,
        choices=BookingKindChoice.choices
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    # 예약 시 한 개의 방만 가능.
    # 방은 여러개의 예약이 가능.
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    # 체험 예약 또한 마찬가지로 구성.
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )

    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField(

    )

    # def __str__(self):
    #     return self.user
