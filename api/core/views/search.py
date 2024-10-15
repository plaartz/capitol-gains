from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.controllers import SearchController

@require_http_methods(['POST'])
@csrf_exempt # idk if the react post request sends a csrf token
def search_view(request):
    data = json.loads(request.body)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    politician_type = data.get("politician_type")
    politician_house = data.get("politician_house")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    search_controller = SearchController(first_name, last_name, politician_type, politician_house, start_date, end_date)
    transaction_data = search_controller.get_transactions()

    return JsonResponse(transaction_data, safe = False)