from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from typing import Dict, List
from product.models import Category, Product
from openfoodfacts.api import Api, DataCleaner


class FillDatabase:
    """ Class in charge of OpenFoodFacts data recovery and integration in database """

    def __init__(self, categories: List[str]) -> None:
        self.api: Api = Api()
        self.clean_datas: DataCleaner = DataCleaner()
        self.categories: List[str] = categories

    def run(self) -> None:
        # Product.objects.all().delete()
        # Category.objects.all().delete()
        for category_name in self.categories:
            result = self.api.get_data(category_name)
            for product in self.clean_datas.get_product(result):
                self.insert_database(product, category_name)

    def insert_database(self, product_data: Dict, category_name: str) -> None:
        """Method in charge of the database insertion for a product and its relationned category
        
        Args:
            product_data (Dict): A dictionnary containing all datas to be inserted in database for a product.
            category (Category): The Products category objects, used to create the relation in database.
        """

        product_object, product_created = Product.objects.get_or_create(**product_data)
        category_object, category_created = Category.objects.get_or_create(
            name=category_name
        )

        category_object.products.add(product_object)
        category_object.save()


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
