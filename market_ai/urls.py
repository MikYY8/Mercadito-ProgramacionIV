from django.urls import path
from . import views

app_name = "market_ai"

urlpatterns = [
    path("price-suggest/", views.price_suggest, name="price-suggest"),
    path("chat/", views.ai_chat, name="ai-chat"),
    path("recommend/<int:pk>/", views.recommend_similar, name="recommend-similar"),
]