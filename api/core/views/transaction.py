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
