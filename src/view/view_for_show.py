from django.http import HttpResponse
from django.template import loader

# Create your views here.


def index(request):
    index_html = loader.get_template("index.html")
    return HttpResponse(index_html.render({}, request))


def table_show(request):
    index_html = loader.get_template("table.html")
    return HttpResponse(index_html.render({}, request))
