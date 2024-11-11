from django.shortcuts import get_object_or_404
import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .seralizers import ProductSerializer


# Create your views here.
# takes request returns response


@api_view()
def product_list(request):
    queryset = Product.objects.all()
    seralizer = ProductSerializer(queryset, many=True)
    return Response(seralizer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
