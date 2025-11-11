from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from store.serialzers import ProductSerializer
# Create your views here.

@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer=ProductSerializer(query_set,many=True)
    return Response(serializer.data)
@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
