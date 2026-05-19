from django.urls import path
from .views import (
    CategoryList,
    ProductList,
    ProductByCategory,
    BlogList,
    CategoryListView,
    ProductsByParentCategory,
    ProductDetail,
    FeaturedBlog,
    BlogDetail,
    SearchProducts,
    load_data
)

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('categories/filter/', CategoryListView.as_view()),
    path('products/', ProductList.as_view()),
    path('products/category/<slug:slug>/', ProductByCategory.as_view()),
    path('products/by-parent/<slug:slug>/', ProductsByParentCategory.as_view()),
    path('products/detail/<slug:slug>/', ProductDetail.as_view()),
    path('blogs/', BlogList.as_view()),
    path('blogs/featured/', FeaturedBlog.as_view()),
    path('blogs/<slug:slug>/', BlogDetail.as_view()),
    path("search/", SearchProducts.as_view()),
    path('load-data/', load_data),
]