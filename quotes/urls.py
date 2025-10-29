from django.urls import path
from .views import request_quote

app_name = "quotes"
urlpatterns = [
    path("solicitar/<int:product_id>/", request_quote, name="request-quote"),
]