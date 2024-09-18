from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from book.models import Book
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# class UserList(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, format=None):
#         data = [
#             {
#                     user.username: {
#                     'username':user.username,
#                     'is_active':user.is_active,
#                     'is_superuser':user.is_superuser,
#                     'password':user.password
#                 }
#             }
#             for user in User.objects.all()
#         ]
#
#         return Response(data,status=status.HTTP_200_OK)

class BookList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        books = Book.objects.all()
        data = {
                book.title: {
                "book_id": book.id,
                "author": book.author,
                "title": book.title,
                "published": book.published_date,
                "description": book.description,
                }
        for book in books
        }

        return Response(data)
