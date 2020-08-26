from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from typing import List
from product.models import Category, Product
from openfoodfacts.api import Api, DataCleaner


class FillDatabase:
    """ Class in charge of OpenFoodFacts data recovery and integration in database """

    def __init__(self, categories: List[str]) -> None:
        self.api: Api = Api()
        self.clean_datas: DataCleaner = DataCleaner()
        self.categories: List[str] = categories

    def run(self) -> None:
        Product.objects.all().delete()
        Category.objects.all().delete()
        for category in self.categories:
            result = self.api.get_data(category)
            category = Category.objects.create(name=category)
            for product in self.clean_datas.get_product(result):
                self.insert_database(product, category)
                

    def insert_database(self, product, category) -> None:
        Product.objects.create(**product)
        category.products.add(product)


class Command(BaseCommand):
    help: str = "Lance la récupération des données de l'API OpenFoodFacts pour remplir la base de données PurBeurre"

    def handle(self, *args, **options) -> None:
        print("Lancement de la récupération des données de l'API OFF")
        categories = [
            "Sodas",
            "Desserts",
            "Sauces",
        ]
        fill_database: FillDatabase = FillDatabase(categories)
        fill_database.run()

        print("Récupération terminée")
