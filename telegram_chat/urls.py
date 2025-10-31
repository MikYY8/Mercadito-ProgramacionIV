from django.urls import path, include
from . import views

app_name = 'telegram_chat'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path("chat/api/post/", views.post_message, name="post_message"),
    
    # path('webhook/', views.telegram_webhook, name='telegram_webhook'),
]