import json
import pytest
from django.http import HttpResponse
from django.test import Client, TestCase
from product.models import Category, Product
from tests.conftest import Config
from user.models import User


class TestFavoritesSubstituteView(TestCase):
    def test_favorites_substitutes(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """

        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        client.login(username="test@mail.com", password="password8chars")
        response: HttpResponse = client.get("/favorites/",)
        assert response.status_code == 200  # Testing redirection

    def test_favorites_substitutes_not_connected(self) -> None:
        """Test if the url returns a correct 302 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get("/favorites/",)
        assert response.status_code == 302  # Testing redirection


class TestFavoriteSaveView(TestCase):
    @pytest.mark.django_db(transaction=True)
    def test_add_favorite(self) -> None:
        """Test the correct favorite registration.
        """
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        client.login(username="test@mail.com", password="password8chars")
        category: Category = Category.objects.create(name="Boissons")
        for product in Config.PRODUCT_AND_SUBSTITUTE_DATA["product"]:
            Product.objects.create(**product)
            category.products.add(product["code"])

        response: HttpResponse = client.post(
            "/favorites/add",
            {"product": "3068320115161", "substitute": "3068320115161",},
        )
        json_response: dict = json.loads(response.content.decode("utf-8"))[
            "favori_added"
        ]

        self.assertEqual(json_response, "success")

    def test_add_favorite_not_connected(self) -> None:
        """Test if the url returns a correct 302 http status code.
        """
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        category: Category = Category.objects.create(name="Boissons")
        for product in Config.PRODUCT_AND_SUBSTITUTE_DATA["product"]:
            Product.objects.create(**product)
            category.products.add(product["code"])

        response: HttpResponse = client.post(
            "/favorites/add",
            {"product": "3068320115161", "substitute": "3068320115161",},
        )
        self.assertEqual(response.status_code, 302)
