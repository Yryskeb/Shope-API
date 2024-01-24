from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model

from apps.account.views import LoginView
from apps.product.models import Product
from apps.category.models import Category
from apps.product.views import ProductViewSet

User = get_user_model()


class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.access_token = self.setup_user_token()
        self.setup_category()
        self.setup_product()

    def setup_user(self):
        return User.objects.create_superuser('admin@ad.ru', '1')

    def setup_category(self):
        Category.objects.create(name='category1')

    def setup_product(self):
        products = [
            Product(
                owner=self.user, title='test1', category=Category.objects.first(),
                price=1200.00, stock='in_stock'
            ),
            Product(
                owner=self.user, title='test2', category=Category.objects.first(),
                price=1200.00, stock='in_stock'
            ),
            Product(
                owner=self.user, title='test3', category=Category.objects.first(),
                price=1200.00, stock='in_stock'
            )
        ]
        Product.objects.bulk_create(products)

    def setup_user_token(self):
        data = {
            'email': 'admin@ad.ru',
            'password': '1'
        }
        request = self.factory.post('api/v1/account/login', data)
        view = LoginView.as_view()
        response = view(request)
        return response.data['access']

    def test_get_product(self):
        request = self.factory.get('api/v1/product')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 200
        assert Product.objects.count() == 3

    def test_post_product(self):
        image = open('/home/myrza/Documents/makers/week13/metro/media/products/rock.jpeg', 'rb')
        data = {
            'owner': self.user.id,
            'title': 'test2',
            'category': Category.objects.first().slug,
            'price': 122.22,
            'stock': 'in_stock',
            'image': image
        }
        request = self.factory.post('api/v1/product', data, HTTP_AUTHORIZATION='Bearer '+self.access_token)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201




