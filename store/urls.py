from django.urls import path
from rest_framework_nested import routers
from . import views
from pprint import pprint


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)


pprint(router.urls)


products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

# URL Configuration
urlpatterns = router.urls + products_router.urls
