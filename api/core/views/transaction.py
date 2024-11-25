from json import loads, JSONDecodeError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.controllers import transaction

@require_http_methods(["POST"])
def upload_transaction_information(request) -> JsonResponse:
    """
    private POST view for developers to upload stock transactions scraped from government website
    @return     JsonResponse with a success message or a detailed error message
    """
    try:
        data = loads(request.body)
    except JSONDecodeError:
        return JsonResponse({"error":"Invalid JSON"},status=400)
    status = transaction.upload_transactions(data['data'])
    if status == 200:
        return JsonResponse({"status":"ok","message": "Transactions uploaded"}, status=200)
    if status == 400:
        return JsonResponse({"error": "Bad request, missing or invalid data"}, status=400)
    if status == 409:
        return JsonResponse({"error": "Conflict, integrity error with the database"}, status=409)
    return JsonResponse({"error": "Internal server error when uploading transactions"}, status=500)

@require_http_methods(["GET"])
def fetch_transaction_price_info(request) -> JsonResponse:
    """
    GET method to get price information for the provided transaction.

    :returns JsonResponse: Returns a JsonResponse
    """
    transaction_id = request.GET.get("id")
    if transaction_id is None:
        return JsonResponse({"error": "No transaction id provided"},status=400)
    try:
        transaction_id = int(transaction_id)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Bad transaction id provided"},status=400)

    data, status = transaction.get_price_information(transaction_id)

    if status == 400:
        return JsonResponse({"error":"Error fetching data"},status=400)
    #Test data reload now
    return JsonResponse({"prices":data,"size":len(data)})
