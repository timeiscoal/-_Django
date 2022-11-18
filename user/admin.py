from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
# fieldsets는 section을 만들 수 있다.


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        ("프로필",

         {"fields": (
             ("username", "profile_photo"),
             "password",
             ("name", "gender"),
             "email",
             "is_host",
             ("language", "currency"),

         ),
         },
         ),

        ("Permissions",
         {
             "fields": (
                 "is_active",
                 "is_staff",
                 "is_superuser",
                 "groups",
                 "user_permissions",
             ),
         },

         ),

        ("Important Dates",
         {
             "fields": (
                 "last_login",
                 "date_joined",
             ),
         },
         ),
    )

    list_display = (

        "username",
        "email",
        "name",
        "is_host",
    )
