from django.db import models
from django.contrib.auth import get_user_model
from apps.category.models import Category

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'в наличии'),
        ('out_of_stock', 'нет в наличии')
    )

    owner = models.ForeignKey(User, related_name='products', on_delete=models.RESTRICT)
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.CharField(choices=STATUS_CHOICES, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
