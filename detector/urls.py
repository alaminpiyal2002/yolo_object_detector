from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("download/<str:filename>/", views.download_result, name="download_result"),
]