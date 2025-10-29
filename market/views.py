from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from rest_framework import viewsets
from rest_framework import permissions
from .models import Product
from .serializers import ProductSerializer
import mercadopago
from django.conf import settings
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.filter(active=True).order_by("-created_at")
    return render(request, "product_list.html", {"products": products})

# Crear producto
@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("product-list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

# Editar producto
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product-list")
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form})

# Eliminar producto
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.active = False
        product.save()
        return redirect("product-list")
    return render(request, "product_confirm_delete.html", {"product": product})

#Para Swagger / Redoc
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# añadir al carrito
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += 1
    item.save()
    return redirect("view-cart")

# ver carrito
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})

# lo de MP
def create_preference(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": product.title,
                "quantity": 1,
                "unit_price": float(product.price),
                "currency_id": "ARS",
            }
        ],
        "back_urls": {
        "success": "https://www.google.com",   # temporal para test
        "failure": "https://www.google.com",
        "pending": "https://www.google.com",
        },
        # "back_urls": {
        #     "success": request.build_absolute_uri("/pago-exitoso/"),
        #     "failure": request.build_absolute_uri("/pago-fallido/"),
        #     "pending": request.build_absolute_uri("/pago-pendiente/"),
        # },
        "auto_return": "approved",
    }

    preference = sdk.preference().create(preference_data)

    # Log completo en consola Django
    print("MercadoPago response:", preference)

    if preference["status"] != 201:  # 201 es éxito en MP
        return JsonResponse({
            "error": "No se pudo crear la preferencia",
            "detalle": preference
        }, status=400)

    return JsonResponse({"init_point": preference["response"]["init_point"]})