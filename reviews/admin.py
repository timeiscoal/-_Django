from django.contrib import admin
from .models import Review
# Register your models here.


# 22.11.20
class WordFilter(admin.SimpleListFilter):

    title = "Filter by words"

    parameter_name = "word"

    def lookups(self, request, models_admin):
        return [
            ("최고", "최고"),
            ("grate", "Grate"),
            ("wow", "WoW"),
        ]

    def queryset(self, request, reviews):
        choice = self.value()
        if choice == None:
            return reviews.all()
        elif choice == "최고":
            return reviews.filter(rating__lt=100)
        elif choice == "grate" or "wow":
            return reviews.filter(payload__contains=choice)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )
