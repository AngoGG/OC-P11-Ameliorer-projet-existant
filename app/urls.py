"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfî
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from product.views import ProductAutocompleteView
from . import views


app_name: str = "app"

urlpatterns: List = [
    path(r"", views.HomeView.as_view(), name="home"),
    path(r"legal", views.LegalNoticeView.as_view(), name="legal_notice"),
    path(
        r"product_autocomplete",
        ProductAutocompleteView.as_view(),
        name="product_autocomplete",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns
