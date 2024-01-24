from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import *
from .permissions import IsAuthorOrAdmin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import logging
from ..rating.serializers import RatingSerializer

logger = logging.getLogger(__name__)


class Pagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category', 'stock')

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return IsAuthenticated(), IsAuthorOrAdmin(),
        return IsAuthenticatedOrReadOnly(),

    def perform_create(self, serializer):
        logger.info(self.request.user)
        serializer.save(owner=self.request.user)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'GET':
            ratings = product.ratings.all()
            serializer = RatingSerializer(instance=ratings, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('You already rated this product', status=400)
            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return Response("You didn't rated this product")
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Deleted', status=204)


@api_view(['GET'])
def get_hello(request):
    print(request.hello)
    return Response('hello')

