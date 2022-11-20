from django.contrib import admin
from .models import ChatRoom, Message
# Register your models here.


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "chatrooms",
        "participants",
        "__str__",

    )

    # 22.11.20 해결. username과 name.
    search_fields = (
        "chatrooms__name",
        "participants__username",
    )
