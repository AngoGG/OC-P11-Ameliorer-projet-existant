import pytest
from django.db.models.query import QuerySet
from django.test import TestCase
from product.models import Product
from substitute.models import Substitute
from tests.conftest import Config
from user.models import User


class TestSubstitute(TestCase):
    @pytest.mark.django_db(transaction=True)
    def test_add_favorite(self) -> None:
        """Test if a favorite is correctly saved in database
        """

        user: User = User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        product_code: str = "3068320115160"
        code_substitute: str = "3068320115161"
        for product in Config.PRODUCT_AND_SUBSTITUTE_DATA["product"]:
            Product.objects.create(**product)

        product: QuerySet = Product.objects.filter(code=product_code).first()
        substitute: QuerySet = Product.objects.filter(code=code_substitute).first()

        Substitute.add_favorite(user, product, substitute)
        substitutes: QuerySet = Substitute.objects.filter(user=user)
        assert len(substitutes) == 1
        for substitute in substitutes:
            assert substitute.user.email == "test@mail.com"
            assert substitute.product.code == product_code
            assert substitute.substitute.code == code_substitute

    @pytest.mark.django_db(transaction=True)
    def test_get_favorite(self) -> None:
        """Test the correct retrieving of a user favorites products
        """
        user: User = User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        product_code: str = "3068320115160"
        code_substitute: str = "3068320115161"
        for product in Config.PRODUCT_AND_SUBSTITUTE_DATA["product"]:
            Product.objects.create(**product)

        product: QuerySet = Product.objects.filter(code=product_code).first()
        substitute: QuerySet = Product.objects.filter(code=code_substitute).first()

        Substitute.objects.create(user=user, product=product, substitute=substitute)

        favorite: QuerySet = Substitute.get_favorite(user)

        for fav in favorite:
            assert fav.user.email == "test@mail.com"
            assert fav.product_id == product_code
            assert fav.substitute_id == code_substitute
