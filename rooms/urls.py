from django.urls import path
from rooms import views


urlpatterns = [
    path('amenites/', views.Amenities.as_view(), name="amenities"),
    path('amenites/<int:amenities_pk>/',
         views.AmenitiesDetail.as_view(), name="amenitiesdetail"),

]
