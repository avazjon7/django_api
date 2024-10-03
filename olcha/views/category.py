from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from olcha.models import Category
from olcha.serializer import CategoriesGroupsProductsSerializer
from olcha.permission import IsOwnerOrReadOnly


class CategoriesDetailListApiView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related('groups__products').all()
    serializer_class = CategoriesGroupsProductsSerializer


class CategoryDetailApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CategoriesGroupsProductsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.prefetch_related('groups__products').all()

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAddView(generics.CreateAPIView):
    serializer_class = CategoriesGroupsProductsSerializer
