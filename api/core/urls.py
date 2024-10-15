from django.urls import path

from . import views

urlpatterns = [
    path("test",views.test.view1,name="Index"),
    path("fetch-stock-ids", views.stock.get_stocks, name="Fetch Stocks"),
    path("upload-stock-prices", views.stock.upload_stock_prices, name="Upload Prices"),
    path("search", views.search.search_view, name = "Index"),
]
