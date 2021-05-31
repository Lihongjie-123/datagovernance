from django.http import HttpResponse

# Create your views here.


def api_test(request):

    return HttpResponse("test ok")
