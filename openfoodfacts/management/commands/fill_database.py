from pathlib import Path
from typing import Dict, List
from django.core.management.base import BaseCommand, CommandParser
import yaml
from product.models import Category, Product
from openfoodfacts.api import Api, DataCleaner


class FillDatabase:
    """ Class in charge of OpenFoodFacts data recovery and integration in database """

    def __init__(self, categories: List[str], clean_database) -> None:
        self.api: Api = Api()
        self.clean_datas: DataCleaner = DataCleaner()
        self.categories: List[str] = categories
        self.clean_database: bool = clean_database

    def run(self) -> None:
        if self.clean_database:
            Product.objects.all().delete()
            Category.objects.all().delete()
        for category_name in self.categories:
            result = self.api.get_data(category_name)
            for product in self.clean_datas.get_product(result):
                self.insert_database(product, category_name)

    @staticmethod
    def insert_database(product_data: Dict, category_name: str) -> None:
        """Method in charge of the database insertion for a product and its relationned category

        Args:
            product_data (Dict): A dictionnary containing all datas
                to be inserted in database for a product.
            category (Category): The Products category objects,
                used to create the relation in database.
        """

        product_object, product_created = Product.objects.get_or_create(**product_data)
        category_object, category_created = Category.objects.get_or_create(
            name=category_name
        )

        category_object.products.add(product_object)
        category_object.save()


class Command(BaseCommand):
    """This class is in charge of the custom command process.
        Get and add all arguments and run the database insertion process.
    """

    help: str = "Lance la récupération des données de l'API OpenFoodFacts pour remplir la base de données PurBeurre"

    def __init__(self) -> None:
        self.categories_yaml_path: Path = Path(__file__).parent.parent.parent.joinpath(
            "categoriesList.yml"
        )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--category",
            action="append",
            default=[],
            dest="categories",
            help="List of the expected categories products to retrieve from OFF)",
        )

        parser.add_argument(
            "--clean",
            action="store_true",
            default=False,
            dest="clean",
            help="Clean the database before fill it with OFF data",
        )

    def handle(self, *args, **options) -> None:
        print("Lancement de la récupération des données de l'API OFF")

        with self.categories_yaml_path.open() as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)

        if not options["categories"]:
            options["categories"] = data["categories"]
        fill_database: FillDatabase = FillDatabase(
            options["categories"], options["clean"]
        )
        fill_database.run()

        print("Récupération terminée")
