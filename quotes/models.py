from django.db import models
from django.conf import settings
from market.models import Product

class QuoteRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)