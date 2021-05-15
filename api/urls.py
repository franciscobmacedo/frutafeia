from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("produtores", views.ProdutorViewSet)
router.register("produtos", views.ProdutoViewSet)
router.register("disponibilidades", views.DisponibilidadeViewSet)


app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "getdisponibilidades",
        views.getDisponibilidades.as_view(),
        name="get_disponibilidades",
    ),
]
