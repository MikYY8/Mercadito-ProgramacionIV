from . import views
from django.contrib import admin
from django.urls import path, include
from .views import product_list, product_create

urlpatterns = [
    path("lista/", product_list, name="product-list"),
    path("nuevo/", product_create, name="product-create"),

    path("", views.product_list, name="productlist"),
    path("create/", views.product_create, name="product-create"),
    path("edit/<int:pk>/", views.product_edit, name="product-edit"),
    path("delete/<int:pk>/", views.product_delete, name="product-delete"),
    path("cart/", views.view_cart, name="view-cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add-to-cart"),

    # Mercado Pago
    path("pago/<int:product_id>/", views.create_preference, name="crear-preferencia"),
    # duplicado ¿
    path("pago-carrito/", views.create_preference, name="crear-preferencia-carrito"),
]
