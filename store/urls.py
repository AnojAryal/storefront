from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from pprint import pprint


router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
pprint(router.urls)


# URLConfig
urlpatterns = router.urls
