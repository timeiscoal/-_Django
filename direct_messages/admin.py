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

    search_fields = (
        "chatrooms__name",
        # "participants", 추후 구현. 채팅에 참여하는 유저 이름을 검색하면 해당 채팅창이 나오게 구성.
    )
