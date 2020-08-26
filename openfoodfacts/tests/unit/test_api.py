#!/usr/bin/env python3
"""
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-05-02
@note    0.0.1 (2020-05-02) : Init file
"""

from typing import Dict
import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from openfoodfacts.api import Api, DataCleaner
from openfoodfacts.management.commands.fill_database import FillDatabase
from product.models import Category, Product
from tests.conftest import Config


class TestApi:
    """Api Test Class.
    """

    def test__product_is_valid(self) -> None:
        """ Method testing the generation of a product for database insertion """
        data_cleaner: DataCleaner = DataCleaner()
        assert data_cleaner._product_is_valid(Config.VALID_PRODUCT_DATA) is True
        assert data_cleaner._product_is_valid(Config.PRODUCT_DATA_EMPTY_FIELD) is False
        assert (
            data_cleaner._product_is_valid(Config.PRODUCT_DATA_MISSING_FIELD) is False
        )

    def test__nutrients_are_valid(self) -> None:
        """ Method testing the generation of a product for database insertion """
        data_cleaner: DataCleaner = DataCleaner()
        assert data_cleaner._nutrients_are_valid(Config.VALID_NUTRIMENTS_DATA) is True
        assert (
            data_cleaner._nutrients_are_valid(Config.NUTRIMENTS_DATA_MISSING_FIELD)
            is False
        )

    def test_get_product(self) -> None:
        """ Method testing the generation of a product for database insertion """
        results = Config.PRODUCT_RESULTS
        data_cleaner: DataCleaner = DataCleaner()
        for product in data_cleaner.get_product(Config.OPENFOODFACTS_DATA):
            assert product == results

    @pytest.mark.django_db(transaction=True)
    def test_insert_database(self):
        """ Method testing the insertion of a product into a database """
        expected_results = Config.DATABASE_EXPECTED
        category_name = "Boissons"
        category_object = Category.objects.create(name=category_name)

        fill_database: FillDatabase = FillDatabase(category_name)
        fill_database.insert_database(expected_results, category_object)
        assert Product.objects.count() == 1

        product_data = Product.objects.first()
        for attr_key, attr_val in expected_results.items():
            assert expected_results[attr_key] == getattr(product_data, attr_key)

        assert Category.objects.count() == 1
        assert Category.objects.first().name == category_name
        assert Product.objects.first().category_set.first().name  == category_name

    def test_get_data(self, monkeypatch: MonkeyPatch) -> None:
        """ Method testing data recovery via the OpenFoodFacts API """

        class MockResponse:
            @staticmethod
            def json() -> Dict:
                return Config.OPENFOODFACTS_DATA

        api: Api = Api()

        def mockreturn(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mockreturn)
        assert api.get_data("Boissons") == Config.OPENFOODFACTS_DATA
