from quiz import views as api_views
from django.urls import path

urlpatterns = [
    path("", api_views.index, name="index"),
]