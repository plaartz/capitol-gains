import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.controllers import get_transactions

@require_http_methods(['POST'])
@csrf_exempt # idk if the react post request sends a csrf token
def search_view(request):
    """
    POST method which provides transactions that are searched by the user

    @return    retursn JsonResponse with requested data or an error message 
    """

    if not request.body or request.body is None or request.body == b'' :
        return JsonResponse({"error": "No body provided!"}, status = 400)

    data = json.loads(request.body)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    politician_type = data.get("politician_type")
    politician_house = data.get("politician_house")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    page_no = request.GET.get("pageNo")
    page_size = request.GET.get("pageSize")

    # Handle page number
    if page_no is None:
        page_no = 1    # We are defaulting to the first page
    else:
        page_no = max(1, int(page_no))

    # Handle invalid page size
    if page_size is None:
        page_size = 100    # We are defaulting to page size 100
    else:
        page_size = min(max(int(page_size), 1), 100)    # Ensures 1 <= page size <= 100

    transaction_data, size = get_transactions(
        first_name, last_name,
        politician_type,
        politician_house,
        start_date,
        end_date,
        page_no,
        page_size
    )

    response_data = {
        'data': transaction_data,
        'size': size
    }

    return JsonResponse(response_data, safe = False)
