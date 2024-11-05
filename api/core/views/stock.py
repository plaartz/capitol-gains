from json import loads, JSONDecodeError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.controllers import stock
@require_http_methods(["GET"])
def get_stocks(_) -> JsonResponse:
    """
    private GET view for users fetching stocks that aren't updated
    @return     JsonResponse with the data or a detailed error message
    """
    try:
        data, status = stock.get_stocks_to_update()
    #pylint: disable=broad-exception-caught
    except Exception as e:
        return {"status":500,"error":str(e)}

    response = {"status":status}
    if status == 200:
        response["stocks"] = data
        response["size"] = len(data)
    else:
        response["error"] = data
    return JsonResponse(response,status=status)

@require_http_methods(["POST"])
def upload_stock_prices(request) -> JsonResponse:
    """
    private POST view for users posting stocks that need to be updated
    @return     JsonResponse with a success message or a detailed error message
    """
    try:
        data = loads(request.body)
    except JSONDecodeError:
        return JsonResponse({"error":"Invalid JSON"},status=400)
    status = stock.upload_stock_prices(data['data'])
    if status == 200:
        return JsonResponse({"status":"ok","message": "Prices uploaded"}, status=200)
    if status == 400:
        return JsonResponse({"error": "Bad request, missing or invalid data"}, status=400)
    if status == 409:
        return JsonResponse({"error": "Conflict, integrity error with the database"}, status=409)
    if status == 500:
        return JsonResponse(
            {"error": "Internal server error while updating stock prices"},
            status=500
        )
    return JsonResponse({"error": "Unexpected error occurred"}, status=500)
