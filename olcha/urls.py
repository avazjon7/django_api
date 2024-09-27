from django.urls import path
from olcha.views import category, group, product, product_attr

urlpatterns = [
    path('categories/', category.CategoryList.as_view()),
    path('group/', group.GroupList.as_view()),
    path('categories/detail/<int:pk>/', category.CategoryDetailApiView.as_view()),
    path('groups/detail/<int:pk>/', group.GroupDetailApiView.as_view()),
    path('products/', product.ProductCreate.as_view()),
    path('products/detail/<slug:slug>/', product.ProductDetail.as_view()),

    path('product/productattributes/', product_attr.ProductAttributesApi.as_view()),
    path('product/productattributes/detail/<int:pk>/', product_attr.ProductAttributeDetail.as_view()),

    path('product/attributevalues/', product_attr.AttributeValueApiView.as_view()),
    path('product/attributevalues/detail/<int:pk>/', product_attr.AttributeValueDetail.as_view()),

    path('product/attributekeys/', product_attr.AttributeKeyApiView.as_view()),
    path('product/attributekeys/detail/<int:pk>/', product_attr.AttributeKeyDetail.as_view()),

]