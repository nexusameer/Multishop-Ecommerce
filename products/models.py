from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_image= models.ImageField(upload_to='product_images', null=True, blank=True)
    org_price = models.IntegerField(null=True, blank=True)
    dis_price = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.org_price and self.dis_price is None:
            self.dis_price = self.org_price * 0.5
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name