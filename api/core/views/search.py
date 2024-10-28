#pylint: disable=too-many-locals
import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.controllers import get_transactions, get_transaction

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
    order_by = request.GET.get("orderBy")
    order = request.GET.get("order")

    # Make sure the order by is a valid selection
    valid_options = [
        "transaction_date",
        "disclosure_date",
        "transaction_type",
        "transaction_amount",
        "politician_type",
        "politician_house",
        "first_name",
        "last_name",
        "stock_ticker",
        "stock_price"
    ]

    if order_by is None or order_by == "" or order_by.lower() not in valid_options:
        order_by = "transaction_date"
    order_by = order_by.lower()

    # Handle order
    if order is None or order == "" or (order.upper() not in ["ASC", "DESC"]):
        order = "DESC"
    order = order.upper()

    # Handle page number
    if page_no is None:
        page_no = 1    # We are defaulting to the first page
    else:
        # Make sure we are getting an int for page number
        try:
            page_no = int(page_no)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'pageNo must be an integer!'}, status=400)
        page_no = max(1, page_no)

    # Handle invalid page size
    if page_size is None:
        page_size = 100    # We are defaulting to page size 100
    else:
        # Make sure we are getting an int for page size
        try:
            page_size = int(page_size)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'pageSize must be an integer!'}, status=400)
        page_size = min(max(page_size, 1), 100)    # Ensures 1 <= page size <= 100

    transaction_data, size = get_transactions(
        first_name, last_name,
        politician_type,
        politician_house,
        start_date,
        end_date,
        page_no,
        page_size,
        order_by,
        order
    )

    response_data = {
        'data': transaction_data,
        'size': size
    }

    return JsonResponse(response_data, safe = False)

@require_http_methods(['GET'])
def fetch_transaction(request):

    transaction_id = request.GET.get("id")
    if transaction_id is None:
        return JsonResponse({"error": "No transaction id provided"},status=400)
    try:
        transaction_id = int(transaction_id)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Bad transaction id provided"},status=400)

    transaction, status = get_transaction(transaction_id)

    if status == 400:
        return JsonResponse({"error":"Error fetching transaction"},status=400)
    
    return JsonResponse({"transaction":transaction}) 


