from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('bugs/', views.bugs),
    path('bugs/critter_info/', views.bugs_info),
    path('fish/', views.fish),
    path('fish/critter_info/', views.fish_info),
    path('sea_creatures/', views.sea_creatures),
    path('sea_creatures/critter_info/', views.sea_creatures_info),
]