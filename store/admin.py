from django.contrib import admin
from .models import Category, ProductFAQ, Product,Blog, PlantSpecification, PotSpecification, CareProductSpecification
from .forms import ProductFAQBulkForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock','badge_text', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    # 🔥 IMPORTANT: only subcategories show
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.exclude(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'featured',
        'is_published',
        'created_at',
    )

    list_filter = ('category', 'featured', 'is_published')
    search_fields = ('title', 'tags')

    prepopulated_fields = {'slug': ('title',)}

    ordering = ('-created_at',)




@admin.register(ProductFAQ)
class ProductFAQAdmin(admin.ModelAdmin):
    form = ProductFAQBulkForm
    list_display = ('product', 'question', 'order')

    def save_model(self, request, obj, form, change):
        product = form.cleaned_data['product']

        for i in range(1, 5):
            q = form.cleaned_data.get(f'question_{i}')
            a = form.cleaned_data.get(f'answer_{i}')

            if q and a:
                ProductFAQ.objects.create(
                    product=product,
                    question=q,
                    answer=a,
                    order=i
                )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PlantSpecification)
admin.site.register(PotSpecification)
admin.site.register(CareProductSpecification)