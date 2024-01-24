from django.db.models import Avg
from rest_framework import serializers
from .models import Product
from apps.rating.serializers import RatingSerializer


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr.setdefault('rating', instance.ratings.aggregate(Avg('rating')))
        rating = repr['rating']
        rating.setdefault('rating_count', instance.ratings.count())
        return repr





