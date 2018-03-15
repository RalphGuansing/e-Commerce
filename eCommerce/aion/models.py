from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField


class Address_Details(models.Model):
    house_number = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    subdivision = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.IntegerField(default=0)
    country = models.CharField(max_length=200)

    #(House #, Street, Subdivision, City, Postal Code, Country)
    def __str__(self):
        return '('+ self.house_number +', '+ self.street +', '+ self.subdivision +', '+ self.city +', '+ str(self.postal_code) +', '+ self.country +')'

    class Meta:
        verbose_name_plural = "Address_Details"

class User_Details(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    billing_address = models.ForeignKey(Address_Details, on_delete=models.CASCADE, related_name ="billing_address", blank=True,null=True)
    shipping_address = models.ForeignKey(Address_Details, on_delete=models.CASCADE,related_name ="shipping_address", blank=True,null=True)

    type_choice = (
        ('Customer', 'Customer'),
        ('Product Manager', 'Product Manager'),
        ('Accounting Manager', 'Accounting Manager'),
        ('Administrator', 'Administrator'),
    )

    account_type = models.CharField(max_length=50, choices=type_choice, default=type_choice[0][0])

    def __str__(self):
        return str(self.user_id) +', '+ self.first_name +' '+ self.last_name

    class Meta:
        verbose_name_plural = "User_Details"


class Product(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    item_photo = models.FileField(blank=True,null=True)
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(default='')
    item_quantity = models.IntegerField(default=0)
    item_price = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    isPurchased = models.BooleanField(default=False)

    type_choice = (
        ('Analog watch', 'Analog watch'),
        ('Digital watch', 'Digital watch'),
        ('Smart watch', 'Smart watch'),
    )

    item_type = models.CharField(max_length=50, choices=type_choice, default=type_choice[0][0])
    item_type_slug = AutoSlugField(populate_from='item_type', blank=True)

    def __str__(self):
        return self.item_name +' ('+str(self.id)+') '

    def get_absolute_url(self):
        return reverse('home')

class Cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    isPurchased = models.BooleanField(default=False)

    def __str__(self):
        return 'cart of ' + self.user_id.username

class Order(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart,on_delete=models.CASCADE)
    item_quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'order of ' + self.cart_id.user_id.username +' product '+str(self.product_id.id )

class Review(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    commentText = models.CharField(max_length=250)
    stars = models.DecimalField(max_digits=2, decimal_places=1)
    
    
