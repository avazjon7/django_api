from rest_framework import generics
from olcha.models import ProductAttribute, AttributeKey, AttributeValue
from olcha.serializer import (
    ProductAttributeSerializer,
    AttributeKeySerializer,
    AttributeValueSerializer
)

# Generic base class to reduce repetition
class BaseListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'pk'


class BaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'


# Product Attribute views
class ProductAttributesApi(BaseListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductAttributeDetail(BaseRetrieveUpdateDestroyAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


# Attribute Key views
class AttributeKeyApiView(BaseListCreateAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeKeyDetail(BaseRetrieveUpdateDestroyAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


# Attribute Value views
class AttributeValueApiView(BaseListCreateAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class AttributeValueDetail(BaseRetrieveUpdateDestroyAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
