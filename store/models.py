from django.db import models

# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ================= PRODUCT =================
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    tag = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)

    # 🔥 Detailed content
    about_product = models.TextField(blank=True)

    rating = models.FloatField(default=0)

    # ✅ PRICE LOGIC
    price = models.DecimalField(max_digits=10, decimal_places=2)

    has_discount = models.BooleanField(default=False)  # 🔥 NEW

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    discount_percentage = models.IntegerField(
        null=True,
        blank=True
    )

    badge_text = models.CharField(max_length=50, blank=True, null=True)

    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 PREMIUM FIELDS
    delivery_info = models.CharField(max_length=150, blank=True)
    shipping_info = models.CharField(max_length=150, blank=True)
    return_policy = models.CharField(max_length=150, blank=True)

    whats_included = models.TextField(blank=True)
    show_in_search = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
def clean(self):
    from django.core.exceptions import ValidationError

    if self.has_discount:
        if not self.old_price:
            raise ValidationError("Old price required when discount is enabled")

        if not self.discount_percentage:
            raise ValidationError("Discount % required when discount is enabled")

    else:
        self.old_price = None
        self.discount_percentage = None

# ================= PLANT SPEC =================
class PlantSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='plant_spec')

    sunlight = models.CharField(max_length=50, blank=True)
    water = models.CharField(max_length=50, blank=True)
    humidity = models.CharField(max_length=50, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)

    pet_friendly = models.BooleanField(default=False)
    height = models.CharField(max_length=50, blank=True)
    pot_included = models.BooleanField(default=True)

    # 🌿 benefits
    air_purifying = models.BooleanField(default=False)
    low_maintenance = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title} - Plant Spec"


# ================= POT SPEC =================
class PotSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='pot_spec')

    material = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)
    drainage = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.title} - Pot Spec"


# ================= CARE PRODUCT SPEC =================
class CareProductSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='care_spec')

    usage = models.TextField(blank=True)
    weight = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.product.title} - Care Spec"


# ================= BLOG =================
class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('indoor', 'Indoor Plants'),
        ('outdoor', 'Outdoor Plants'),
        ('care', 'Plant Care'),
        ('tips', 'Gardening Tips'),
        ('services', 'Garden Services'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,default='tips')
    tags = models.CharField(max_length=150, blank=True)

    short_description = models.TextField()
    content = models.TextField()  # later rich text kar sakte hai

    image = models.ImageField(upload_to='blog_images/')
    featured = models.BooleanField(default=False)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# ================= FAQ =================
class ProductFAQ(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='faqs'
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.title} - {self.question}"