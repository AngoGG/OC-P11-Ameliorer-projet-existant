from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from . import views

app_name: str = "substitute"

urlpatterns = [
    url(r"^$", views.FavoritesSubstituteView.as_view(), name="favorites",),
    path(r"add", views.FavoriteSaveView.as_view(), name="save"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns
