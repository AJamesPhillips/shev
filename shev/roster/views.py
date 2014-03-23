from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from . import models
from datetime import datetime


def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return HttpResponse("<h1>Whatchew talking about?</h1>")

def day(request, day, month, year):
    the_day = get_object_or_404(models.Day, day = datetime(int(year),int(month),int(day)))
    the_shifts = the_day.shift_set.all()
    return render_to_response("day.html",{'day': the_day, 'shifts': the_shifts})
    return HttpResponse("<h1>%s %s %s</h1> %s" % (day, month, year, the_day))
