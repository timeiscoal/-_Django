from django.urls import path, include
from experiences import views

urlpatterns = [

    path("perk/", views.PerkView.as_view(), name="PerkView"),
    path("perk/<int:perk_id>/", views.PerkDetailView.as_view(),
         name="PerkDetailView"),


]
