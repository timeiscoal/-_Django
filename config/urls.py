from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', include("categories.urls")),
    path('rooms/', include("rooms.urls")),
    path('experiences/', include("experiences.urls")),
    path("medias/", include("medias.urls")),
    path("wishlist/", include("wishlists.urls")),
    path("users/", include("user.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('categories/', include("categories.urls")),
#     path('rooms/', include("rooms.urls")),
#     path('experiences/', include("experiences.urls")),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 이렇게 +static의 방식은 보안상 문제가 발생할 수 있어서 개발단계에서만 진행하기를 권장하고 있다. 이는 신뢰할수 없는 유저에게서 업로드된 콘텐츠가 올라 갈 수 있기 때문이다.

# 파일을 호스팅하는 서버에 파일을 넣고, 다음에 장고에게는 URL을 제공하는 방식으로 진행하자.
# 그래서 모델의 변경이 필요하다.
