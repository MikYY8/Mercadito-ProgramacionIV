from django.urls import path
from . import views

app_name = "simple_chat"
urlpatterns = [
    path("comparar/<str:nombre>/", views.CompararPrecios),
]