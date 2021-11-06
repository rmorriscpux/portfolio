from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [

]

if settings.DEBUG:
    urlpatterns.extend([
    path('test/', views.test),
    ])