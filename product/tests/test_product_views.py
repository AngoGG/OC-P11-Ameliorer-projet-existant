import pytest
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.test import Client, TestCase
from product.models import Product, Category
from tests.conftest import Config


class TestIndexView(TestCase):
    def test_index_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get(
            "/products/search/", {"search": "Product Name",},
        )
        assert response.status_code == 200


class TestDetailView(TestCase):
    @pytest.mark.django_db(transaction=True)
    def test_detail_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        Product.objects.create(**Config.DATABASE_EXPECTED)
        code_product: dict = Config.DATABASE_EXPECTED["code"]
        response: HttpResponse = client.get(f"/products/{code_product}/")
        assert response.status_code == 200


class TestSubstituteView(TestCase):
    @pytest.mark.django_db(transaction=True)
    def test_detail_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        product_code: str = "3068320115161"
        category: Category = Category.objects.create(name="Boissons")
        for product in Config.PRODUCT_AND_SUBSTITUTE_DATA["product"]:
            Product.objects.create(**product)
            category.products.add(product["code"])
        response: HttpResponse = client.get(f"/products/substitutes/{product_code}/")
        assert response.status_code == 200

