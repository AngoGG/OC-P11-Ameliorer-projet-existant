from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, View
from product.models import Product
from product.views import Product
from user.models import User
from .models import Substitute


class FavoritesSubstituteView(LoginRequiredMixin, ListView):
    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user
        favorites: QuerySet = Substitute.get_favorite(user)
        return render(
            request, "substitute/favorites_substitutes.html", {"products": favorites,},
        )


class FavoriteSaveView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user
        product: QuerySet = Product.objects.filter(
            code=request.POST.get("product")
        ).first()
        substitute: QuerySet = Product.objects.filter(
            code=request.POST.get("substitute")
        ).first()
        Substitute.add_favorite(user, product, substitute)
        return JsonResponse({"favori_added": "success",})
