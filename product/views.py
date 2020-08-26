from typing import List
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from substitute.models import Substitute
from .models import Product


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products: QuerySet = Product.objects.filter(
            name__istartswith=request.GET.get("search")
        ).order_by("-nutriscore_grade")
        return render(request, "product/index.html", {"products": products})


class DetailView(View):
    def get(self, request: HttpRequest, code_product: str) -> HttpResponse:
        product: QuerySet = Product.objects.get(code=code_product)
        return render(request, "product/detail.html", {"product": product})


class SubstituteIndexView(View):
    def get(self, request: HttpRequest, code_product: str) -> HttpResponse:
        """Get all the substitute of the requested product
        and send it with the substitute template.
        """

        product: QuerySet = Product.objects.get(code=code_product)
        substitutes: QuerySet = Product.get_substitute(
            code_product, product.nutriscore_grade
        )
        user_favorite_list: List = []
        if request.user.is_authenticated:
            user_favorites: QuerySet = Substitute.get_favorite(request.user)
            for favorite in user_favorites:
                user_favorite_list.append(favorite.substitute_id)
        return render(
            request,
            "product/substitutes_index.html",
            {
                "product_code": code_product,
                "product_name": product.name,
                "product_image": product.image,
                "substitutes": substitutes,
                "favorites": user_favorite_list,
            },
        )


class ProductAutocompleteView(View):
    def get(self, request) -> HttpResponse:
        """Get and send the list of all products names
        in database for the autocompletion.
        """

        products_list: List = []
        for product in Product.objects.all():
            products_list.append(product.name)
        return JsonResponse(products_list, safe=False)
