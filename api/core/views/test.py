from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.controllers import SearchController

@require_http_methods(['GET'])
def view1(request):
    """ Test docstring """
    test = request
    print(test)
    return HttpResponse("Hello World 1")
