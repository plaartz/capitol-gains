from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from json import loads, JSONDecodeError

@require_http_methods(["GET"])
def get_stocks(request) -> JsonResponse:
    return JsonResponse({"stocks":[
        {"ticker":"AVGO","date_range":1}
    ]})

@require_http_methods(["POST"])
def upload_stock_prices(request) -> HttpResponse:
    try:
        #print(request.body)
        data = loads(request.body)
        print(data)
    except JSONDecodeError:
        return JsonResponse({"error":"Invalid JSON"},status=400)
    return HttpResponse("Files uploaded")