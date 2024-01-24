from django.db import models
from apps.product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'too bad'),
        (2, 'bad'),
        (3, 'normal'),
        (4, 'good'),
        (5, 'excellent')
    )

    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ['owner', 'product']



