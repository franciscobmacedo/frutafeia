from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("produtores", views.ProdutorViewSet)
router.register("produtos", views.ProdutoViewSet)
router.register("familiaproduto", views.FamiliaProdutoViewSet)
router.register("disponibilidades", views.DisponibilidadeViewSet)
router.register("ranking", views.RankingViewSet)
router.register("mapasdecampo", views.MapasDeCampoViewSet)


app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "getdisponibilidades",
        views.getDisponibilidades.as_view(),
        name="get_disponibilidades",
    ),
    path(
        "getprodutores",
        views.getProdutores.as_view(),
        name="get_produtores",
    ),
    path(
        "getprodutos",
        views.getProdutos.as_view(),
        name="get_produtos",
    ),
    path(
        "tipoprodutos",
        views.tipoProdutos.as_view(),
        name="tipo_produtos",
    ),
    path(
        "estadoprodutor",
        views.estadoProdutor.as_view(),
        name="estado_produtor",
    ),
    path(
        "medida",
        views.medida.as_view(),
        name="medida",
    ),
]
