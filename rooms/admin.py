from django.contrib import admin
from .models import Room, Amenity


# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "category",
        "city",
        "price",
        "toilets",
        "kind",
        "total_amenitese"

    )
    list_filter = (

        "country",
        "city",
        "price",
        "kind",
        "amenities",
    )


@admin.register(Amenity)
class Amenity(admin.ModelAdmin):

    list_display = (

        "description",
        "updated_at",

    )
