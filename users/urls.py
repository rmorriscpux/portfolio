from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.user_profile),
    path('register/', views.register_page),
    path('register/create/', views.create),
    path('login/', views.login_page),
    path('login/verify/', views.login_verify),
    path('add_credit/', views.add_credit),
    path('edit/', views.modify),
    path('edit/update/', views.update),
    path('destroy/', views.destroy),
]

if settings.DEBUG:
    urlpatterns.extend([
        path('test/', views.test),
        path('test/post/', views.test_post),
    ])