from multiprocessing import context
from django.shortcuts import get_object_or_404
import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .seralizers import ProductSerializer


# Create your views here.
# takes request returns response


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related("collection").all()
        seralizer = ProductSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(seralizer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response("OK")


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response("Ok")
