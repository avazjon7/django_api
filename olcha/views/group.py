from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from olcha.models import Group
from olcha.serializer import GroupSerializer


class GroupDetailListApiView(generics.GenericAPIView):
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Group.objects.prefetch_related('products').filter(
            slug=self.kwargs.get(self.lookup_field)
        )

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupAddView(generics.CreateAPIView):
    serializer_class = GroupSerializer
