from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from user.serializer import UserSerializer
from rest_framework import generics

class UserRegisterApiView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        return user

class UserLogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:

            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
