from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "app/home.html")


class LegalNoticeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "app/legal_notice.html")
