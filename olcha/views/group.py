from rest_framework import status, generics, mixins
from rest_framework.response import Response
from olcha.models import Group
from olcha.serializer import GroupSerializer

# List and Create API for Group
class GroupList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {'success': True, 'message': 'Group created successfully', 'data': response.data},
                status=status.HTTP_201_CREATED
            )
        return response


# Retrieve, Update, and Delete API for Group
class GroupDetailApiView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        # Directly use retrieve() as get_object handles object not found
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Use update() directly; status code will be set automatically
        response = self.update(request, *args, **kwargs)
        return Response({'success': True, 'message': 'Group updated successfully', 'data': response.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Perform delete using the standard destroy() method
        response = self.destroy(request, *args, **kwargs)
        return Response({'success': True, 'message': 'Group deleted successfully'}, status=status.HTTP_200_OK)
