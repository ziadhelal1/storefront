from ast import With
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from store.serialzers import ProductSerializer
from django.db.models import Q
from django.db.models import F
# Create your views here.

@api_view()
def product_list(request):
    # this n+1 problem 
    # this is very heavy operation
    # query_set = Product.objects.all()
    # for product in query_set:
    #     print(product.title, product.Collection.title)

    # and this is solution of n+1 problem
    # here just one query is executed
    query_set = Product.objects.select_related('Collection').all()
    for product in query_set:
        print(product.title, product.Collection.title)
    serializer=ProductSerializer(query_set,many=True)


    # Build filter query without  using Q() expression.

    Product.objects.filter(price__gt=50, Collection_id=1)
    # Build dynamic filter query using Q() expression.
    Product.objects.filter(Q(price__gt=50) & Q(Collection_id=1))
    # This Update fetches all products into Python and then saves them one by one.
    for product in Product.objects.all():
        product.price += 10
        product.save()
    # Update any field values directly in SQL using F() expression.
    Product.objects.update(price=F('price') + 10)


    # if we want to fetch all products
    products = Product.objects.all()

    # Optimize query to fetch only specific fields.
    products = Product.objects.only('title', 'price')

    # optimize query to defer loading of large text fields.
    products = Product.objects.defer('description')
    # With only() → SQL has fewer selected columns.
    # With defer() → SQL selects all except deferred ones.


    # Using values() to fetch dictionaries instead of model instances.
    # Efficient because Django does not create model instances, just fetches raw data.
    queryset_usingval = Product.objects.all().values('id', 'title', 'price')


    # Using values_list() to fetch tuples instead of model instances.
    # More efficient for simple lists of values.
    queryset_usingvalist = Product.objects.all().values_list('title', 'price')


    # now i alter the price to be this to apply indexing in price coulmn 
    # and the apply migration
    # price = models.DecimalField(max_digits=6, decimal_places=2,db_index=True)
    count = Product.objects.filter(price__gt=1000).count()



    countafterindexing = Product.objects.filter(price__gt=1000).count()

#  the deffienece between count and countafterindexing is that
# before indexing the query took more time to execute because it had to scan the entire table

    return Response(serializer.data)
# Initially, I used Product.objects.all() which executed one query for products, and one additional query per product to fetch the related collection — causing N+1 queries.

# After using select_related('Collection'), Django performed a single SQL JOIN query to fetch both products and their collections together.

# I verified this improvement using Django Debug Toolbar (query count reduced from N+1 to 1).
@api_view()
def product_detail(request, pk):

    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
