from django.db import models
from base.models import BaseModole
from autoslug import AutoSlugField


class Category(BaseModole):
    category_name = models.CharField(max_length=100, unique=True , blank= True , null=True )
    slugField = AutoSlugField(populate_from='category_name' ,unique=True, blank=True, null=True)
    category_image = models.ImageField(upload_to='category',blank=True, null=True)

    def __str__(self):
        return self.category_name

class SubCategory(BaseModole):
    
    subcategory_name = models.CharField(max_length=100, unique=True)
    slugField = AutoSlugField(populate_from='subcategory_name', unique=True, blank=True, null=True)
    subcategory_image = models.ImageField(upload_to='subcategory',blank=True, null=True)

    def __str__(self) -> str:
        return self.subcategory_name

class Size_variations(BaseModole):
    Size_name  = models.CharField(max_length=100)
    Size_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.Size_name

class color_variations(BaseModole):
    color_name = models.CharField(max_length=100)
    color_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name


class Product(BaseModole):
   
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_cat", blank=True, null=True)
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    product_name = models.CharField(max_length=100)
    slugField = AutoSlugField(populate_from='get_slug_source', unique=True, blank=True, null=True)
    product_Brand = models.CharField(max_length=100,blank=True, null=True)
    product_artical = models.CharField(max_length=100 ,blank=True, null=True)
    product_price = models.IntegerField()
    product_dicount = models.IntegerField( default= 20 )
    product_Size = models.ManyToManyField(Size_variations,blank=True )
    product_color = models.ManyToManyField(color_variations,blank=True,)
    product_decribstion = models.TextField()

    def get_slug_source(self):
        return f"{self.product_name}-{self.product_Brand or ''}-{self.product_artical or ''}"
    
    @property
    def discounted_price(self):
        if self.product_dicount > 0:
            discount_amount = (self.product_dicount / 100) * self.product_price
            discounted_price = self.product_price - discount_amount
            return discounted_price
        else:
            return self.product_price

    def __str__(self) -> str :
        return f"{str(self.udid, )}, {(self.product_name)}, {(self.product_Brand), {(self.product_artical)}} "

    
  
    
class ProductImage(BaseModole):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product', blank=True, null=True)