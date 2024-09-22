from rest_framework import generics, views, serializers
from olcha import serializer
from rest_framework.response import Response
from olcha.models import Category, Group, Product
from rest_framework import status
from django.http import Http404

# Create your views here.

class CategoriesDetailListApiView(generics.ListCreateAPIView):
    queryset = Category.objects.prefetch_related('groups__products').all()
    serializer_class = serializer.CategoriesGroupsProductsSerializer


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.CategoriesGroupsProductsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.prefetch_related('groups__products').all()

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Detail(views.APIView):
    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404()

    def get(self, request, slug, serializer=None):
        product = self.get_object(slug)
        serializer = serializer.ProductDetailSerializer(product)
        return Response(serializer.data)

    def delete(self, request, slug):
        product = self.get_object(slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupDetailListApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        group_slug = self.kwargs.get('slug')
        return Group.objects.prefetch_related('products').filter(
            slug=group_slug
        )

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ProductDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return Product.objects.get(slug=slug)

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset
        except Product.DoesNotExist:
            raise Http404("Not found.")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAddView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('id')[:1]
    serializer_class = serializer.ProductSerializer