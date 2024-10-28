from django.urls import path

from . import views

urlpatterns = [
    path("test",views.test.view1,name="Index"),
    path("fetch-stock-ids", views.stock.get_stocks, name="Fetch Stocks"),
    path("upload-stock-prices", views.stock.upload_stock_prices, name="Upload Prices"),
    path("search", views.search.search_view, name = "Search"),
    path("get-transaction", views.search.fetch_transaction, name = "Get Transaction"),
    path(
        "upload-transactions",
        views.transaction.upload_transaction_information,
        name="transaction"
    )
]
