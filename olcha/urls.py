from django.urls import path
from olcha import views

urlpatterns = [
    path('', views.CategoriesDetailListApiView.as_view(), name='categories_detail_list'),
    path('category/<slug:slug>/', views.CategoryDetailApiView.as_view(), name='category_detail'),
    path('category/<slug:category_slug>/<slug:slug>/', views.GroupDetailListApiView.as_view(),name='group_detail'),
    path('product/view/<slug:slug>/', views.ProductDetailApiView.as_view(), name='product_detail'),
    path('add-product/', views.ProductAddView.as_view(), name='add_product'),
]