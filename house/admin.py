from django.contrib import admin
from .models import House
# Register your models here.


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    fields = (
        "name",
        "description",
        ("address", "price",),
        "pets_allowed",
    )

    list_display = (

        "name",
        "address",
        "price",
        "pets_allowed",
    )

    list_filter = (

        "price",
        "pets_allowed",

    )

    search_fields = (
        "name__startswith",
        "address__startswith",
        "price",

    )

    list_display_links = (
        "name",

    )

    # 반려 동물 동반 가능 여부 수정을 리스트에서도 가능.
    list_editable = (
        "pets_allowed",
    )
