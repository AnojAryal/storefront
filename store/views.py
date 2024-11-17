from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django.http import HttpResponse
import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer


# Create your views here.
# takes request returns response


# class based view
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        seralizer = ProductSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(seralizer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with order item."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based view
@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        seralizer = CollectionSerializer(
            queryset,
            many=True,
        )
        return Response(seralizer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=pk
    )
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serailizer = CollectionSerializer(collection, data=request)
        serailizer.is_valid(raise_exception=True)
        serailizer.save()
        return Response(serailizer.data)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "collection cant be deleted because it includes on eor more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
