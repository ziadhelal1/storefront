from rest_framework import serializers
from .models import Product, Customer, Order, Collection
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'inventory', 'last_updated', 'Collection']