from django.urls import path
from rooms import views


urlpatterns = [
    path("", views.RoomView.as_view(), name="rooms"),
    path("<int:room_id>/", views.RoomDetailView.as_view(), name="roomDetail"),
    path("<int:room_id>/reviews/",
         views.RoomReviews.as_view(), name="roomReview"),
    path("<int:room_id>/photos/",
         views.RoomPhotos.as_view(), name="roomPhotos"),
    path('amenites/', views.Amenities.as_view(), name="amenities"),
    path('amenites/<int:amenities_pk>/',
         views.AmenitiesDetail.as_view(), name="amenitiesdetail"),

]
