from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import Http404
from olcha.models import Product, AttributeKey, AttributeValue
from olcha.serializer import (
    ProductSerializer,
    ProductDetailSerializer,
    AttributeKeySerializer,
    AttributeValueSerializer,
)
from olcha.permission import IsOwnerOrReadOnly


class ProductsListApiView(generics.ListCreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs.get(self.lookup_field))

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'request': self.request}

    def get_object(self):
        queryset = self.get_queryset()
        if queryset.exists():
            return queryset.first()
        raise Http404("Product not found.")

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAddView(generics.CreateAPIView):
    serializer_class = ProductSerializer


class AttributeKeyListApiView(generics.ListCreateAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeValueListApiView(generics.ListCreateAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
