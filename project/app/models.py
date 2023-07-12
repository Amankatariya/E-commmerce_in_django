from collections.abc import Iterable
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



# Create your models here.
class slider(models.Model):
        DISCOUNT_DEAL=(
        ('HOT DEALS', 'HOT DEALS'),
        ( 'New Arrsivels', 'New Arrsivels'),
        )   
        image=models.ImageField(upload_to='media/slider_img')
        discount_deal= models.CharField(choices=DISCOUNT_DEAL,max_length=100)
        SALE=models.IntegerField()
        brand_name=models.CharField(max_length=200)
        discount=models.IntegerField()
        link=models.CharField(max_length=200)


        def __str__(self) -> str:
                return self.brand_name

class category(models.Model):
        name=models.CharField(max_length=100)

        def __str__(self) -> str:
             return self.name
        
class section(models.Model):
        name=models.CharField(max_length=100)

        def __str__(self) -> str:
             return self.name


class Product(models.Model):
        total_quantity = models.IntegerField(default=10)
        name=models.CharField(max_length=100)
        available = models.IntegerField(default=10)
        image= models.ImageField()
        discount =models.IntegerField(default=7)
        tax =models.IntegerField(null=True,default=0)
        packing_cost =models.IntegerField(null=True,default=0)
        delivery_charge =models.IntegerField(null=True,default=0)
        big_img=models.ImageField()
        small_img_first=models.ImageField()
        small_img_second=models.ImageField()
        price=models.IntegerField()
        Product_information = RichTextField(null=True,default="Transform your living spaces into stunning showcases of style and sophistication with our exquisite collection of furniture. Crafted with meticulous attention to detail and unparalleled quality, each piece is a testament to exceptional craftsmanship and timeless design")
        category=models.ForeignKey(category,on_delete=models.CASCADE)
        weight=models.IntegerField(null=True,default=110)
        dimensions=models.CharField(max_length=100,null=True,default="18 inches x 18 inches x 36 inches")
        color=models.CharField(max_length=100,null=True,default="white")
        size=models.CharField(max_length=100,null=True,default="Medium")
        slug = models.SlugField(default='',max_length=500,unique=True,blank=True)

        def __str__(self) -> str:
                return self.name
        

        def save(self, *args, **kwargs):
        # Generate the slug if it is not already set
                if not self.slug:
                        self.slug = self.generate_slug()
                super().save(*args, **kwargs)

        def generate_slug(self):
                return self.name.replace(" ", "-").lower()
        
        def get_absolute_url(self):
                return reverse('product_detail', kwargs={'slug': self.slug})


        # def save(self,*args , kwargs):
        #        self.slug = generate_slug(self.product_name)
        #        super(Product, self).save(*args , kwargs)

        # def get_absolute_url(self):
        #      return reverse("product_detail", args=[self.slug])

        class Meta:
             db_table = "app_Product"

# def generate_slug(instance, new_slug=None):
#     slug = slugify(instance.product_name)
#     if new_slug is not None:
#         slug = new_slug
#     qs = product.objects.filter(slug=slug).order_by('-id')
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return generate_slug(instance, new_slug=new_slug)
#     return slug

def generate_slug(title:str )->str:
        title=slugify(title)

        while(Product.objects.filter(slug=title).exists()):
              title=f'{slugify(title)}-{str(uuid.uuid4())[:4]}'

        return title

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)

        # pre_save.connect(pre_save_post_receiver, product)


class product_img(models.Model):
        product =models.ForeignKey(Product,on_delete=models.CASCADE)
        p_image=models.ImageField() 
 
        def __str__(self) -> str:
                return self.product.name



#===========================================================================================



class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'
    REFUNDED = 'refunded', 'Refunded'




#========================order-sedction===================#
class Order(models.Model):
       user=models.ForeignKey(User,on_delete=models.CASCADE)
       first_name=models.CharField(max_length=100)
       address=models.TextField()
       country=models.CharField(max_length=100)
       address=models.CharField(max_length=100)
       city_town=models.CharField(max_length=100)
       state=models.CharField(max_length=100)
       pincode=models.IntegerField()
       email=models.EmailField(max_length=100)
       amount=models.CharField(max_length=100)
       phone=models.IntegerField()
       payment_id=models.CharField(max_length=300,null=True,blank=True)
       paid=models.BooleanField(default=False,null=True)
       date=models.DateField(auto_now_add=True)

       payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices)
       razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)


       def __str__(self) -> str:
               return self.user.username 
       
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Product_Images/Order_Img")
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username


#===================================accounts_models_=========================#
User=models.ForeignKey(User, on_delete=models.CASCADE)