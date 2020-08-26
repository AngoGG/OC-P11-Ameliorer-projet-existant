from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from . import views

app_name: str = "product"

urlpatterns = [
    path(r"search/", views.IndexView.as_view(), name="index"),
    path(r"<int:code_product>/", views.DetailView.as_view(), name="detail"),
    path(
        r"substitutes/<int:code_product>/",
        views.SubstituteIndexView.as_view(),
        name="search_substitutes",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns
