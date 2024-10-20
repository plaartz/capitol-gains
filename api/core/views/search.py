from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.controllers import get_transactions

@require_http_methods(['POST'])
@csrf_exempt # idk if the react post request sends a csrf token
def search_view(request):
    """
    POST method which provides transactions that are searched by the user

    @return    retursn JsonResponse with requested data or an error message 
    """
    data = json.loads(request.body)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    politician_type = data.get("politician_type")
    politician_house = data.get("politician_house")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    pageNo = data.get("pageNo")
    pageSize = data.get("pageSize")

    # Handle invalid page number
    if pageNo == 0:
        return JsonResponse({'Error': "Page number must be greater than zero!"}, status = 400)

    # Handle invalid page size
    if pageSize > 100:
        return JsonResponse({'Error': "Maximum page size is 100!"}, status = 400)
    
    transaction_data = get_transactions(first_name, last_name, politician_type, politician_house, start_date, end_date, pageNo, pageSize)
    size = len(transaction_data)

    response_data = {
        'data': transaction_data,
        'size': size
    }

    return JsonResponse(response_data, safe = False)
    