from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from perfil import views
from rest_framework import routers, permissions
from market.views import ProductViewSet, create_preference
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register("products", ProductViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Mercadito API",
        default_version="v1",
        description="API para manejar productos de Mercadito (compra, venta, trueque).",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ejemplo@ejemplo.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path("", home, name="home"),
    path("market/", include("market.urls")),  # mercado
    path("accounts/", include("allauth.urls")),  # login/signup
	path("accounts/", include("allauth.urls")),  # allauth
    path("productos/", include("market.urls")),  # users
	path("profiles/", include("perfil.urls")),	 # profiles
    path("editar/", views.edit_profile, name="edit_profile"),
    path("ver_perfil/", views.profile_view, name="profile"),
    path("ai/", include("market_ai.urls", namespace="market_ai")),
    #   path("api/", include(router.urls)),
    path("pago/<int:product_id>/", create_preference, name="crear-preferencia"),
    # duplicado ¿
    path("", include("presence.urls")),
    path("presence/", include("presence.urls", namespace="presence")),
    path("chat/", include("simple_chat.urls", namespace="simple_chat")),
    path("quotes/", include("quotes.urls", namespace="quotes")),

    # Swagger endpoints
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

