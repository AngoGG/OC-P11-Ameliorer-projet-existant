from django.db import models

# Create your models here.


class Product(models.Model):
    code: models.CharField = models.CharField(
        primary_key=True, max_length=55, blank=False, unique=True
    )
    name: models.CharField = models.CharField(max_length=255, blank=False)
    nutriscore_grade: models.CharField = models.CharField(max_length=1, blank=False)
    url: models.CharField = models.CharField(max_length=255, blank=False)
    image: models.URLField = models.URLField(max_length=255, blank=False)
    nutrient_levels: models.URLField = models.URLField(max_length=255, blank=False)
    carbohydrates_100g: models.FloatField = models.FloatField(null=True)
    sugars_100g: models.FloatField = models.FloatField(null=True)
    fat_100g: models.FloatField = models.FloatField(null=True)
    saturated_fat_100g: models.FloatField = models.FloatField(null=True)
    proteins_100g: models.FloatField = models.FloatField(null=True)
    salt_100g: models.FloatField = models.FloatField(null=True)
    kcal_100g: models.FloatField = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_substitute(
        product_code: str, product_nutriscore: str
    ) -> models.query.QuerySet:
        product_category = Product.get_category(product_code)[0]
        return Product.objects.filter(
            nutriscore_grade__lte=product_nutriscore, category__name=product_category
        ).order_by("nutriscore_grade")

    @staticmethod
    def get_category(product_code: str) -> models.query.QuerySet:
        product = Product.objects.get(pk=product_code)
        return product.category_set.all()


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=255, blank=False, unique=True)
    products: models.ManyToManyField = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return self.name
