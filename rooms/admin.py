from django.contrib import admin
from .models import Room, Amenity

# 22.11.20


@admin.action(description="선택한 방의 가격을 0으로 조정하기")
def reset_prices(models_admin, request, rooms):

    for room in rooms.all():
        room.price = 0
        room.save()

    # Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    # Not String
    actions = (
        reset_prices,
    )

    list_display = (
        "name",
        "country",
        "category",
        "city",
        "price",
        "toilets",
        "kind",
        "total_amenitese",
        "rating",

    )
    list_filter = (

        "country",
        "city",
        "price",
        "kind",
        "amenities",
    )

    # 22.11.20
    search_fields = (
        "name__startswith",
        "price",
        "owner__name",
        "country",
    )


@admin.register(Amenity)
class Amenity(admin.ModelAdmin):

    list_display = (

        "description",
        "updated_at",

    )
