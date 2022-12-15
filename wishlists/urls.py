from django.urls import path
from .views import WishlistView, WishListDetailView, WishlistToggleView


urlpatterns = [


    path("", WishlistView.as_view()),
    path("<int:pk>/", WishListDetailView.as_view()),
    path("<int:pk>/rooms/<int:room_pk>/", WishlistToggleView.as_view())


]
