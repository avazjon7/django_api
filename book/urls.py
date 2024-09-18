from django.urls import path, include

from book import admin
# from book.views import UserList
from book.views import BookList


urlpatterns = [
    # path('all/users/',UserList.as_view(), name='index')
    path('all/books/',BookList.as_view(), name='book_list'),
    # path('admin/', admin.site.urls),
]
