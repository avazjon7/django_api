from django.urls import path

from olcha import views

urlpatterns = [
    path('category', views.CategoryListApiView.as_view(), name='category-list'),
    path('product-detail/<int:pk>/', views.ProductDetailApiView.as_view(), name='product_detail'),
    path('category-detail/<int:pk>/', views.CategoryDetailApiView.as_view(), name='category_detail'),
    path('group-detail/<int:pk>/', views.GroupDetailListApiView.as_view(), name='group_detail'),
]