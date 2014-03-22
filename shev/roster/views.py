from django.http import HttpResponse, HttpResponseNotFound

def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return HttpResponse("<h1>Whatchew talking about?</h1>")
