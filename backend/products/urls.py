from django.urls import path

from .views import ProductSearchView

urlpatterns = [
    path("products/search/", ProductSearchView.as_view(), name="product-search"),
]