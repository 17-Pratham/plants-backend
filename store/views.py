from rest_framework.views import APIView
import json
from django.core.management import call_command
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, Category, Blog
from .serializers import ProductListSerializer,ProductDetailSerializer, CategorySerializer, BlogSerializer


# ✅ All Categories
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ✅ All Products
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetail(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)

            serializer = ProductDetailSerializer(
                product,
                context={'request': request}
            )

            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"})


# ✅ Products by Category (IMPORTANT)
class ProductByCategory(APIView):
    def get(self, request, slug):
        products = Product.objects.filter(
            category__slug=slug,
            is_active=True
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
class BlogList(APIView):
    def get(self, request):
        category = request.GET.get('category')

        blogs = Blog.objects.filter(is_published=True)

        if category:
            blogs = blogs.filter(category=category)

        blogs = blogs.order_by('-created_at')

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
class BlogDetail(APIView):
    def get(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug, is_published=True)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=404)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)

class FeaturedBlog(APIView):
    def get(self, request):
        blog = Blog.objects.filter(featured=True, is_published=True).first()

        if not blog:
            return Response({'message': 'No featured blog'}, status=404)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        parent = self.request.GET.get('parent')
        # print("🔥 PARAM =", parent)

        if parent:
            return Category.objects.filter(parent__slug=parent)

        return Category.objects.all()
    
class ProductsByParentCategory(APIView):
    def get(self, request, slug):
        try:
            parent = Category.objects.get(slug=slug)

            children = Category.objects.filter(parent=parent)

            products = Product.objects.filter(
                category__in=children,
                is_active=True
            )

            serializer = ProductListSerializer(
                products,
                many=True,
                context={'request': request}
            )

            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"})
        
class SearchProducts(APIView):
    def get(self, request):
        query = request.GET.get("q", "")

        # 🔥 case 1: user typing
        if query:
            products = Product.objects.filter(
                Q(title__icontains=query) |
                Q(tag__icontains=query) |
                Q(description__icontains=query)
            ).filter(is_active=True)

        # 🔥 case 2: default (no typing)
        else:
            products = Product.objects.filter(
                is_active=True,
                show_in_search=True
            )

        serializer = ProductListSerializer(products[:10], many=True)

        return Response(serializer.data)
    
def load_data(request):
    call_command('loaddata', 'data.json')
    return JsonResponse({"status": "data loaded"})