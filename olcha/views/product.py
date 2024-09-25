from rest_framework.generics import ListCreateAPIView, ListAPIView

from olcha.models import Product, Image
from olcha.serializer import ProductSerializer, ImageSerializer


class ProductListApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageListApiView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer