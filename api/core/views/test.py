from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(['GET'])
def view1(request):
    return HttpResponse("Hello World 1")